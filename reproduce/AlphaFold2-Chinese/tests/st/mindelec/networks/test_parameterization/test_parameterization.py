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
test parameterization
"""

import time

import pytest
import numpy as np
import mindspore.nn as nn
from mindspore.common import set_seed
import mindspore.common.dtype as mstype
from mindspore import context
from mindspore.train.callback import Callback

from easydict import EasyDict as edict
from mindelec.solver import Solver
from mindelec.vision import MonitorTrain, MonitorEval

from src.dataset import create_dataset
from src.maxwell_model import S11Predictor
from src.loss import EvalMetric

set_seed(123456)
np.random.seed(123456)
context.set_context(mode=context.GRAPH_MODE, device_target="Ascend")

opt = edict({
    'epochs': 100,
    'print_interval': 50,
    'batch_size': 8,
    'save_epoch': 10,
    'lr': 0.0001,
    'input_dim': 3,
    'device_num': 1,
    'device_target': "Ascend",
    'checkpoint_dir': './ckpt/',
    'save_graphs_path': './graph_result/',
    'input_path': './dataset/Butterfly_antenna/data_input.npy',
    'label_path': './dataset/Butterfly_antenna/data_label.npy',
})


class TimeMonitor(Callback):
    """
    Monitor the time in training.
    """

    def __init__(self, data_size=None):
        super(TimeMonitor, self).__init__()
        self.data_size = data_size
        self.epoch_time = time.time()
        self.per_step_time = 0
        self.t = 0

    def epoch_begin(self, run_context):
        """
        Record time at the begin of epoch.
        """
        self.t = run_context
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

    def get_step_time(self,):
        return self.per_step_time


def get_lr(data):
    """
    get_lr
    """
    num_milestones = 10
    if data['train_data_length'] % opt.batch_size == 0:
        iter_number = int(data['train_data_length'] / opt.batch_size)
    else:
        iter_number = int(data['train_data_length'] / opt.batch_size) + 1
    iter_number = opt.epochs * iter_number
    milestones = [int(iter_number * i / num_milestones) for i in range(1, num_milestones)]
    milestones.append(iter_number)
    learning_rates = [opt.lr * 0.5 ** i for i in range(0, num_milestones - 1)]
    learning_rates.append(opt.lr * 0.5 ** (num_milestones - 1))
    return milestones, learning_rates


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_parameterization():
    """
    test parameterization
    """
    data, config_data = create_dataset(opt)

    model_net = S11Predictor(opt.input_dim)
    model_net.to_float(mstype.float16)

    milestones, learning_rates = get_lr(data)

    optim = nn.Adam(model_net.trainable_params(),
                    learning_rate=nn.piecewise_constant_lr(milestones, learning_rates))

    eval_error_mrc = EvalMetric(scale_s11=config_data["scale_S11"],
                                length=data["eval_data_length"],
                                frequency=data["frequency"],
                                show_pic_number=4,
                                file_path='./eval_res')

    solver = Solver(network=model_net,
                    mode="Data",
                    optimizer=optim,
                    metrics={'eval_mrc': eval_error_mrc},
                    loss_fn=nn.MSELoss())

    monitor_train = MonitorTrain(per_print_times=1,
                                 summary_dir='./summary_dir_train')

    monitor_eval = MonitorEval(summary_dir='./summary_dir_eval',
                               model=solver,
                               eval_ds=data["eval_loader"],
                               eval_interval=opt.print_interval,
                               draw_flag=True)

    time_monitor = TimeMonitor()
    callbacks_train = [monitor_train, time_monitor, monitor_eval]

    solver.model.train(epoch=opt.epochs,
                       train_dataset=data["train_loader"],
                       callbacks=callbacks_train,
                       dataset_sink_mode=True)

    loss_print, l2_s11_print = monitor_eval.loss_final, monitor_eval.l2_s11_final
    per_step_time = time_monitor.get_step_time()

    print('loss_mse:', loss_print)
    print('l2_s11:', l2_s11_print)
    print('per_step_time:', per_step_time)

    assert l2_s11_print <= 1.0
    assert per_step_time <= 10.0
