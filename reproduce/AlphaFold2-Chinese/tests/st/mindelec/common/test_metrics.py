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
""" test metrics """
import pytest
import numpy as np

import mindspore
from mindspore import Tensor
from mindspore import context
from mindelec.common import L2

context.set_context(mode=context.GRAPH_MODE, device_target="Ascend")


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_l2():
    """test l2"""
    x = Tensor(np.array([0.1, 0.2, 0.6, 0.9]), mindspore.float32)
    y = Tensor(np.array([0.1, 0.25, 0.7, 0.9]), mindspore.float32)
    metric = L2()
    metric.clear()
    metric.update(x, y)
    result = metric.eval()
    assert result == 0.09543302997807275
