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
"""test geometry module: base classes"""
import pytest
import numpy as np
from easydict import EasyDict as edict

from mindelec.geometry import Geometry, PartSamplingConfig, SamplingConfig, create_config_from_edict

def check_create_config_from_edict():
    try:
        sampling_config = ["geom", "IC", "BC"]
        config = create_config_from_edict(sampling_config)
        print("check config: {}".format(config))
    except TypeError:
        print("get sampling config type error")


def check_part_sampling_config(size, random_sampling, sampler, random_merge, with_normal):
    try:
        config = PartSamplingConfig(size, random_sampling, sampler, random_merge, with_normal)
        print("check config: {}".format(config.__dict__))
    except TypeError:
        print("get TypeError")


temp_config = edict({
    'domain': edict({
        'random_sampling': True,
        'size': 100,
    }),
    'BC': edict({
        'random_sampling': True,
        'size': 100,
        'sampler': 'uniform',
        'random_merge': True,
    }),
})


def check_sampling_config_case1():
    """check_sampling_config_case1"""
    with pytest.raises(TypeError):
        SamplingConfig("test")
    with pytest.raises(KeyError):
        SamplingConfig({"test": "test"})
    with pytest.raises(TypeError):
        SamplingConfig({"domain": "test"})
    with pytest.raises(TypeError):
        part_sampling_config_dict = {"domain": PartSamplingConfig("test", False, True)}
        SamplingConfig(part_sampling_config_dict)

    part_sampling_config_dict = {"domain": PartSamplingConfig([100, 100], False, "uniform", True, True),
                                 "BC": PartSamplingConfig(100, True, "uniform", True, True)}
    sampling_config_tmp = SamplingConfig(part_sampling_config_dict)
    for attr, config in sampling_config_tmp.__dict__.items():
        if config is not None:
            print("check sampling config: {}: {}".format(attr, config.__dict__))


def check_sampling_config_case2(config_in):
    """check_sampling_config_case2"""
    sampling_config_tmp = create_config_from_edict(config_in)
    for attr, config in sampling_config_tmp.__dict__.items():
        if config is not None:
            print("check sampling config: {}: {}".format(attr, config.__dict__))


def check_sampling_config_case3(config_in):
    """check_sampling_config_case3"""
    config_in.ttime = config_in.domain
    sampling_config_tmp = create_config_from_edict(config_in)
    for attr, config in sampling_config_tmp.__dict__.items():
        if config is not None:
            print("check sampling config: {}: {}".format(attr, config.__dict__))


def check_geometry_case1():
    """check_geometry_case1"""
    with pytest.raises(ValueError):
        Geometry("geom", 2, 0.0, 1.0)
    with pytest.raises(TypeError):
        Geometry("geom", 2, [0, 0], [1, 1], sampling_config="test")

    geom = Geometry("geom", 1, 0.0, 1.0)
    with pytest.raises(TypeError):
        geom.set_sampling_config('test')

    with pytest.raises(NotImplementedError):
        geom.sampling()

    for attr, config in geom.__dict__.items():
        if config is not None:
            print("check sampling config: {}: {}".format(attr, config))

    try:
        geom = Geometry("geom", 1, 1.0, 0.0)
        for attr, config in geom.__dict__.items():
            if config is not None:
                print("check sampling config: {}: {}".format(attr, config))
    except ValueError:
        print("get ValueError")


sampling_config2 = create_config_from_edict(temp_config)


def check_geometry_case2(sampling_config_tmp):
    """check_geometry_case2"""
    geom = Geometry("geom", 1, 0.0, 1.0, sampling_config=sampling_config_tmp)
    geom.set_name("geom_name")
    for attr, config in geom.__dict__.items():
        if config is not None:
            print("check sampling config: {}: {}".format(attr, config))


def check_geometry_case3(config_in):
    """check_geometry_case3"""
    geom = Geometry("geom", 1, 0.0, 1.0)
    for attr, configs in geom.__dict__.items():
        if configs is not None:
            print("check sampling config: {}: {}".format(attr, configs))

    geom.set_name("geom_name")
    geom.set_sampling_config(create_config_from_edict(config_in))
    for attr, config in geom.__dict__.items():
        if attr == "sampling_config" and config is not None:
            print("check sampling config after set: {}: {}".format(attr, config.__dict__))
            for attrs, configs in config.__dict__.items():
                if configs is not None:
                    print("check sampling config: {}: {}".format(attrs, configs.__dict__))
        else:
            if config is not None:
                print("check sampling config after set: {}: {}".format(attr, config))


def check_geometry_case4():
    """check_geometry_case4"""
    try:
        geom = Geometry(10, 1, 1.0, 0.0)
        for attr, config in geom.__dict__.items():
            if config is not None:
                print("check sampling config: {}: {}".format(attr, config))
    except TypeError:
        print("get geom name type error")

    geom = Geometry("geom", 1, 0.0, 1.0)
    try:
        geom.set_name("geom_name")
    except TypeError:
        print("get set geom name type error")
    geom.set_name("geom_name")

    try:
        geom = Geometry("geom", 1.0, 1.0, 2.0)
        for attr, config in geom.__dict__.items():
            if config is not None:
                print("check sampling config: {}: {}".format(attr, config))
    except TypeError:
        print("get geom dim type error")

    try:
        geom = Geometry("geom", 1, 1.0, 0.0)
    except ValueError:
        print("get geom coord value error")

    try:
        geom = Geometry("geom", 1, {"min": 0.0}, {"max": 1.0})
    except TypeError:
        print("get geom coord type error")

    try:
        geom = Geometry("geom", 1, 0.0, 1.0, dtype=np.uint32)
    except TypeError:
        print("get geom data type error")

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_part_sampling_config():
    """test_check_part_sampling_config"""
    check_part_sampling_config(100, True, "uniform", True, True)
    check_part_sampling_config(100, False, "sobol", True, True)
    check_part_sampling_config([100, 100], False, "sobol", True, True)
    check_part_sampling_config([100, 100], True, "uniform", True, True)
    check_part_sampling_config(100, False, "lhs", True, True)
    check_part_sampling_config(100, False, "halton", True, True)
    check_create_config_from_edict()


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_sampling_config_case1():
    """test_check_sampling_config_case1"""
    check_sampling_config_case1()


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_sampling_config_case2():
    """test_check_sampling_config_case2"""
    check_sampling_config_case2(temp_config)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_sampling_config_case3():
    """test_check_sampling_config_case3"""
    check_sampling_config_case3(temp_config)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_geometry_case1():
    """test_check_geometry_case1"""
    check_geometry_case1()


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_geometry_case2():
    """test_check_geometry_case2"""
    check_geometry_case2(sampling_config2)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_geometry_case3():
    """test_check_geometry_case3"""
    check_geometry_case3(temp_config)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_geometry_case4():
    """test_check_geometry_case4"""
    check_geometry_case4()
