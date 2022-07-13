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
"""dataset generation and loading"""

import numpy as np
from mindspore.common import set_seed

from mindelec.data import Dataset, ExistedDataConfig

np.random.seed(0)
set_seed(0)

PATCH_DIM = [25, 50, 25]
NUM_SAMPLE = 10000
INPUT_PATH = ""
DATA_CONFIG_PATH = "./data_config.npy"
SAVE_DATA_PATH = "./"


def generate_data(input_path):
    """generate training data and data configuration"""
    space_temp = np.load(input_path)

    print("data load finish")
    print("random cropping...")
    space_data = np.ones((NUM_SAMPLE,
                          PATCH_DIM[0],
                          PATCH_DIM[1],
                          PATCH_DIM[2],
                          space_temp.shape[-1])).astype(np.float32)
    rand_pos = np.random.randint(low=0, high=(space_temp.shape[0] - PATCH_DIM[0])*\
                                             (space_temp.shape[1] - PATCH_DIM[1])*\
                                             (space_temp.shape[2] - PATCH_DIM[2]), size=NUM_SAMPLE)
    for i, pos in enumerate(rand_pos):
        z = pos % (space_temp.shape[2] - PATCH_DIM[2])
        y = (pos // (space_temp.shape[2] - PATCH_DIM[2])) % (space_temp.shape[1] - PATCH_DIM[1])
        x = (pos // (space_temp.shape[2] - PATCH_DIM[2])) // (space_temp.shape[1] - PATCH_DIM[1])
        space_data[i] = space_temp[x : x+PATCH_DIM[0], y : y+PATCH_DIM[1], z : z+PATCH_DIM[2], :]
    print("random crop finished")

    space_data[:, :, :, :, 2] = np.log10(space_data[:, :, :, :, 2] + 1.0)
    data_config = np.ones(4)
    for i in range(4):
        data_config[i] = np.max(np.abs(space_data[:, :, :, :, i]))
        space_data[:, :, :, :, i] = space_data[:, :, :, :, i] / data_config[i]

    length = space_data.shape[0] // 10
    test_data = space_data[:length]
    train_data = space_data[length:]

    space_data = space_data.transpose((0, 4, 1, 2, 3))

    np.save(DATA_CONFIG_PATH, data_config)
    np.save(SAVE_DATA_PATH+"/train_data.npy", train_data)
    np.save(SAVE_DATA_PATH+"/test_data.npy", test_data)
    print("AE train and test data and data config is saved")


def create_dataset(input_path, label_path, batch_size=8, shuffle=True):
    electromagnetic = ExistedDataConfig(name="electromagnetic",
                                        data_dir=[input_path, label_path],
                                        columns_list=["inputs", "label"],
                                        data_format=input_path.split('.')[-1])
    dataset = Dataset(existed_data_list=[electromagnetic])
    data_loader = dataset.create_dataset(batch_size=batch_size, shuffle=shuffle)

    return data_loader

if __name__ == "__main__":
    generate_data(INPUT_PATH)
