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
#pylint: disable=W0622
"""
test parameterization
"""

import pytest
import numpy as np
import mindspore.nn as nn
from mindspore.common import set_seed
import mindspore.common.dtype as mstype
from mindspore import context, Tensor

from mindelec.solver import Solver, Problem, LossAndTimeMonitor
from mindelec.data import ExistedDataConfig, Dataset
from mindelec.loss import Constraints
from mindelec.common import L2

set_seed(0)
np.random.seed(0)

context.set_context(mode=context.GRAPH_MODE, device_target="Ascend")


class NetWithoutLoss(nn.Cell):
    """define network"""
    def __init__(self, input_dim, output_dim):
        super(NetWithoutLoss, self).__init__()
        self.fc1 = nn.Dense(input_dim, 64)
        self.fc2 = nn.Dense(64, output_dim)

    def construct(self, *input):
        x = input[0]
        out = self.fc1(x)
        out = self.fc2(out)
        return out


class RectPde(Problem):
    def __init__(self, domain_name):
        self.domain_name = domain_name

    def governing_equation(self, *output, **kwargs):
        u = output[0]
        x = kwargs[self.domain_name]
        return u - x


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_solver():
    """
    test solver
    """
    input_path = "./input.npy"
    label_path = "./label.npy"
    input = np.random.randn(1000, 3)
    output = np.random.randn(1000, 3)
    np.save(input_path, input)
    np.save(label_path, output)

    exist_train = ExistedDataConfig(name="existed_data",
                                    data_dir=[input_path, label_path],
                                    columns_list=["inputs", "label"],
                                    constraint_type="Equation",
                                    data_format="npy")

    dataset = Dataset(existed_data_list=[exist_train])
    train_dataset = dataset.create_dataset(batch_size=500, shuffle=True)
    steps_per_epoch = len(dataset)
    prob_dict = {exist_train.name: RectPde(domain_name="existed_data_inputs")}
    train_constraints = Constraints(dataset, prob_dict)

    model = NetWithoutLoss(3, 3)
    optim = nn.Adam(model.trainable_params(), learning_rate=1e-4)

    solver = Solver(network=model,
                    mode="PINNs",
                    optimizer=optim,
                    train_constraints=train_constraints,
                    train_input_map={"existed_data": ["existed_data_inputs"]},
                    metrics={'l2': L2(), 'distance': nn.MAE()})

    loss_time_callback = LossAndTimeMonitor(steps_per_epoch)
    solver.train(5, train_dataset, callbacks=[loss_time_callback])

    pred_input = Tensor(np.random.randn(20, 3), mstype.float32)
    pred_output = solver.predict(pred_input)
    assert pred_output.shape == (20, 3)
