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
"""test geometry module: CSG classes"""
import pytest
from easydict import EasyDict as edict
from mindelec.geometry import create_config_from_edict
from mindelec.geometry import Rectangle, Disk, Interval
from mindelec.geometry import CSGIntersection, CSGDifference, CSGUnion, CSGXOR, CSG

sampling_config_csg = edict({
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

sampling_config_csg2 = edict({
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

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_csg_union():
    """test check union"""
    disk = Disk("disk", (1.2, 0.5), 0.8)
    rect = Rectangle("rect", (-1.0, 0), (1, 1))

    union = CSGUnion(rect, disk, create_config_from_edict(sampling_config_csg))
    union = rect | disk
    for samplers in ["uniform", "lhs", "halton", "sobol"]:
        print("check random sampler: {}".format(samplers))
        if "domain" in sampling_config_csg.keys():
            sampling_config_csg.domain.sampler = samplers
        if "BC" in sampling_config_csg.keys():
            sampling_config_csg.BC.sampler = samplers

        union.set_sampling_config(create_config_from_edict(sampling_config_csg2))
        bc = union.sampling(geom_type="BC")

        union.set_sampling_config(create_config_from_edict(sampling_config_csg))
        domain = union.sampling(geom_type="domain")
        bc, bc_normal = union.sampling(geom_type="BC")
        print(bc, bc_normal, domain)

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_csg_difference():
    """test_check_csg_difference"""
    disk = Disk("disk", (1.2, 0.5), 0.8)
    rect = Rectangle("rect", (-1.0, 0), (1, 1))

    difference = CSGDifference(rect, disk, create_config_from_edict(sampling_config_csg))
    difference = rect - disk
    for samplers in ["uniform", "lhs", "halton", "sobol"]:
        print("check random sampler: {}".format(samplers))
        if "domain" in sampling_config_csg.keys():
            sampling_config_csg.domain.sampler = samplers
        if "BC" in sampling_config_csg.keys():
            sampling_config_csg.BC.sampler = samplers

        difference.set_sampling_config(create_config_from_edict(sampling_config_csg2))
        bc = difference.sampling(geom_type="BC")

        difference.set_sampling_config(create_config_from_edict(sampling_config_csg))
        domain = difference.sampling(geom_type="domain")
        bc, bc_normal = difference.sampling(geom_type="BC")
        print(bc, bc_normal, domain)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_csg_intersection():
    """test_check_csg_intersection"""
    disk = Disk("disk", (1.2, 0.5), 0.8)
    rect = Rectangle("rect", (-1.0, 0), (1, 1))

    intersec = CSGIntersection(rect, disk, create_config_from_edict(sampling_config_csg))
    intersec = rect & disk
    for samplers in ["uniform", "lhs", "halton", "sobol"]:
        print("check random sampler: {}".format(samplers))
        if "domain" in sampling_config_csg.keys():
            sampling_config_csg.domain.sampler = samplers
        if "BC" in sampling_config_csg.keys():
            sampling_config_csg.BC.sampler = samplers

        intersec.set_sampling_config(create_config_from_edict(sampling_config_csg2))
        bc = intersec.sampling(geom_type="BC")

        intersec.set_sampling_config(create_config_from_edict(sampling_config_csg))
        domain = intersec.sampling(geom_type="domain")
        bc, bc_normal = intersec.sampling(geom_type="BC")
        print(bc, bc_normal, domain)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_csg_xor():
    """test_check_csg_xor"""
    disk = Disk("disk", (1.2, 0.5), 0.8)
    rect = Rectangle("rect", (-1.0, 0), (1, 1))

    xor = CSGXOR(rect, disk, create_config_from_edict(sampling_config_csg))
    xor = rect ^ disk
    for samplers in ["uniform", "lhs", "halton", "sobol"]:
        print("check random sampler: {}".format(samplers))
        if "domain" in sampling_config_csg.keys():
            sampling_config_csg.domain.sampler = samplers
        if "BC" in sampling_config_csg.keys():
            sampling_config_csg.BC.sampler = samplers

        xor.set_sampling_config(create_config_from_edict(sampling_config_csg2))
        bc = xor.sampling(geom_type="BC")

        xor.set_sampling_config(create_config_from_edict(sampling_config_csg))
        domain = xor.sampling(geom_type="domain")
        bc, bc_normal = xor.sampling(geom_type="BC")
        print(bc, bc_normal, domain)


no_src_sampling_config = edict({
    'domain': edict({
        'random_sampling': True,
        'size': 200,
        'sampler': 'uniform'
    }),
})

no_src_sampling_config1 = edict({
    'BC': edict({
        'random_sampling': True,
        'size': 200,
        'sampler': 'uniform',
        'with_normal': False
    }),
})

no_src_sampling_config2 = edict({
    'domain': edict({
        'random_sampling': False,
        'size': [10, 10]
    }),
})

no_src_sampling_config3 = edict({
    'BC': edict({
        'random_sampling': False,
        'size': [10, 10]
    }),
})

no_src_sampling_config4 = edict({
    'IC': edict({
        'random_sampling': False,
        'size': [10, 10]
    }),
})

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_point_src_csg():
    """test_check_point_src_csg"""
    src_region = Disk("src", (0.0, 0.0), 0.2)
    rectangle = Rectangle("rect", (-1, -1), (1, 1))
    line = Interval("line", -1, 1)

    with pytest.raises(TypeError):
        no_src_region = CSG("test", rectangle, 2, [0, 0], [1, 1])
    with pytest.raises(TypeError):
        no_src_region = CSG("test", 2, rectangle, [0, 0], [1, 1])
    with pytest.raises(ValueError):
        no_src_region = CSG("test", rectangle, line, [0, 0], [1, 1])

    no_src_region = rectangle - src_region
    no_src_region.set_name("no_src")

    with pytest.raises(ValueError):
        no_src_region.set_sampling_config(None)

    with pytest.raises(TypeError):
        no_src_region.set_sampling_config("test")

    with pytest.raises(ValueError):
        no_src_region.set_sampling_config(create_config_from_edict(no_src_sampling_config2))

    with pytest.raises(ValueError):
        no_src_region.set_sampling_config(create_config_from_edict(no_src_sampling_config3))

    with pytest.raises(ValueError):
        no_src_region.set_sampling_config(create_config_from_edict(no_src_sampling_config4))

    no_src_region.set_sampling_config(create_config_from_edict(no_src_sampling_config))
    with pytest.raises(KeyError):
        no_src_region.sampling(geom_type="BC")

    no_src_region.set_sampling_config(create_config_from_edict(no_src_sampling_config1))
    with pytest.raises(KeyError):
        no_src_region.sampling(geom_type="domain")
    with pytest.raises(ValueError):
        no_src_region.sampling(geom_type="test")

    no_src_region.sampling(geom_type="BC")
