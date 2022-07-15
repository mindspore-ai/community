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

from mindspore import context
from mindspore import Tensor
from mindelec.architecture import MTLWeightedLossCell

context.set_context(mode=context.GRAPH_MODE, device_target="Ascend")


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_linear():
    net = MTLWeightedLossCell(num_losses=2)
    input_data = Tensor(np.array([1.0, 1.0]).astype(np.float32))
    output = net(input_data)
    print(output.asnumpy())


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_mlt_num_losses_error():
    with pytest.raises(TypeError):
        MTLWeightedLossCell('a')
