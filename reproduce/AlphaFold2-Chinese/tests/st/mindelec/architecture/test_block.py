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
""" test block """
import pytest
import numpy as np

from mindspore import nn, context
from mindspore import Tensor, Parameter

from mindelec.architecture import LinearBlock, ResBlock
from mindelec.architecture import InputScaleNet, FCSequential, MultiScaleFCCell

context.set_context(mode=context.GRAPH_MODE, device_target="Ascend")


class Net(nn.Cell):
    """ Net definition """
    def __init__(self,
                 input_channels,
                 output_channels,
                 weight='normal',
                 bias='zeros',
                 has_bias=True):
        super(Net, self).__init__()
        self.fc = LinearBlock(input_channels, output_channels, weight, bias, has_bias)

    def construct(self, input_x):
        return self.fc(input_x)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_linear():
    """test linear block"""
    weight = Tensor(np.random.randint(0, 255, [8, 64]).astype(np.float32))
    bias = Tensor(np.random.randint(0, 255, [8]).astype(np.float32))
    net = Net(64, 8, weight=weight, bias=bias)
    input_data = Tensor(np.random.randint(0, 255, [128, 64]).astype(np.float32))
    output = net(input_data)
    print(output.asnumpy())


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_linear_nobias():
    """test linear block with no bias"""
    weight = Tensor(np.random.randint(0, 255, [8, 64]).astype(np.float32))
    net = Net(64, 8, weight=weight, has_bias=False)
    input_data = Tensor(np.random.randint(0, 255, [128, 64]).astype(np.float32))
    output = net(input_data)
    print(output.asnumpy())


class Net1(nn.Cell):
    """ Net definition """
    def __init__(self,
                 input_channels,
                 output_channels,
                 weight='normal',
                 bias='zeros',
                 has_bias=True,
                 activation=None):
        super(Net1, self).__init__()
        self.fc = ResBlock(input_channels, output_channels, weight, bias, has_bias, activation)

    def construct(self, input_x):
        return self.fc(input_x)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_res():
    """test res block"""
    weight = Tensor(np.random.randint(0, 255, [8, 8]).astype(np.float32))
    bias = Tensor(np.random.randint(0, 255, [8]).astype(np.float32))
    net = Net1(8, 8, weight=weight, bias=bias)
    input_data = Tensor(np.random.randint(0, 255, [128, 8]).astype(np.float32))
    output = net(input_data)
    print(output.asnumpy())


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_res_nobias():
    """test res block with no bias"""
    weight = Tensor(np.random.randint(0, 255, [8, 8]).astype(np.float32))
    net = Net1(8, 8, weight=weight, has_bias=False)
    input_data = Tensor(np.random.randint(0, 255, [128, 8]).astype(np.float32))
    output = net(input_data)
    print(output.asnumpy())


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_res_activation():
    """test res block with activation"""
    weight = Tensor(np.random.randint(0, 255, [8, 8]).astype(np.float32))
    bias = Tensor(np.random.randint(0, 255, [8]).astype(np.float32))
    net = Net1(8, 8, weight=weight, bias=bias, activation='sin')
    input_data = Tensor(np.random.randint(0, 255, [128, 8]).astype(np.float32))
    output = net(input_data)
    print(output.asnumpy())


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_res_channel_error():
    with pytest.raises(ValueError):
        ResBlock(3, 6)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_input_scale():
    """test input scale cell"""
    inputs = np.random.uniform(size=(16, 3)) + 3.0
    inputs = Tensor(inputs.astype(np.float32))
    input_scale = [1.0, 2.0, 4.0]
    input_center = [3.5, 3.5, 3.5]
    net = InputScaleNet(input_scale, input_center)
    output = net(inputs).asnumpy()

    assert np.all(output[:, 0] <= 0.5) and np.all(output[:, 0] >= -0.5)
    assert np.all(output[:, 1] <= 1.0) and np.all(output[:, 0] >= -1.0)
    assert np.all(output[:, 2] <= 2.0) and np.all(output[:, 0] >= -2.0)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_fc_sequential():
    """test fc sequential cell"""
    inputs = np.ones((16, 3))
    inputs = Tensor(inputs.astype(np.float32))
    net = FCSequential(3, 3, 5, 32, weight_init="ones", bias_init="zeros")
    output = net(inputs).asnumpy()
    target = np.ones((16, 3)) * -31.998459
    assert np.allclose(output, target, rtol=5e-2)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_mulscale_without_latent():
    """test multi-scale net without latent vector"""
    inputs = np.ones((16, 3)) + 3.0
    inputs = Tensor(inputs.astype(np.float32))
    input_scale = [1.0, 2.0, 4.0]
    input_center = [3.5, 3.5, 3.5]
    net = MultiScaleFCCell(3, 3, 5, 32,
                           weight_init="ones", bias_init="zeros",
                           input_scale=input_scale, input_center=input_center)
    output = net(inputs).asnumpy()
    target = np.ones((16, 3)) * -61.669254
    assert np.allclose(output, target, rtol=5e-2)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_mulscale_with_latent():
    """test multi-scale net with latent vector and input scale"""
    inputs = np.ones((64, 3)) + 3.0
    inputs = Tensor(inputs.astype(np.float32))
    num_scenarios = 4
    latent_size = 16
    latent_init = np.ones((num_scenarios, latent_size)).astype(np.float32)
    latent_vector = Parameter(Tensor(latent_init), requires_grad=True)
    input_scale = [1.0, 2.0, 4.0]
    input_center = [3.5, 3.5, 3.5]
    net = MultiScaleFCCell(3, 3, 5, 32,
                           weight_init="ones", bias_init="zeros",
                           input_scale=input_scale, input_center=input_center, latent_vector=latent_vector)
    output = net(inputs).asnumpy()
    target = np.ones((64, 3)) * -57.8849
    assert np.allclose(output, target, rtol=5e-2)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_mulscale_with_latent_noscale():
    """test multi-scale net with latent vector"""
    inputs = np.ones((64, 3))
    inputs = Tensor(inputs.astype(np.float32))
    num_scenarios = 4
    latent_size = 16
    latent_init = np.ones((num_scenarios, latent_size)).astype(np.float32)
    latent_vector = Parameter(Tensor(latent_init), requires_grad=True)
    net = MultiScaleFCCell(3, 3, 5, 32,
                           weight_init="ones", bias_init="zeros", latent_vector=latent_vector)
    output = net(inputs).asnumpy()
    target = np.ones((64, 3)) * -105.62799
    assert np.allclose(output, target, rtol=5e-2)
