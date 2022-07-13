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
"""dataset utilities"""

import os
import numpy as np

from mindelec.data import Dataset, ExistedDataConfig

INPUT_PATH = ""
LABEL_PATH = ""
DATA_CONFIG_PATH = "./data_config.npz"
SAVE_DATA_PATH = "./"

def custom_normalize(dataset, mean=None, std=None):
    """ custom normalization """
    ori_shape = dataset.shape
    dataset = dataset.reshape(ori_shape[0], -1)
    dataset = np.transpose(dataset)
    if mean is None:
        mean = np.mean(dataset, axis=1)
    dataset = dataset - mean[:, None]
    if std is None:
        std = np.std(dataset, axis=1)
        std += (np.abs(std) < 0.0000001)
    dataset = dataset / std[:, None]
    dataset = np.transpose(dataset)
    dataset = dataset.reshape(ori_shape)
    return dataset, mean, std

def generate_data(input_path, label_path):
    """generate dataset for s11 parameter prediction"""

    data_input = np.load(input_path)
    if os.path.exists(DATA_CONFIG_PATH):
        data_config = np.load(DATA_CONFIG_PATH)
        mean = data_config["mean"]
        std = data_config["std"]
    data_input, mean, std = custom_normalize(data_input)
    data_label = np.load(label_path)

    print(data_input.shape)
    print(data_label.shape)

    data_input = data_input.transpose((0, 4, 1, 2, 3))
    data_label[:, :] = np.log10(-data_label[:, :] + 1.0)
    scale_s11 = 0.5 * np.max(np.abs(data_label[:, :]))
    data_label[:, :] = data_label[:, :] / scale_s11

    np.savez(DATA_CONFIG_PATH, scale_s11=scale_s11, mean=mean, std=std)
    np.save(os.path.join(SAVE_DATA_PATH, 'data_input.npy'), data_input)
    np.save(os.path.join(SAVE_DATA_PATH, 'data_label.npy'), data_label)
    print("data saved in target path")


def create_dataset(input_path, label_path, batch_size=8, shuffle=True):
    electromagnetic = ExistedDataConfig(name="electromagnetic",
                                        data_dir=[input_path, label_path],
                                        columns_list=["inputs", "label"],
                                        data_format=input_path.split('.')[-1])
    dataset = Dataset(existed_data_list=[electromagnetic])
    data_loader = dataset.create_dataset(batch_size=batch_size, shuffle=shuffle)

    return data_loader

if __name__ == "__main__":
    generate_data(input_path=INPUT_PATH, label_path=LABEL_PATH)
