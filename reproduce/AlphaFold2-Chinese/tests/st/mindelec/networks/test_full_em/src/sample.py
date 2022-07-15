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
sample fake data for train and test
"""
import os
import numpy as np


def generate_data(train_path, test_path):
    """generate fake data"""
    if not os.path.exists(train_path):
        os.makedirs(train_path)
    if not os.path.exists(test_path):
        os.makedirs(test_path)

    inputs = np.ones((162, 50, 50, 8, 37), dtype=np.float32)
    label = np.ones((162, 50, 50, 8, 6), dtype=np.float32)
    np.save(train_path + "inputs.npy", inputs)
    np.save(train_path + "label.npy", label)

    scale = np.ones((6, 162), dtype=np.float32)
    np.save(test_path + "inputs.npy", inputs)
    np.save(test_path + "label.npy", label)
    np.save(test_path + "scale.npy", scale)
