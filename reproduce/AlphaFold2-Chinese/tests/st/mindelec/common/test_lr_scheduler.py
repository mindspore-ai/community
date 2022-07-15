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
from mindspore import context
from mindspore.common.tensor import Tensor
from mindspore.common import dtype as mstype
from mindelec.common import LearningRate, get_poly_lr

context.set_context(mode=context.GRAPH_MODE, device_target="Ascend")


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_learning_rate():
    """test LearningRate"""
    learning_rate = LearningRate(0.1, 0.001, 0, 10, 0.5)
    res = learning_rate(Tensor(10000, mstype.int32))
    assert res == 0.001


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_learning_rate_power_value_error():
    with pytest.raises(ValueError):
        LearningRate(0.1, 0.001, 0, 10, -0.5)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_learning_rate_warmup_steps_type_error():
    """test TypeError cases"""
    with pytest.raises(TypeError):
        LearningRate(0.1, 0.001, 0.1, 10, 0.5)
    with pytest.raises(ValueError):
        LearningRate(0.0, 0.001, 0, 10, 0.5)
    with pytest.raises(ValueError):
        LearningRate(0.1, -0.001, 0, 10, 0.5)
    with pytest.raises(ValueError):
        LearningRate(0.1, 0.001, 0, 0, 0.5)
    with pytest.raises(ValueError):
        LearningRate(0.1, 0.001, -1, 10, 0.5)
    with pytest.raises(ValueError):
        LearningRate(0.1, 0.001, 0, -10, 0.5)
    with pytest.raises(ValueError):
        LearningRate(0.1, 0.001, 1, -10, 0.5)

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_get_poly_lr():
    """test get_poly_lr"""
    res = get_poly_lr(100, 0.001, 0.1, 0.0001, 1000, 10000, 0.5)
    assert res.shape == (9900,)
    with pytest.raises(ValueError):
        get_poly_lr(-1, 0.001, 0.1, 0.0001, 1000, 10000, 0.5)
    with pytest.raises(ValueError):
        get_poly_lr(100, 0.0, 0.1, 0.0001, 1000, 10000, 0.5)
    with pytest.raises(ValueError):
        get_poly_lr(100, 0.001, 0.1, 0.0, 1000, 10000, 0.5)
    with pytest.raises(ValueError):
        get_poly_lr(100, 0.001, 0.1, 0.0001, 1000, 0, 0.5)
    with pytest.raises(ValueError):
        get_poly_lr(100, 0.001, 0.1, 0.0001, 1000, 10000, -0.5)

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_get_poly_lr1():
    """test get_poly_lr"""
    res = get_poly_lr(100, 0.001, 0.1, 0.0001, 0, 10000, 0.5)
    assert res.shape == (9900,)
