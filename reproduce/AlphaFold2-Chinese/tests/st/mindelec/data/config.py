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
sampling and dataset settings
"""

from easydict import EasyDict as edict

ds_config = edict({
    'train': edict({
        'batch_size': 100,
        'shuffle': True,
        'drop_remainder': True,
    }),
    'eval': edict({
        'batch_size': 100,
        'shuffle': False,
        'drop_remainder': False,
    }),
})

src_sampling_config = edict({
    'domain': edict({
        'random_sampling': True,
        'size': 400,
        'sampler': 'uniform'
    }),
    'IC': edict({
        'random_sampling': True,
        'size': 100,
        'sampler': 'uniform',
    }),
    'time': edict({
        'random_sampling': True,
        'size': 10,
        'sampler': 'uniform',
    }),
})

no_src_sampling_config = edict({
    'domain': edict({
        'random_sampling': True,
        'size': 100,
        'sampler': 'uniform'
    }),
    'IC': edict({
        'random_sampling': True,
        'size': 100,
        'sampler': 'uniform',
    }),
    'time': edict({
        'random_sampling': True,
        'size': 10,
        'sampler': 'uniform',
    }),
})

bc_sampling_config = edict({
    'BC': edict({
        'random_sampling': True,
        'size': 100,
        'sampler': 'uniform',
        'with_normal': True
    }),
    'time': edict({
        'random_sampling': True,
        'size': 10,
        'sampler': 'uniform',
    }),
})
