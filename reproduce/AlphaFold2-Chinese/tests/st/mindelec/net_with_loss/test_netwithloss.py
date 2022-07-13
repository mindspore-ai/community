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
test net_with_loss
"""
import os
from easydict import EasyDict as edict
import numpy as np
import pytest

import mindspore.nn as nn
import mindspore.ops as ops
from mindspore import Tensor
from mindspore import context, ms_function
from mindspore.common import set_seed
from mindelec.geometry import Rectangle, create_config_from_edict
from mindelec.data import Dataset, ExistedDataConfig
from mindelec.loss import Constraints, NetWithLoss, NetWithEval
from mindelec.architecture import ResBlock, LinearBlock
from mindelec.solver import Problem
from mindelec.common import L2
from mindelec.operators import Grad

set_seed(1)
np.random.seed(1)
context.set_context(mode=context.GRAPH_MODE, device_target="Ascend")

path = os.getcwd()
data_config = edict({
    'data_dir': [path+'/inputs.npy', path+'/label.npy'],  # absolute dir
    'columns_list': ['input_data', 'label'],
    'data_format': 'npy',
    'constraint_type': 'Equation',
    'name': 'exist'
})

if not os.path.exists(data_config['data_dir'][0]):
    data_in = np.ones((32, 2), dtype=np.float32)
    np.save(path+"/inputs.npy", data_in)

if not os.path.exists(data_config['data_dir'][1]):
    data_label = np.ones((32, 1), dtype=np.float32)
    np.save(path+"/label.npy", data_label)


rectangle_config = edict({
    'domain': edict({
        'random_sampling': True,
        'size': 2500,
        'sampler': 'uniform'
    }),
    'BC': edict({
        'random_sampling': True,
        'size': 200,
        'sampler': 'uniform'
    })
})

rectangle_config1 = edict({
    'domain': edict({
        'random_sampling': True,
        'size': 2500,
        'sampler': 'uniform'
    }),
})


class Net(nn.Cell):
    """net definition"""
    def __init__(self, input_dim, output_dim, hidden_layer=128, activation="sin"):
        super(Net, self).__init__()
        self.resblock = ResBlock(hidden_layer, hidden_layer, activation=activation)
        self.fc1 = LinearBlock(input_dim, hidden_layer)
        self.fc2 = LinearBlock(hidden_layer, output_dim)

    def construct(self, *inputs):
        x = inputs[0]
        out = self.fc1(x)
        out = self.resblock(out)
        out = self.fc2(out)
        return out


class RectPde(Problem):
    """rectangle pde problem"""
    def __init__(self, domain_name=None, bc_name=None, label_name=None, net=None):
        super(RectPde, self).__init__()
        self.domain_name = domain_name
        self.bc_name = bc_name
        self.label_name = label_name
        self.type = "Equation"
        self.jacobian = Grad(net)

    @ms_function
    def governing_equation(self, *output, **kwargs):
        u = output[0]
        data = kwargs[self.domain_name]
        u_x = self.jacobian(data, 0, 0, u)
        return u_x

    @ms_function
    def boundary_condition(self, *output, **kwargs):
        u = output[0]
        x = kwargs[self.bc_name][:, 0]
        y = kwargs[self.bc_name][:, 1]
        return u - ops.sin(x) * ops.cos(y)

    @ms_function
    def constraint_function(self, *output, **kwargs):
        u = output[0]
        label = kwargs[self.label_name]
        return u - label


class RectPde1(Problem):
    """rectangle pde problem with no boundary condition"""
    def __init__(self, domain_name, net):
        super(RectPde1, self).__init__()
        self.domain_name = domain_name
        self.type = "Equation"
        self.jacobian = Grad(net)

    @ms_function
    def governing_equation(self, *output, **kwargs):
        u = output[0]
        data = kwargs[self.domain_name]
        u_x = self.jacobian(data, 0, 0, u)
        return u_x


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_netwithloss():
    """test netwithloss function"""
    model = Net(2, 1, 128, "sin")
    rect_space = Rectangle("rectangle", coord_min=[-1.0, -1.0], coord_max=[1.0, 1.0],
                           sampling_config=create_config_from_edict(rectangle_config))

    geom_dict = {rect_space: ["domain", "BC"]}
    dataset = Dataset(geom_dict)
    dataset.create_dataset(batch_size=4, shuffle=True)
    prob_dict = {rect_space.name: RectPde(domain_name="rectangle_domain_points", bc_name="rectangle_BC_points",
                                          net=model)}
    train_constraints = Constraints(dataset, prob_dict)
    metrics = {'l2': L2(), 'distance': nn.MAE()}
    train_input_map = {'rectangle_domain': ['rectangle_domain_points'], 'rectangle_BC': ['rectangle_BC_points']}
    loss_network = NetWithLoss(model, train_constraints, metrics, train_input_map)

    domain_points = Tensor(np.ones([32, 2]).astype(np.float32))
    bc_points = Tensor(np.ones([32, 2]).astype(np.float32))
    bc_normal = Tensor(np.ones([32, 2]).astype(np.float32))
    out = loss_network(domain_points, bc_points, bc_normal)
    print(out)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_netwithloss1():
    """test netwithloss function1"""
    model = Net(2, 1, 128, "sin")
    rect_space = Rectangle("rectangle", coord_min=[-1.0, -1.0], coord_max=[1.0, 1.0],
                           sampling_config=create_config_from_edict(rectangle_config1))
    geom_dict = {rect_space: ["domain"]}
    dataset = Dataset(geom_dict)
    dataset.create_dataset(batch_size=4, shuffle=True)
    prob_dict = {rect_space.name: RectPde1(domain_name="rectangle_domain_points", net=model)}
    train_constraints = Constraints(dataset, prob_dict)
    metrics = {'l2': L2(), 'distance': nn.MAE()}
    train_input_map = {'rectangle_domain': ['rectangle_domain_points']}
    loss_network = NetWithLoss(model, train_constraints, metrics, train_input_map)

    domain_points = Tensor(np.ones([32, 2]).astype(np.float32))
    out = loss_network(domain_points)
    print(out)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_netwitheval():
    """test netwitheval function"""
    model = Net(2, 1, 128, "sin")
    src_domain = ExistedDataConfig(name="src_domain",
                                   data_dir=[path+"/inputs.npy", path+"/label.npy"],
                                   columns_list=["inputs", "label"],
                                   data_format="npy",
                                   constraint_type="Label",
                                   random_merge=False)
    test_prob_dict = {src_domain.name: RectPde(domain_name=src_domain.name+"_inputs",
                                               label_name=src_domain.name+"_label", net=model)}
    test_dataset = Dataset(existed_data_list=[src_domain])
    test_dataset.create_dataset(batch_size=4, shuffle=False)
    test_constraints = Constraints(test_dataset, test_prob_dict)
    metrics = {'l2': L2(), 'distance': nn.MAE()}
    loss_network = NetWithEval(model, test_constraints, metrics)

    data = Tensor(np.ones([32, 2]).astype(np.float32))
    label = Tensor(np.ones([32, 1]).astype(np.float32))
    out = loss_network(data, label)
    print(out)
