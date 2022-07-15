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

from mindelec.data import Dataset, ExistedDataConfig
from mindelec.geometry import Disk, Rectangle, TimeDomain, GeometryWithTime
from mindelec.geometry import create_config_from_edict

from .sampling_config import no_src_sampling_config, src_sampling_config, bc_sampling_config

def get_test_data(test_data_path):
    """load labeled data for evaluation"""
    # check data
    paths = [test_data_path + '/input.npy', test_data_path + '/output.npy']
    inputs = np.load(paths[0])
    label = np.load(paths[1])
    return inputs, label

def create_train_dataset(train_data_path):
    """create training dataset from existed data files"""
    src_ic = ExistedDataConfig(name="src_ic",
                               data_dir=[train_data_path + "elec_src_ic.npy"],
                               columns_list=["points"],
                               data_format="npy",
                               constraint_type="IC",
                               random_merge=False)
    boundary = ExistedDataConfig(name="boundary",
                                 data_dir=[train_data_path + "elec_no_src_bc.npy"],
                                 columns_list=["points"],
                                 data_format="npy",
                                 constraint_type="BC",
                                 random_merge=True)
    no_src_ic = ExistedDataConfig(name="no_src_ic",
                                  data_dir=[train_data_path + "elec_no_src_ic.npy"],
                                  columns_list=["points"],
                                  data_format="npy",
                                  constraint_type="IC",
                                  random_merge=True)
    src_domain = ExistedDataConfig(name="src_domain",
                                   data_dir=[train_data_path + "elec_src_domain.npy"],
                                   columns_list=["points"],
                                   data_format="npy",
                                   constraint_type="Equation",
                                   random_merge=True)
    no_src_domain = ExistedDataConfig(name="no_src_domain",
                                      data_dir=[train_data_path + "elec_no_src_domain.npy"],
                                      columns_list=["points"],
                                      data_format="npy",
                                      constraint_type="Equation",
                                      random_merge=True)
    dataset = Dataset(existed_data_list=[no_src_domain, no_src_ic, boundary, src_domain, src_ic])
    return dataset

def create_random_dataset(config):
    """create training dataset by online sampling"""
    disk_radius = config["src_radius"]
    disk_origin = config["src_pos"]
    coord_min = config["coord_min"]
    coord_max = config["coord_max"]

    disk = Disk("src", disk_origin, disk_radius)
    rectangle = Rectangle("rect", coord_min, coord_max)
    diff = rectangle - disk
    time_interval = TimeDomain("time", 0.0, config["range_t"])
    no_src_region = GeometryWithTime(diff, time_interval)
    no_src_region.set_name("no_src")
    no_src_region.set_sampling_config(create_config_from_edict(no_src_sampling_config))
    src_region = GeometryWithTime(disk, time_interval)
    src_region.set_name("src")
    src_region.set_sampling_config(create_config_from_edict(src_sampling_config))
    boundary = GeometryWithTime(rectangle, time_interval)
    boundary.set_name("bc")
    boundary.set_sampling_config(create_config_from_edict(bc_sampling_config))

    geom_dict = {src_region: ["domain", "IC"],
                 no_src_region: ["domain", "IC"],
                 boundary: ["BC"]}

    dataset = Dataset(geom_dict)
    return dataset
