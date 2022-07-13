# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""train process"""
import json
import math
import pytest
import numpy as np

from mindspore.common import set_seed
from mindspore import context, Tensor, nn
from mindspore.train import DynamicLossScaleManager
from mindspore.train.callback import ModelCheckpoint, CheckpointConfig
from mindspore.train.serialization import load_checkpoint, load_param_into_net
import mindspore.common.dtype as mstype
from mindspore.common.initializer import HeUniform

from mindelec.loss import Constraints
from mindelec.solver import Solver, LossAndTimeMonitor
from mindelec.common import L2
from mindelec.architecture import MultiScaleFCCell, MTLWeightedLossCell

from src.dataset import create_train_dataset, create_random_dataset
from src.maxwell import Maxwell2DMur
from src.lr_scheduler import MultiStepLR

set_seed(123456)
np.random.seed(123456)

context.set_context(mode=context.GRAPH_MODE, save_graphs=False, device_target="Ascend", save_graphs_path="./graph")


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_time_domain_maxwell():
    """training process"""
    config = json.load(open("./config.json"))
    print("check config: {}".format(config))
    if config["random_sampling"]:
        elec_train_dataset = create_random_dataset(config)
    else:
        elec_train_dataset = create_train_dataset(config["train_data_path"])
    train_dataset = elec_train_dataset.create_dataset(batch_size=config["train_batch_size"],
                                                      shuffle=True,
                                                      prebatched_data=True,
                                                      drop_remainder=True)
    steps_per_epoch = len(elec_train_dataset)
    print("check train dataset size: ", len(elec_train_dataset))

    # define network
    model = MultiScaleFCCell(config["input_size"],
                             config["output_size"],
                             layers=config["layers"],
                             neurons=config["neurons"],
                             input_scale=config["input_scale"],
                             residual=config["residual"],
                             weight_init=HeUniform(negative_slope=math.sqrt(5)),
                             act="sin",
                             num_scales=config["num_scales"],
                             amp_factor=config["amp_factor"],
                             scale_factor=config["scale_factor"]
                             )

    model.to_float(mstype.float16)
    model.input_scale.to_float(mstype.float32)
    mtl = MTLWeightedLossCell(num_losses=elec_train_dataset.num_dataset)

    # define problem
    train_prob = {}
    for dataset in elec_train_dataset.all_datasets:
        train_prob[dataset.name] = Maxwell2DMur(model=model, config=config,
                                                domain_name=dataset.name + "_points",
                                                ic_name=dataset.name + "_points",
                                                bc_name=dataset.name + "_points")
    print("check problem: ", train_prob)
    train_constraints = Constraints(elec_train_dataset, train_prob)

    # optimizer
    params = model.trainable_params() + mtl.trainable_params()
    lr_scheduler = MultiStepLR(config["lr"], config["milestones"], config["lr_gamma"],
                               steps_per_epoch, config["train_epoch"])
    lr = lr_scheduler.get_lr()
    optim = nn.Adam(params, learning_rate=Tensor(lr))

    if config["load_ckpt"]:
        param_dict = load_checkpoint(config["load_ckpt_path"])
        load_param_into_net(model, param_dict)
        load_param_into_net(mtl, param_dict)
    # define solver
    solver = Solver(model,
                    optimizer=optim,
                    mode="PINNs",
                    train_constraints=train_constraints,
                    test_constraints=None,
                    metrics={'l2': L2(), 'distance': nn.MAE()},
                    loss_fn='smooth_l1_loss',
                    loss_scale_manager=DynamicLossScaleManager(init_loss_scale=2 ** 10, scale_window=2000),
                    mtl_weighted_cell=mtl,
                    )

    loss_time_callback = LossAndTimeMonitor(steps_per_epoch)
    callbacks = [loss_time_callback]
    if config["save_ckpt"]:
        config_ck = CheckpointConfig(save_checkpoint_steps=10,
                                     keep_checkpoint_max=2)
        ckpoint_cb = ModelCheckpoint(prefix='ckpt_maxwell_frq1e9',
                                     directory=config["save_ckpt_path"], config=config_ck)
        callbacks += [ckpoint_cb]

    solver.train(config["train_epoch"], train_dataset, callbacks=callbacks, dataset_sink_mode=True)

    assert loss_time_callback.get_loss() <= 2.5
    assert loss_time_callback.get_step_time() <= 75.0
