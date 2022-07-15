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
"""s parameter prediction model training test"""
import time
import pytest
import numpy as np

import mindspore.nn as nn
from mindspore import context
from mindspore.common import set_seed
import mindspore.common.initializer as weight_init
from mindspore.train.callback import LossMonitor, Callback

from mindelec.solver import Solver

from src.dataset import create_dataset
from src.model import S11Predictor
from src.lr_generator import step_lr_generator
from src.config import config
from src.metric import MyMSELoss, EvalMetric

set_seed(0)
np.random.seed(0)

context.set_context(mode=context.GRAPH_MODE,
                    save_graphs=False,
                    device_target="Ascend")


class TimeMonitor(Callback):
    """
    Monitor the time in training.
    """

    def __init__(self, data_size=None):
        super(TimeMonitor, self).__init__()
        self.data_size = data_size
        self.epoch_time = time.time()
        self.per_step_time = 0
        self._tmp = None

    def epoch_begin(self, run_context):
        """
        Record time at the begin of epoch.
        """
        self.epoch_time = time.time()
        self._tmp = run_context

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

def init_weight(net):
    """init_weight"""
    for _, cell in net.cells_and_names():
        if isinstance(cell, (nn.Conv3d, nn.Dense)):
            cell.weight.set_data(weight_init.initializer(weight_init.HeNormal(),
                                                         cell.weight.shape,
                                                         cell.weight.dtype))

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_s_predictor_train():
    """training"""
    train_input_path = "input.npy"
    train_label_path = "label.npy"
    train_input = np.ones((100, 496, 20, 40, 3), np.float32)
    train_label = np.ones((100, 1001), np.float32)
    np.save(train_input_path, train_input)
    np.save(train_label_path, train_label)

    model_net = S11Predictor(input_dim=config["input_channels"])
    init_weight(net=model_net)

    train_dataset = create_dataset(input_path=train_input_path,
                                   label_path=train_label_path,
                                   batch_size=config["batch_size"],
                                   shuffle=True)

    step_size = train_dataset.get_dataset_size()
    milestones, learning_rates = step_lr_generator(step_size,
                                                   config["epochs"],
                                                   config["lr"],
                                                   config["lr_decay_milestones"])
    optimizer = nn.Adam(model_net.trainable_params(),
                        learning_rate=nn.piecewise_constant_lr(milestones, learning_rates))

    loss_net = MyMSELoss()

    eval_step_size = train_dataset.get_dataset_size() * config["batch_size"]
    evl_error_mrc = EvalMetric(scale_s11=1,
                               length=eval_step_size,
                               frequency=np.linspace(0, 4*10**8, 1001),
                               show_pic_number=4,
                               file_path='./eval_result')

    solver = Solver(model_net,
                    train_input_map={'train': ['train_input_data']},
                    test_input_map={'test': ['test_input_data']},
                    optimizer=optimizer,
                    metrics={'evl_mrc': evl_error_mrc,},
                    amp_level="O2",
                    loss_fn=loss_net)

    time_cb = TimeMonitor()
    solver.model.train(config["epochs"],
                       train_dataset,
                       callbacks=[LossMonitor(), time_cb],
                       dataset_sink_mode=False)
    res = solver.model.eval(train_dataset, dataset_sink_mode=False)
    per_step_time = time_cb.get_step_time()
    l1_error = res['evl_mrc']['l2_error']
    print('test_res:', f'l1_error: {l1_error:.10f} ')
    print(f'per step time: {per_step_time:.10f} ')
    assert l1_error <= 0.01
    assert per_step_time <= 100
