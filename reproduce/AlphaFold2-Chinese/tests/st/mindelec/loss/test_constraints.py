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
"""Test constraints"""
import pytest
from mindelec.data import Dataset
from mindelec.loss import Constraints
from mindelec.geometry import Rectangle


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_constraints_dataset_type_error():
    with pytest.raises(TypeError):
        Constraints(1, 1)

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_existed_data_config_type_error():
    rectangle = Rectangle("rect", (-1, -1), (1, 1))
    geom_dict = {rectangle: ["domain"]}
    dataset = Dataset(geom_dict)
    with pytest.raises(TypeError):
        Constraints(dataset, 1)
