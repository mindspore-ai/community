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
# ==============================================================================
"""
dataset
"""
import os
import shutil
import numpy as np
from mindelec.data import Dataset, ExistedDataConfig


def custom_normalize(data):
    """
    get normalize data
    """
    print("Custom normalization is called")
    ori_shape = data.shape
    data = data.reshape(ori_shape[0], -1)
    data = np.transpose(data)
    mean = np.mean(data, axis=1)
    data = data - mean[:, None]
    std = np.std(data, axis=1)
    std += (np.abs(std) < 0.0000001)
    data = data / std[:, None]
    data = np.transpose(data)
    data = data.reshape(ori_shape)
    return data


def create_dataset(opt):
    """
    load data
    """
    data_input_path = opt.input_path
    data_label_path = opt.label_path

    data_input = np.load(data_input_path)
    data_label = np.load(data_label_path)

    frequency = data_label[0, :, 0]
    data_label = data_label[:, :, 1]

    print(data_input.shape)
    print(data_label.shape)
    print("data load finish")

    data_input = custom_normalize(data_input)

    config_data_prepare = {}

    config_data_prepare["scale_input"] = 0.5 * np.max(np.abs(data_input), axis=0)
    config_data_prepare["scale_S11"] = 0.5 * np.max(np.abs(data_label))

    data_input[:, :] = data_input[:, :] / config_data_prepare["scale_input"]
    data_label[:, :] = data_label[:, :] / config_data_prepare["scale_S11"]

    permutation = np.random.permutation(data_input.shape[0])
    data_input = data_input[permutation]
    data_label = data_label[permutation]

    length = data_input.shape[0] // 10
    train_input, train_label = data_input[length:], data_label[length:]
    eval_input, eval_label = data_input[:length], data_label[:length]

    print(np.shape(train_input))
    print(np.shape(train_label))
    print(np.shape(eval_input))
    print(np.shape(eval_label))

    if not os.path.exists('./data_prepare'):
        os.mkdir('./data_prepare')
    else:
        shutil.rmtree('./data_prepare')
        os.mkdir('./data_prepare')

    train_input = train_input.astype(np.float32)
    np.save('./data_prepare/train_input', train_input)
    train_label = train_label.astype(np.float32)
    np.save('./data_prepare/train_label', train_label)
    eval_input = eval_input.astype(np.float32)
    np.save('./data_prepare/eval_input', eval_input)
    eval_label = eval_label.astype(np.float32)
    np.save('./data_prepare/eval_label', eval_label)

    electromagnetic_train = ExistedDataConfig(name="electromagnetic_train",
                                              data_dir=['./data_prepare/train_input.npy',
                                                        './data_prepare/train_label.npy'],
                                              columns_list=["inputs", "label"],
                                              data_format="npy")
    electromagnetic_eval = ExistedDataConfig(name="electromagnetic_eval",
                                             data_dir=['./data_prepare/eval_input.npy',
                                                       './data_prepare/eval_label.npy'],
                                             columns_list=["inputs", "label"],
                                             data_format="npy")
    train_batch_size = opt.batch_size
    eval_batch_size = len(eval_input)

    train_dataset = Dataset(existed_data_list=[electromagnetic_train])
    train_loader = train_dataset.create_dataset(batch_size=train_batch_size, shuffle=True)

    eval_dataset = Dataset(existed_data_list=[electromagnetic_eval])
    eval_loader = eval_dataset.create_dataset(batch_size=eval_batch_size, shuffle=False)

    data = {
        "train_loader": train_loader,
        "eval_loader": eval_loader,

        "train_data": train_input,
        "train_label": train_label,
        "eval_data": eval_input,
        "eval_label": eval_label,

        "train_data_length": len(train_label),
        "eval_data_length": len(eval_label),
        "frequency": frequency,
    }

    return data, config_data_prepare
