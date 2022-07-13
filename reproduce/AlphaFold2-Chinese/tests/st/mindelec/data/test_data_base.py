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
"""Test data_base."""
import pytest
import numpy as np
from mindelec.data import ExistedDataConfig
from mindelec.data.data_base import Data


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_existed_data_config_name_error():
    with pytest.raises(TypeError):
        ExistedDataConfig(1, "/home/a.npy", "data")


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_existed_data_config_data_dir_error():
    with pytest.raises(TypeError):
        ExistedDataConfig("a", 1, "data")


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_existed_data_config_column_list_error():
    with pytest.raises(TypeError):
        input_path = "./input_data.npy"
        input_data = np.random.randn(10, 3)
        np.save(input_path, input_data)
        ExistedDataConfig("a", input_path, 1)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_existed_data_config_constraint_type_error():
    with pytest.raises(TypeError):
        input_path = "./input_data.npy"
        input_data = np.random.randn(10, 3)
        np.save(input_path, input_data)
        ExistedDataConfig("a", input_path, "data", contraint_type="a")


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_existed_data_config_data_format_typeerror():
    with pytest.raises(TypeError):
        input_path = "./input_data.npy"
        input_data = np.random.randn(10, 3)
        np.save(input_path, input_data)
        ExistedDataConfig("a", input_path, "data", 1)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_existed_data_config_data_format_valueerror():
    with pytest.raises(ValueError):
        input_path = "./input_data.npy"
        input_data = np.random.randn(10, 3)
        np.save(input_path, input_data)
        ExistedDataConfig("a", input_path, "data", "csv")


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_existed_data_config_data_constraint_type_valueerror():
    with pytest.raises(TypeError):
        input_path = "./input_data.npy"
        input_data = np.random.randn(10, 3)
        np.save(input_path, input_data)
        ExistedDataConfig("a", input_path, "data", constraint_type='1')

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_existed_data_config_data_constraint_type_valueerror1():
    with pytest.raises(TypeError):
        input_path = "./input_data.npy"
        input_data = np.random.randn(10, 3)
        np.save(input_path, input_data)
        ExistedDataConfig("a", input_path, "data", constraint_type='test')

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_existed_data_config_random_merge_error():
    with pytest.raises(TypeError):
        input_path = "./input_data.npy"
        input_data = np.random.randn(10, 3)
        np.save(input_path, input_data)
        ExistedDataConfig("a", input_path, "data", random_merge=1)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_data_name_type_error():
    with pytest.raises(TypeError):
        Data(1)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_data_columns_list_type_error():
    with pytest.raises(TypeError):
        Data(columns_list=1)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_data_constraint_type_type_error():
    with pytest.raises(TypeError):
        Data(constraint_type=1)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_data_constraint_type_type_error1():
    with pytest.raises(TypeError):
        Data(constraint_type="labe")


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_data_set_constraint_type_type_error():
    with pytest.raises(TypeError):
        data = Data()
        data.set_constraint_type("test")


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_data_create_dataset_nie_error():
    with pytest.raises(NotImplementedError):
        data = Data()
        data.create_dataset()


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_data_get_item_nie_error():
    with pytest.raises(NotImplementedError):
        data = Data()
        print(data[0])


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_data_len_nie_error():
    with pytest.raises(NotImplementedError):
        data = Data()
        len(data)
