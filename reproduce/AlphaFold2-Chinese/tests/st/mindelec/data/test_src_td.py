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
"""test dataset module, call CSG ant GeometryWithTime"""
import pytest
import numpy as np
from easydict import EasyDict as edict

from mindelec.data import Dataset
from mindelec.geometry import Rectangle, TimeDomain, GeometryWithTime, create_config_from_edict


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_dataset():
    """check dataset"""
    sampling_config = edict({
        'domain': edict({
            'random_sampling': False,
            'size': [10, 10],
        }),
        'BC': edict({
            'random_sampling': False,
            'size': 100,
            'with_normal': True,
        }),
        'IC': edict({
            'random_sampling': False,
            'size': [10, 10],
        }),
        'time': edict({
            'random_sampling': False,
            'size': 40,
        }),
    })

    rect_space = Rectangle("rectangle", coord_min=[0, 0], coord_max=[10, 10])
    time = TimeDomain("time", 0.0, 20)
    grid = GeometryWithTime(rect_space, time)
    grid.set_sampling_config(create_config_from_edict(sampling_config))
    grid.set_name("grid")
    geom_dict = {grid: ["domain", "BC", "IC"]}
    dataset = Dataset(geom_dict)

    def preprocess_fn(*data):
        bc_data = data[1]
        bc_normal = np.ones(bc_data.shape)
        return data[0], data[1], bc_normal, data[2], data[3]

    colunms_map = {"grid_domain_points": ["grid_domain_points"],
                   "grid_BC_points": ["grid_BC_points", "grid_BC_tangent"],
                   "grid_BC_normal": "grid_BC_normal",
                   "grid_IC_points": "grid_IC_points"}
    train_data = dataset.create_dataset(batch_size=8192, shuffle=False, drop_remainder=False,
                                        preprocess_fn=preprocess_fn,
                                        input_output_columns_map=colunms_map)
    dataset.set_constraint_type({dataset.all_datasets[0]: "Equation",
                                 dataset.all_datasets[1]: "BC",
                                 dataset.all_datasets[2]: "IC"})
    print("get merged data: {}".format(dataset[5]))
    for sub_data in dataset.all_datasets:
        print("get data: {}".format(sub_data[5]))

    dataset_iter = train_data.create_dict_iterator(num_epochs=1)
    np.set_printoptions(threshold=np.inf)
    for _ in range(1):
        for data in dataset_iter:
            for k, v in data.items():
                print("key: ", k)
                print(v)
            break
