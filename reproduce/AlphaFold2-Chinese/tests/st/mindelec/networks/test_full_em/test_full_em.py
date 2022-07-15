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
"""
train
"""
import os
import time
import numpy as np
import pytest

import mindspore.nn as nn
import mindspore.common.initializer as weight_init
from mindspore.common import set_seed
from mindspore import Tensor
from mindspore import context
from mindspore.train.callback import Callback, LossMonitor
from mindspore.train.loss_scale_manager import DynamicLossScaleManager
from mindelec.solver import Solver
from src.dataset import create_dataset
from src.loss import MyMSELoss, EvaLMetric
from src.maxwell_model import Maxwell3D
from src.config import config
from src.sample import generate_data

set_seed(0)
np.random.seed(0)

train_data_path = "./train_data_em/"
test_data_path = "./test_data_em/"

print("pid:", os.getpid())
context.set_context(mode=context.GRAPH_MODE, device_target="Ascend")


class TimeMonitor(Callback):
    """
    Monitor the time in training.
    """

    def __init__(self, data_size=None):
        super(TimeMonitor, self).__init__()
        self.data_size = data_size
        self.epoch_time = time.time()
        self.per_step_time = 0

    def epoch_begin(self, run_context):
        """
        Record time at the begin of epoch.
        """
        run_context.original_args()
        self.epoch_time = time.time()

    def epoch_end(self, run_context):
        """
        Print process cost time at the end of epoch.
        """
        epoch_seconds = (time.time() - self.epoch_time) * 1000
        step_size = self.data_size
        cb_params = run_context.original_args()
        if hasattr(cb_params, "batch_num"):
            batch_num = cb_params.batch_num
            if isinstance(batch_num, int) and batch_num > 0:
                step_size = cb_params.batch_num

        self.per_step_time = epoch_seconds / step_size
        print("epoch time: {:5.3f} ms, per step time: {:5.3f} ms".format(epoch_seconds, self.per_step_time), flush=True)

    def get_step_time(self,):
        return self.per_step_time


def get_lr(lr_init, steps_per_epoch, total_epochs):
    """get lr"""
    lr_each_step = []
    total_steps = steps_per_epoch * total_epochs
    for i in range(total_steps):
        epoch = i // steps_per_epoch
        lr_local = lr_init
        if epoch <= 15:
            lr_local = lr_init
        elif epoch <= 45:
            lr_local = lr_init * 0.5
        elif epoch <= 300:
            lr_local = lr_init * 0.25
        elif epoch <= 600:
            lr_local = lr_init * 0.125
        lr_each_step.append(lr_local)
    learning_rate = np.array(lr_each_step).astype(np.float32)
    print(learning_rate)
    return learning_rate


def init_weight(net):
    """init weight"""
    for _, cell in net.cells_and_names():
        if isinstance(cell, (nn.Conv3d, nn.Dense)):
            cell.weight.set_data(weight_init.initializer(weight_init.HeNormal(),
                                                         cell.weight.shape,
                                                         cell.weight.dtype))


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_full_em():
    """train"""
    generate_data(train_data_path, test_data_path)
    train_dataset, _ = create_dataset(train_data_path, batch_size=config.batch_size, shuffle=True)
    test_dataset, config_scale = create_dataset(test_data_path, batch_size=config.batch_size,
                                                shuffle=False, drop_remainder=False, is_train=False)
    model_net = Maxwell3D(6)
    init_weight(net=model_net)
    train_step_size = train_dataset.get_dataset_size()
    lr = get_lr(config.lr, train_step_size, config.epochs)
    optimizer = nn.Adam(model_net.trainable_params(), learning_rate=Tensor(lr))
    loss_net = MyMSELoss()
    loss_scale = DynamicLossScaleManager()

    tets_step_size = test_dataset.get_dataset_size()
    test_batch_size = test_dataset.get_batch_size()
    data_length = tets_step_size * test_batch_size // config.t_solution
    evl_error_mrc = EvaLMetric(data_length, config_scale, test_batch_size)
    solver = Solver(model_net,
                    optimizer=optimizer,
                    loss_scale_manager=loss_scale,
                    amp_level="O2",
                    keep_batchnorm_fp32=False,
                    loss_fn=loss_net,
                    metrics={"evl_mrc": evl_error_mrc})

    time_cb = TimeMonitor()
    solver.model.train(5, train_dataset, callbacks=[LossMonitor(), time_cb], dataset_sink_mode=False)
    res = solver.model.eval(test_dataset, dataset_sink_mode=False)
    per_step_time = time_cb.get_step_time()
    l2_s11 = res['evl_mrc']['l2_error']
    print('test_res:', f'l2_error: {l2_s11:.10f} ')
    print(f'per step time: {per_step_time:.10f} ')
    assert l2_s11 <= 0.05
    assert per_step_time <= 150
