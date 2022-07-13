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
"""
create dataset
"""
import numpy as np
from mindelec.data import Dataset
from mindelec.geometry import Disk, Rectangle, TimeDomain, GeometryWithTime
from mindelec.geometry import create_config_from_edict

from .sampling_config import no_src_sampling_config, src_sampling_config, bc_sampling_config

def get_test_data(test_data_path):
    """load label_dataed data for evaluation"""
    # check data
    paths = [test_data_path + '/input.npy', test_data_path + '/output.npy']
    input_data = np.load(paths[0])
    label_data = np.load(paths[1])
    return input_data, label_data

def create_random_dataset(config):
    """create training dataset by online sampling"""
    radius = config["src_radius"]
    origin = config["src_pos"]

    disk = Disk("src", origin, radius)
    rect = Rectangle("rect", config["coord_min"], config["coord_max"])
    diff = rect - disk
    interval = TimeDomain("time", 0.0, config["range_t"])
    no_src = GeometryWithTime(diff, interval)
    no_src.set_name("no_src")
    no_src.set_sampling_config(create_config_from_edict(no_src_sampling_config))
    src = GeometryWithTime(disk, interval)
    src.set_name("src")
    src.set_sampling_config(create_config_from_edict(src_sampling_config))
    bc = GeometryWithTime(rect, interval)
    bc.set_name("bc")
    bc.set_sampling_config(create_config_from_edict(bc_sampling_config))

    geom_dict = {src: ["domain", "IC"],
                 no_src: ["domain", "IC"],
                 bc: ["BC"]}

    dataset = Dataset(geom_dict)
    return dataset
