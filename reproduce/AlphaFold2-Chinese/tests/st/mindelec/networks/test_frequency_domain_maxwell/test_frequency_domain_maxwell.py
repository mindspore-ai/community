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
import pytest
import numpy as np

import mindspore.nn as nn
import mindspore.ops as ops
from mindspore import context, ms_function
from mindspore.common import set_seed
from mindspore.train.callback import LossMonitor
from mindspore.train.loss_scale_manager import DynamicLossScaleManager

from mindelec.solver import Solver, Problem
from mindelec.geometry import Rectangle, create_config_from_edict
from mindelec.common import L2
from mindelec.data import Dataset
from mindelec.operators import SecondOrderGrad as Hessian
from mindelec.loss import Constraints

from src.config import rectangle_sampling_config, helmholtz_2d_config
from src.model import FFNN
from src.dataset import test_data_prepare
from src.callback import PredictCallback, TimeMonitor

set_seed(0)
np.random.seed(0)

print("pid:", os.getpid())
context.set_context(mode=context.GRAPH_MODE, save_graphs=False, device_target="Ascend")


# define problem
class Helmholtz2D(Problem):
    """2D Helmholtz equation"""
    def __init__(self, domain_name, bc_name, net, wavenumber=2):
        super(Helmholtz2D, self).__init__()
        self.domain_name = domain_name
        self.bc_name = bc_name
        self.type = "Equation"
        self.wave_number = wavenumber
        self.grad_xx = Hessian(net, input_idx1=0, input_idx2=0, output_idx=0)
        self.grad_yy = Hessian(net, input_idx1=1, input_idx2=1, output_idx=0)
        self.reshape = ops.Reshape()

    @ms_function
    def governing_equation(self, *output, **kwargs):
        """governing equation"""
        u = output[0]
        x = kwargs[self.domain_name][:, 0]
        y = kwargs[self.domain_name][:, 1]
        x = self.reshape(x, (-1, 1))
        y = self.reshape(y, (-1, 1))

        u_xx = self.grad_xx(kwargs[self.domain_name])
        u_yy = self.grad_yy(kwargs[self.domain_name])

        return u_xx + u_yy + self.wave_number**2 * u

    @ms_function
    def boundary_condition(self, *output, **kwargs):
        """boundary condition"""
        u = output[0]
        x = kwargs[self.bc_name][:, 0]
        y = kwargs[self.bc_name][:, 1]
        x = self.reshape(x, (-1, 1))
        y = self.reshape(y, (-1, 1))

        test_label = ops.sin(self.wave_number * x)
        return 100 * (u - test_label)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_frequency_domain_maxwell():
    """train process"""
    net = FFNN(input_dim=2, output_dim=1, hidden_layer=64)

    # define geometry
    geom_name = "rectangle"
    rect_space = Rectangle(geom_name,
                           coord_min=helmholtz_2d_config["coord_min"],
                           coord_max=helmholtz_2d_config["coord_max"],
                           sampling_config=create_config_from_edict(rectangle_sampling_config))
    geom_dict = {rect_space: ["domain", "BC"]}

    # create dataset for train and test
    train_dataset = Dataset(geom_dict)
    train_data = train_dataset.create_dataset(batch_size=helmholtz_2d_config.get("batch_size", 128),
                                              shuffle=True, drop_remainder=False)
    test_input, test_label = test_data_prepare(helmholtz_2d_config)

    # define problem and constraints
    train_prob_dict = {geom_name: Helmholtz2D(domain_name=geom_name + "_domain_points",
                                              bc_name=geom_name + "_BC_points",
                                              net=net,
                                              wavenumber=helmholtz_2d_config.get("wavenumber", 2)),
                      }
    train_constraints = Constraints(train_dataset, train_prob_dict)

    # optimizer
    optim = nn.Adam(net.trainable_params(), learning_rate=helmholtz_2d_config.get("lr", 1e-4))

    # solver
    solver = Solver(net,
                    optimizer=optim,
                    mode="PINNs",
                    train_constraints=train_constraints,
                    test_constraints=None,
                    amp_level="O2",
                    metrics={'l2': L2(), 'distance': nn.MAE()},
                    loss_scale_manager=DynamicLossScaleManager()
                    )

    # train
    time_cb = TimeMonitor()
    loss_cb = PredictCallback(model=net, predict_interval=10, input_data=test_input, label=test_label)
    solver.train(epoch=helmholtz_2d_config.get("epochs", 10),
                 train_dataset=train_data,
                 callbacks=[time_cb, LossMonitor(), loss_cb])
    per_step_time = time_cb.get_step_time()
    l2_error = loss_cb.get_l2_error()

    print(f'l2 error: {l2_error:.10f}')
    print(f'per step time: {per_step_time:.10f}')
    assert l2_error <= 0.05
    assert per_step_time <= 10.0
