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

rectangle_random = edict({
    'domain': edict({
        'random_sampling': True,
        'size': 1000,
        'sampler': 'uniform'
    }),
    'BC': edict({
        'random_sampling': True,
        'size': 200,
        'sampler': 'uniform',
        'with_normal': False,
    }),
})

rectangle_mesh = edict({
    'domain': edict({
        'random_sampling': False,
        'size': [10, 20],
    }),
    'BC': edict({
        'random_sampling': False,
        'size': 50,
        'with_normal': False,
    }),
})

time_random = edict({
    'domain': edict({
        'random_sampling': True,
        'size': 10,
        'sampler': 'lhs'
    })
})

time_mesh = edict({
    'domain': edict({
        'random_sampling': False,
        'size': 10,
    })
})

time_mesh2 = edict({
    'domain': edict({
        'random_sampling': False,
        'size': 10000,
    })
})

time_mesh3 = edict({
    'IC': edict({
        'random_sampling': False,
        'size': 10000,
    })
})

reset_geom_time_config = edict({
    'domain': edict({
        'random_sampling': False,
        'size': [10, 20],
    }),
    'BC': edict({
        'random_sampling': False,
        'size': 50,
        'with_normal': True,
    }),
    'IC': edict({
        'random_sampling': False,
        'size': [10, 10],
    }),
    'time': edict({
        'random_sampling': False,
        'size': 10,
    })
})

reset_geom_time_config2 = edict({
    'domain': edict({
        'random_sampling': False,
        'size': [10, 20],
    }),
    'BC': edict({
        'random_sampling': False,
        'size': 50,
        'with_normal': True,
    }),
    'IC': edict({
        'random_sampling': False,
        'size': [10, 10],
    }),
    'time': edict({
        'random_sampling': True,
        'size': 10,
    })
})

reset_geom_time_config3 = edict({
    'domain': edict({
        'random_sampling': True,
        'size': 200,
    }),
    'BC': edict({
        'random_sampling': True,
        'size': 50,
        'with_normal': True,
    }),
    'IC': edict({
        'random_sampling': False,
        'size': [10, 10],
    }),
    'time': edict({
        'random_sampling': True,
        'size': 10,
    })
})

reset_geom_time_config4 = edict({
    'domain': edict({
        'random_sampling': True,
        'size': 200,
    }),
    'BC': edict({
        'random_sampling': True,
        'size': 50,
        'with_normal': True,
    }),
    'IC': edict({
        'random_sampling': True,
        'size': 100,
    }),
    'time': edict({
        'random_sampling': False,
        'size': 10,
    })
})

reset_geom_time_config5 = edict({
    'time': edict({
        'random_sampling': False,
        'size': 10,
    })
})

def check_rect_with_time_init_config(rect_config, time_config):
    """check_rect_with_time_init_config"""
    rect = Rectangle("rect", [-1.0, -0.5], [1.0, 0.5], sampling_config=create_config_from_edict(rect_config))
    time = TimeDomain("time", 0.0, 1.0, sampling_config=create_config_from_edict(time_config))
    rect_with_time = GeometryWithTime(rect, time)

    # check info
    print("check rect_with_time initial config: {}".format(rect_with_time.__dict__))
    if rect_with_time.sampling_config is not None:
        for key, value in rect_with_time.sampling_config.__dict__.items():
            if value is not None:
                print("  get attr: {}, value: {}".format(key, value.__dict__))

    # sampling
    config = rect_with_time.sampling_config
    if config is None:
        raise ValueError
    if config.domain is not None:
        domain = rect_with_time.sampling(geom_type="domain")
        print("check domain points: {}".format(domain.shape))
    if config.bc is not None:
        if config.bc.with_normal:
            bc, bc_normal = rect_with_time.sampling(geom_type="BC")
            print("check bc points: {}, bc_normal: {}".format(bc.shape, bc_normal.shape))
        else:
            bc = rect_with_time.sampling(geom_type="BC")
            print("check bc points: {}".format(bc.shape))
    if config.ic is not None:
        ic = rect_with_time.sampling(geom_type="IC")
        print("check ic points: {}".format(ic.shape))


def check_rect_with_time_set_config(config):
    """check_rect_with_time_set_config"""
    rect = Rectangle("rect", [-1.0, -0.5], [1.0, 0.5])
    time = TimeDomain("time", 0.0, 1.0)
    try:
        GeometryWithTime(rect, time, create_config_from_edict(config))
    except ValueError:
        print("create_config_from_edict ValueError")

    rect_with_time = GeometryWithTime(rect, time)
    try:
        rect_with_time.sampling(geom_type="domain")
    except ValueError:
        print("sampling ValueError")

    rect_with_time.set_sampling_config(create_config_from_edict(config))

    try:
        rect_with_time.sampling(geom_type="test")
    except ValueError:
        print("sampling ValueError")
    # sampling
    config = rect_with_time.sampling_config
    if config.domain is not None:
        domain = rect_with_time.sampling(geom_type="domain")
        print("check domain points: {}".format(domain.shape))
    else:
        try:
            rect_with_time.sampling(geom_type="domain")
        except ValueError:
            print("sampling KeyError")
    if config.bc is not None:
        if config.bc.with_normal:
            bc, bc_normal = rect_with_time.sampling(geom_type="BC")
            print("check bc points: {}, bc_normal: {}".format(bc.shape, bc_normal.shape))
            normal = copy.deepcopy(bc)
            normal[:, :2] = bc[:, :2] + bc_normal[:, :]
        else:
            bc = rect_with_time.sampling(geom_type="BC")
            print("check bc points: {}".format(bc.shape))
    else:
        try:
            rect_with_time.sampling(geom_type="BC")
        except ValueError:
            print("sampling KeyError")
    if config.ic is not None:
        ic = rect_with_time.sampling(geom_type="IC")
        print("check ic points: {}".format(ic.shape))
    else:
        try:
            rect_with_time.sampling(geom_type="IC")
        except ValueError:
            print("sampling KeyError")


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_rect_with_time_init_config():
    """test_check_rect_with_time_init_config"""
    check_rect_with_time_init_config(rectangle_random, time_random)
    check_rect_with_time_init_config(rectangle_mesh, time_random)
    check_rect_with_time_init_config(rectangle_mesh, time_mesh2)
    check_rect_with_time_init_config(rectangle_random, time_mesh)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_rect_with_time_init_config_error():
    """test_check_rect_with_time_init_config"""
    with pytest.raises(ValueError):
        check_rect_with_time_init_config(rectangle_mesh, time_mesh3)

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_rect_with_time_set_config():
    """test_check_rect_with_time_set_config"""
    check_rect_with_time_set_config(reset_geom_time_config)
    check_rect_with_time_set_config(reset_geom_time_config2)
    check_rect_with_time_set_config(reset_geom_time_config3)
    check_rect_with_time_set_config(reset_geom_time_config4)
    check_rect_with_time_set_config(reset_geom_time_config4)

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_rect_with_time_set_config2():
    """test_check_rect_with_time_set_config"""
    with pytest.raises(ValueError):
        check_rect_with_time_set_config(rectangle_random)
