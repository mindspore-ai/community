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
"""test geometry module: 1d cases"""
import pytest
from easydict import EasyDict as edict

from mindelec.geometry import create_config_from_edict
from mindelec.geometry import Interval, TimeDomain

line_config_out = edict({
    'domain': edict({
        'random_sampling': True,
        'size': 100,
        'sampler': 'uniform'
    }),
    'BC': edict({
        'random_sampling': True,
        'size': 10,
        'sampler': 'uniform',
    }),
})


line_config_out2 = edict({
    'domain': edict({
        'random_sampling': True,
        'size': 100,
        'sampler': 'uniform'
    }),
    'BC': edict({
        'random_sampling': False,
        'size': 10,
        'sampler': 'uniform',
    }),
})

def check_line_interval_case1(line_config):
    """check_line_interval_case1"""
    try:
        Interval("line", 'test', 1.0, sampling_config=create_config_from_edict(line_config))
    except ValueError:
        return
    line = Interval("line", -1.0, 1.0, sampling_config=create_config_from_edict(line_config))

    domain = line.sampling(geom_type="domain")
    bc = line.sampling(geom_type="BC")
    try:
        line.sampling(geom_type="other")
    except ValueError:
        print("get ValueError when sampling other data")

    # uniform sampling
    if "BC" in line_config.keys():
        line_config.BC = None
    if "domain" in line_config.keys():
        line_config.domain.random_sampling = False
    line.set_sampling_config(create_config_from_edict(line_config))
    domain = line.sampling(geom_type="domain")
    try:
        line.sampling(geom_type="BC")
    except KeyError:
        print("get ValueError when sampling BC data")

    # lhs, halton, sobol
    for samplers in ["lhs", "halton", "sobol"]:
        if "domain" in line_config.keys():
            line_config.domain.random_sampling = True
            line_config.domain.sampler = samplers
        line.set_sampling_config(create_config_from_edict(line_config))
        domain = line.sampling(geom_type="domain")
    print(domain, bc)

time_config = edict({
    'domain': edict({
        'random_sampling': True,
        'size': 100,
        'sampler': 'lhs'
    })
})


def check_time_interval(line_config):
    """check_time_interval"""
    try:
        create_config_from_edict({"test": "test"})
    except ValueError:
        return

    line = TimeDomain("time", 0.0, 1.0, sampling_config=create_config_from_edict(line_config))
    domain = line.sampling(geom_type="domain")
    try:
        line.sampling(geom_type="BC")
    except KeyError:
        print("get ValueError when sampling BC data")
    print(domain)

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_time_interval():
    """test_check_time_interval"""
    check_time_interval(time_config)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_line_interval_case1():
    """test_check_time_interval"""
    check_line_interval_case1(line_config_out)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_check_line_interval_case2():
    """test_check_time_interval"""
    check_line_interval_case1(line_config_out2)
