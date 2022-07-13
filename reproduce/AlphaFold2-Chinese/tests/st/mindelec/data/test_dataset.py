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
"""test dataset module"""
import pytest
from easydict import EasyDict as edict
from mindelec.data import Dataset
from mindelec.geometry import create_config_from_edict
from mindelec.geometry import Disk, Rectangle, TimeDomain, GeometryWithTime
from mindelec.data import BoundaryBC, BoundaryIC
from config import ds_config, src_sampling_config, no_src_sampling_config, bc_sampling_config

ic_bc_config = edict({
    'domain': edict({
        'random_sampling': False,
        'size': [10, 20],
    }),
    'BC': edict({
        'random_sampling': True,
        'size': 10,
        'with_normal': True,
    }),
    'IC': edict({
        'random_sampling': True,
        'size': 10,
    }),
    'time': edict({
        'random_sampling': False,
        'size': 10,
    })
})

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_dataset_allnone():
    with pytest.raises(ValueError):
        Dataset()

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_dataset():
    """test dataset"""
    disk = Disk("src", (0.0, 0.0), 0.2)
    rectangle = Rectangle("rect", (-1, -1), (1, 1))
    diff = rectangle - disk
    time = TimeDomain("time", 0.0, 1.0)

    # check datalist
    rect_with_time = GeometryWithTime(rectangle, time)
    rect_with_time.set_sampling_config(create_config_from_edict(ic_bc_config))
    bc = BoundaryBC(rect_with_time)
    ic = BoundaryIC(rect_with_time)
    dataset = Dataset(dataset_list=bc)

    dataset.set_constraint_type("Equation")

    c_type1 = {bc: "Equation", ic: "Equation"}
    with pytest.raises(ValueError):
        dataset.set_constraint_type(c_type1)

    no_src_region = GeometryWithTime(diff, time)
    no_src_region.set_name("no_src")
    no_src_region.set_sampling_config(create_config_from_edict(no_src_sampling_config))
    src_region = GeometryWithTime(disk, time)
    src_region.set_name("src")
    src_region.set_sampling_config(create_config_from_edict(src_sampling_config))
    boundary = GeometryWithTime(rectangle, time)
    boundary.set_name("bc")
    boundary.set_sampling_config(create_config_from_edict(bc_sampling_config))

    geom_dict = ['1', '2']
    with pytest.raises(TypeError):
        Dataset(geom_dict)

    geom_dict = {src_region: ["test"]}
    with pytest.raises(KeyError):
        Dataset(geom_dict)

    geom_dict = {src_region: ["domain", "IC"],
                 no_src_region: ["domain", "IC"],
                 boundary: ["BC"]}
    dataset = Dataset(geom_dict)

    with pytest.raises(ValueError):
        print(dataset[0])

    with pytest.raises(ValueError):
        len(dataset)

    with pytest.raises(ValueError):
        dataset.get_columns_list()

    with pytest.raises(ValueError):
        dataset.create_dataset(batch_size=ds_config.train.batch_size,
                               shuffle=ds_config.train.shuffle,
                               prebatched_data=True,
                               drop_remainder=False)
