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
"""test geometry module: 2d cases"""
import pytest
from easydict import EasyDict as edict

from mindelec.geometry import create_config_from_edict
from mindelec.geometry import Rectangle, Disk

disk_random = edict({
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

disk_mesh = edict({
    'domain': edict({
        'random_sampling': False,
        'size': [100, 180],
    }),
    'BC': edict({
        'random_sampling': False,
        'size': [20, 10],
        'with_normal': False,
    }),
})

disk_mesh_wrong_meshsize = edict({
    'domain': edict({
        'random_sampling': False,
        'size': [100, 180, 200],
    }),
    'BC': edict({
        'random_sampling': False,
        'size': 200,
        'with_normal': False,
    }),
})

disk_mesh_nodomain = edict({
    'BC': edict({
        'random_sampling': False,
        'size': 200,
        'with_normal': False,
    }),
})

disk_mesh_nobc = edict({
    'domain': edict({
        'random_sampling': True,
        'size': 1000,
        'sampler': 'uniform'
    }),
})


def check_disk_random(disk_config):
    """check_disk_random"""
    with pytest.raises(ValueError):
        disk = Disk("disk", (-1.0, 0), -2.0)
    with pytest.raises(ValueError):
        disk = Disk("disk", (-1.0, 0, 3), 2.0)

    disk = Disk("disk", (-1.0, 0), 2.0)
    for samplers in ["uniform", "lhs", "halton", "sobol"]:
        print("check random sampler: {}".format(samplers))
        if "domain" in disk_config.keys():
            disk_config.domain.sampler = samplers
        if "BC" in disk_config.keys():
            disk_config.BC.sampler = samplers

        try:
            disk.sampling(geom_type="domain")
        except ValueError:
            return

        disk.set_sampling_config(create_config_from_edict(disk_config))
        with pytest.raises(ValueError):
            disk.sampling(geom_type="test")

        domain = disk.sampling(geom_type="domain")

        bc = disk.sampling(geom_type="BC")
        disk.sampling_config.bc.with_normal = True
        bc, bc_normal = disk.sampling(geom_type="BC")
        print(bc, bc_normal, domain)


def check_disk_mesh(disk_config):
    """check_disk_mesh"""
    disk = Disk("disk", (-1.0, 0), 2.0, sampling_config=create_config_from_edict(disk_config))
    domain = disk.sampling(geom_type="domain")

    bc = disk.sampling(geom_type="BC")
    disk.sampling_config.bc.with_normal = True
    bc, bc_normal = disk.sampling(geom_type="BC")
    print(bc, bc_normal, domain)


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
        'with_normal': True,
    }),
})

rectangle_mesh = edict({
    'domain': edict({
        'random_sampling': False,
        'size': [50, 25],
    }),
    'BC': edict({
        'random_sampling': False,
        'size': 300,
        'with_normal': True,
    }),
})


def check_rectangle_random(config):
    """check_rectangle_random"""
    rectangle = Rectangle("rectangle", (-3.0, 1), (1, 2))
    for samplers in ["uniform", "lhs", "halton", "sobol"]:
        print("check random sampler: {}".format(samplers))
        if "domain" in config.keys():
            config.domain.sampler = samplers
        if "BC" in config.keys():
            config.BC.sampler = samplers
            config.BC.with_normal = True
        rectangle.set_sampling_config(create_config_from_edict(config))
        domain = rectangle.sampling(geom_type="domain")
        bc, bc_normal = rectangle.sampling(geom_type="BC")

        if "BC" in config.keys():
            config.BC.with_normal = False
        rectangle.set_sampling_config(create_config_from_edict(config))
        bc = rectangle.sampling(geom_type="BC")
        print(bc, bc_normal, domain)


def check_rectangle_mesh(config):
    """check_rectangle_mesh"""
    rectangle = Rectangle("rectangle", (-3.0, 1), (1, 2))
    if "BC" in config.keys():
        config.BC.with_normal = True
    rectangle.set_sampling_config(create_config_from_edict(config))
    domain = rectangle.sampling(geom_type="domain")
    bc, bc_normal = rectangle.sampling(geom_type="BC")

    if "BC" in config.keys():
        config.BC.with_normal = False
    rectangle.set_sampling_config(create_config_from_edict(config))
    bc = rectangle.sampling(geom_type="BC")
    print(bc, bc_normal, domain)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_disk_random():
    """test_check_disk_random"""
    check_disk_random(disk_random)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_disk_mesh():
    """test_check_disk_mesh"""
    check_disk_mesh(disk_mesh)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_disk_mesh_wrong_meshsize_error():
    """test_check_disk_mesh"""
    with pytest.raises(ValueError):
        check_disk_mesh(disk_mesh_wrong_meshsize)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_disk_mesh_nodomain_error():
    """test_check_disk_mesh"""
    with pytest.raises(KeyError):
        check_disk_mesh(disk_mesh_nodomain)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_disk_mesh_nobc_error():
    """test_check_disk_mesh"""
    with pytest.raises(KeyError):
        check_disk_mesh(disk_mesh_nobc)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_rectangle_random():
    """test_check_rectangle_random"""
    check_rectangle_random(rectangle_random)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_rectangle_mesh():
    """test_check_rectangle_mesh"""
    check_rectangle_mesh(rectangle_mesh)
