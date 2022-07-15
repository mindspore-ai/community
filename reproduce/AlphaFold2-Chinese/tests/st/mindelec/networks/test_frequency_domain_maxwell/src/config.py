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
network config setting, will be used in train.py and eval.py
"""
from easydict import EasyDict as ed

# config
rectangle_sampling_config = ed({
    'domain': ed({
        'random_sampling': False,
        'size': [100, 100],
    }),
    'BC': ed({
        'random_sampling': True,
        'size': 128,
        'with_normal': False,
    })
})

# config
helmholtz_2d_config = ed({
    "name": "Helmholtz2D",
    "columns_list": ["input", "label"],
    "epochs": 10,
    "batch_size": 128,
    "lr": 0.001,
    "coord_min": [0.0, 0.0],
    "coord_max": [1.0, 1.0],
    "axis_size": 101,
    "wave_number": 2
})
