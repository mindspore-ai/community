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
config = ed({
    "epochs": 500,
    "batch_size": 8,
    "lr": 0.0001,
    "t_solution": 162,
    "x_solution": 50,
    "y_solution": 50,
    "z_solution": 8,
    "save_checkpoint_epochs": 5,
    "keep_checkpoint_max": 20
})
