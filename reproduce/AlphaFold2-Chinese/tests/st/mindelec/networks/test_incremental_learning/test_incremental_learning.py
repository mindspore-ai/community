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
# ==============================================================================
"""reconstruct process."""
import os
import json
import math
import pytest
import numpy as np

from mindspore.common import set_seed
from mindspore import context, Tensor, nn, Parameter
from mindspore.train import DynamicLossScaleManager
from mindspore.train.callback import ModelCheckpoint, CheckpointConfig
from mindspore.train.serialization import load_checkpoint, load_param_into_net
import mindspore.common.dtype as ms_type
from mindspore.common.initializer import HeUniform


from mindelec.loss import Constraints
from mindelec.solver import Solver, LossAndTimeMonitor
from mindelec.common import L2
from mindelec.architecture import MultiScaleFCCell, MTLWeightedLossCell

from src.dataset import create_random_dataset
from src.lr_scheduler import MultiStepLR
from src.maxwell import Maxwell2DMur

set_seed(123456)
np.random.seed(123456)

context.set_context(mode=context.GRAPH_MODE, save_graphs=False, device_target="Ascend", save_graphs_path="./solver")


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_incremental_learning():
    """pretraining process"""
    print("pid:", os.getpid())
    mode = "pretrain"
    config = json.load(open("./pretrain.json"))
    preprocess_config(config)
    elec_train_dataset = create_random_dataset(config)
    train_dataset = elec_train_dataset.create_dataset(batch_size=config["batch_size"],
                                                      shuffle=True,
                                                      prebatched_data=True,
                                                      drop_remainder=True)
    epoch_steps = len(elec_train_dataset)
    print("check train dataset size: ", len(elec_train_dataset))

    # load ckpt
    if config.get("load_ckpt", False):
        param_dict = load_checkpoint(config["load_ckpt_path"])
        if mode == "pretrain":
            loaded_ckpt_dict = param_dict
        else:
            loaded_ckpt_dict = {}
            latent_vector_ckpt = 0
            for name in param_dict:
                if name == "model.latent_vector":
                    latent_vector_ckpt = param_dict[name].data.asnumpy()
                elif "network" in name and "moment" not in name:
                    loaded_ckpt_dict[name] = param_dict[name]

    # initialize latent vector
    num_scenarios = config["num_scenarios"]
    latent_size = config["latent_vector_size"]
    if mode == "pretrain":
        latent_init = np.random.randn(num_scenarios, latent_size) / np.sqrt(latent_size)
    else:
        latent_norm = np.mean(np.linalg.norm(latent_vector_ckpt, axis=1))
        print("check mean latent vector norm: ", latent_norm)
        latent_init = np.zeros((num_scenarios, latent_size))
    latent_vector = Parameter(Tensor(latent_init, ms_type.float32), requires_grad=True)

    network = MultiScaleFCCell(config["input_size"],
                               config["output_size"],
                               layers=config["layers"],
                               neurons=config["neurons"],
                               residual=config["residual"],
                               weight_init=HeUniform(negative_slope=math.sqrt(5)),
                               act="sin",
                               num_scales=config["num_scales"],
                               amp_factor=config["amp_factor"],
                               scale_factor=config["scale_factor"],
                               input_scale=config["input_scale"],
                               input_center=config["input_center"],
                               latent_vector=latent_vector
                               )

    network = network.to_float(ms_type.float16)
    network.input_scale.to_float(ms_type.float32)

    if config.get("enable_mtl", True):
        mtl_cell = MTLWeightedLossCell(num_losses=elec_train_dataset.num_dataset)
    else:
        mtl_cell = None

    # define problem
    train_prob = {}
    for dataset in elec_train_dataset.all_datasets:
        train_prob[dataset.name] = Maxwell2DMur(network=network, config=config,
                                                domain_column=dataset.name + "_points",
                                                ic_column=dataset.name + "_points",
                                                bc_column=dataset.name + "_points")
    print("check problem: ", train_prob)
    train_constraints = Constraints(elec_train_dataset, train_prob)

    # optimizer
    if mode == "pretrain":
        params = network.trainable_params() + mtl_cell.trainable_params()
        if config.get("load_ckpt", False):
            load_param_into_net(network, loaded_ckpt_dict)
            load_param_into_net(mtl_cell, loaded_ckpt_dict)
    else:
        if config.get("finetune_model"):
            model_params = network.trainable_params()
        else:
            model_params = [param for param in network.trainable_params()
                            if ("bias" not in param.name and "weight" not in param.name)]
        params = model_params + mtl_cell.trainable_params() if mtl_cell else model_params
        load_param_into_net(network, loaded_ckpt_dict)

    lr_scheduler = MultiStepLR(config["lr"], config["milestones"], config["lr_gamma"],
                               epoch_steps, config["train_epoch"])
    optimizer = nn.Adam(params, learning_rate=Tensor(lr_scheduler.get_lr()))

    # problem solver
    solver = Solver(network,
                    optimizer=optimizer,
                    mode="PINNs",
                    train_constraints=train_constraints,
                    test_constraints=None,
                    metrics={'l2': L2(), 'distance': nn.MAE()},
                    loss_fn='smooth_l1_loss',
                    loss_scale_manager=DynamicLossScaleManager(),
                    mtl_weighted_cell=mtl_cell,
                    latent_vector=latent_vector,
                    latent_reg=config["latent_reg"]
                    )

    loss_time_callback = LossAndTimeMonitor(epoch_steps)
    callbacks = [loss_time_callback]
    if config["save_ckpt"]:
        config_ck = CheckpointConfig(save_checkpoint_steps=10, keep_checkpoint_max=2)
        prefix = 'pretrain_maxwell_frq1e9' if mode == "pretrain" else 'reconstruct_maxwell_frq1e9'
        ckpoint_cb = ModelCheckpoint(prefix=prefix, directory=config["save_ckpt_path"], config=config_ck)
        callbacks += [ckpoint_cb]

    solver.train(config["train_epoch"], train_dataset, callbacks=callbacks, dataset_sink_mode=True)
    assert loss_time_callback.get_loss() <= 2.0
    assert loss_time_callback.get_step_time() <= 115.0


def preprocess_config(config):
    """preprocess to get the coefficients of electromagnetic field for each scenario"""
    eps_candidates = config["EPS_candidates"]
    mu_candidates = config["MU_candidates"]
    config["num_scenarios"] = len(eps_candidates) * len(mu_candidates)
    batch_size_single_scenario = config["train_batch_size"]
    config["batch_size"] = batch_size_single_scenario * config["num_scenarios"]
    eps_list = []
    for eps in eps_candidates:
        eps_list.extend([eps] * (batch_size_single_scenario * len(mu_candidates)))
    mu_list = []
    for mu in mu_candidates:
        mu_list.extend([mu] * batch_size_single_scenario)
    mu_list = mu_list * (len(eps_candidates))

    exp_name = "_" + config["Case"] + '_num_scenarios_' +  str(config["num_scenarios"]) \
               + "_latent_reg_" + str(config["latent_reg"])
    if config["save_ckpt"]:
        config["save_ckpt_path"] += exp_name

    config["vision_path"] += exp_name
    config["summary_path"] += exp_name
    print("check config: {}".format(config))
    config["eps_list"] = eps_list
    config["mu_list"] = mu_list
