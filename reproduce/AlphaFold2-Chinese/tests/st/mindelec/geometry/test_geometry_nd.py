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
"""test geometry module: nd cases"""
import pytest
from easydict import EasyDict as edict

from mindelec.geometry import create_config_from_edict
from mindelec.geometry import Cuboid

cuboid_random = edict({
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

cuboid_random2 = edict({
    'BC': edict({
        'random_sampling': True,
        'size': 200,
        'sampler': 'uniform',
        'with_normal': False,
    }),
})

cuboid_mesh = edict({
    'domain': edict({
        'random_sampling': False,
        'size': [20, 30, 10],
    }),
    'BC': edict({
        'random_sampling': False,
        'size': 900,
        'with_normal': True,
    }),
})


cuboid_mesh2 = edict({
    'domain': edict({
        'random_sampling': False,
        'size': [20, 30],
    }),
    'BC': edict({
        'random_sampling': False,
        'size': 900,
        'with_normal': True,
    }),
})

def check_cuboid_random(cuboid_config):
    """check_cuboid_random"""

    cuboid = Cuboid("Cuboid", (-3, -1, 0), [-1, 2, 1])
    for samplers in ["uniform", "lhs", "halton", "sobol"]:
        print("check random sampler: {}".format(samplers))
        if "domain" in cuboid_config.keys():
            cuboid_config.domain.sampler = samplers
        if "BC" in cuboid_config.keys():
            cuboid_config.BC.sampler = samplers

        try:
            cuboid.set_sampling_config("test")
        except TypeError:
            print("set_sampling_config TypeError")

        try:
            cuboid.sampling(geom_type="domain")
        except ValueError:
            print("sampling ValueError")

        cuboid.set_sampling_config(create_config_from_edict(cuboid_config))
        domain = cuboid.sampling(geom_type="domain")
        bc = cuboid.sampling(geom_type="BC")
        assert domain.shape == (1000, 3)
        assert bc.shape == (199, 3)


def check_cuboid_mesh(cuboid_config):
    """check_cuboid_mesh"""
    cuboid = Cuboid("Cuboid", (-3, -1, 0), [-1, 2, 1], sampling_config=create_config_from_edict(cuboid_config))
    domain = cuboid.sampling(geom_type="domain")
    bc, bc_normal = cuboid.sampling(geom_type="BC")
    assert domain.shape == (6000, 3)
    assert bc.shape == (556, 3)
    assert bc_normal.shape == (556, 3)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_cuboid_random():
    """test_check_cuboid_random"""
    check_cuboid_random(cuboid_random)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_cuboid_random_nodomain_error():
    """test_check_cuboid_random"""
    with pytest.raises(KeyError):
        check_cuboid_random(cuboid_random2)

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_cuboid_mesh():
    """test_check_cuboid_mesh"""
    check_cuboid_mesh(cuboid_mesh)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_cuboid_mesh_meshsize_error():
    """test_check_cuboid_mesh"""
    with pytest.raises(ValueError):
        check_cuboid_mesh(cuboid_mesh2)
