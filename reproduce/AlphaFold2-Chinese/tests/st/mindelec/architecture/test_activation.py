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
""" test Activations """
import pytest
import numpy as np

from mindspore import nn
from mindspore import Tensor
from mindspore import context
from mindelec.architecture import get_activation

context.set_context(mode=context.GRAPH_MODE, device_target="Ascend")


class Net(nn.Cell):
    def __init__(self):
        super(Net, self).__init__()
        self.srelu = get_activation("srelu")

    def construct(self, x):
        return self.srelu(x)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_srelu():
    """test srelu activation"""
    net = Net()
    input_tensor = Tensor(np.array([[1.2, 0.1], [0.2, 3.2]], dtype=np.float32))
    output = net(input_tensor)
    print(input_tensor.asnumpy())
    print(output.asnumpy())


class Net1(nn.Cell):
    """net"""
    def __init__(self):
        super(Net1, self).__init__()
        self.sin = get_activation("sin")

    def construct(self, x):
        return self.sin(x)

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_sin():
    """test sin activation"""
    net = Net1()
    input_tensor = Tensor(np.array([[1.2, 0.1], [0.2, 3.2]], dtype=np.float32))
    output = net(input_tensor)
    print(input_tensor.asnumpy())
    print(output.asnumpy())

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_activation_type_error():
    with pytest.raises(TypeError):
        get_activation(1)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_get_activation():
    activation = get_activation("softshrink")
    assert isinstance(activation, nn.Cell)
