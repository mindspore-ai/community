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
"""test geometry module: geometry with time cases"""

import copy
import pytest
from easydict import EasyDict as edict

from mindelec.geometry import create_config_from_edict
from mindelec.geometry import Rectangle, GeometryWithTime, TimeDomain
from mindelec.data import Equation

reset_geom_time_config = edict({
    'domain': edict({
        'random_sampling': False,
        'size': [5, 2],
    }),
    'time': edict({
        'random_sampling': False,
        'size': 10,
    })
})

reset_geom_time_config2 = edict({
    'domain': edict({
        'random_sampling': True,
        'size': 10,
    }),
    'time': edict({
        'random_sampling': False,
        'size': 10,
    })
})

def check_rect_with_time_set_config(config):
    """check_rect_with_time_set_config"""
    rect = Rectangle("rect", [-1.0, -0.5], [1.0, 0.5])
    time = TimeDomain("time", 0.0, 1.0)
    rect_with_time = GeometryWithTime(rect, time)

    with pytest.raises(TypeError):
        Equation(0)
    with pytest.raises(ValueError):
        Equation(rect_with_time)

    config1 = copy.deepcopy(config)
    config1.pop('domain')
    rect_with_time.set_sampling_config(create_config_from_edict(config1))
    with pytest.raises(KeyError):
        Equation(rect_with_time)

    rect_with_time.set_sampling_config(create_config_from_edict(config))
    eq = Equation(rect_with_time)
    for i in range(20):
        print(eq[i])


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_rect_with_time_set_config():
    """test_check_rect_with_time_set_config"""
    check_rect_with_time_set_config(reset_geom_time_config)
    check_rect_with_time_set_config(reset_geom_time_config2)
