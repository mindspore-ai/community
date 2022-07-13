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

# config
config = {
    'base_channels': 8,
    'input_channels': 4,
    'epochs': 2000,
    'batch_size': 8,
    'save_epoch': 100,
    'lr': 0.01,
    'lr_decay_milestones': 5,
    'eval_interval': 20,
    'patch_shape': [25, 50, 25],
}
