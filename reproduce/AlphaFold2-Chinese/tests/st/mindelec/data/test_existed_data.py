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
"""Test existed_data."""
import pytest
import numpy as np
from mindelec.data import ExistedDataset, ExistedDataConfig


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_existed_data_value_error():
    with pytest.raises(ValueError):
        ExistedDataset()

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_existed_data_cnfig_type_error():
    with pytest.raises(TypeError):
        ExistedDataset(data_config=1)

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_existed_config():
    """test various errors"""
    with pytest.raises(ValueError):
        input_path = "./input_data.npy"
        label_path = "./label.npy"
        input_data = np.random.randn(10, 3)
        output = np.random.randn(10, 3)
        np.save(input_path, input_data)
        np.save(label_path, output)

        config = ExistedDataConfig(name="existed_data",
                                   data_dir=[input_path, label_path],
                                   columns_list=["inputs", "label"],
                                   constraint_type="Equation",
                                   data_format="npz")
        dataset = ExistedDataset(data_config=config)

    input_path = "./input_data.npy"
    input_data = np.random.randn(10, 3)
    np.save(input_path, input_data)

    dataset = ExistedDataset(name="existed_data",
                             data_dir=[input_path],
                             columns_list=["inputs"],
                             constraint_type="Equation",
                             data_format="npy")
    for i in range(20):
        print(dataset[i])

    dataset = ExistedDataset(name="existed_data",
                             data_dir=[input_path],
                             columns_list=["inputs"],
                             constraint_type="Equation",
                             data_format="npy",
                             random_merge=False)
    for i in range(20):
        print(dataset[i])
