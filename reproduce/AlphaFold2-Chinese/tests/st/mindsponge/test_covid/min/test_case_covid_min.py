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
"""Test case covid min"""

import time
import numpy as np
import pytest
from mindspore import context, Tensor
from mindsponge.md.simulation import Simulation

class ArgsOpt():
    """ArgsOpt"""
    def __init__(self):
        self.amber_parm = '/home/workspace/mindspore_dataset/mindsponge_data/min1/s1ace2.parm7'
        self.box = ''
        self.c = '/home/workspace/mindspore_dataset/mindsponge_data/min1/s1ace2_min1.rst7'
        self.checkpoint = ''
        self.device_id = 0
        self.i = '/home/workspace/mindspore_dataset/mindsponge_data/min1/min1.in'
        self.o = ''
        self.r = ''
        self.u = False
        self.x = ''

@pytest.mark.level0
@pytest.mark.platform_x86_gpu_training
@pytest.mark.env_onecard
def test_case_poly():
    """test_case_covid_min"""
    context.set_context(mode=context.GRAPH_MODE, device_target="GPU", save_graphs=False)
    args_opt = ArgsOpt()
    simulation = Simulation(args_opt)
    for i in range(10):
        temperature, total_potential_energy, sigma_of_bond_ene, sigma_of_angle_ene, sigma_of_dihedral_ene, \
        nb14_lj_energy_sum, nb14_cf_energy_sum, lj_energy_sum, ee_ene, _, _, _, _ = \
        simulation(Tensor(i), Tensor(0))
        if i == 0:
            print(temperature, total_potential_energy, sigma_of_bond_ene, sigma_of_angle_ene, sigma_of_dihedral_ene, \
        nb14_lj_energy_sum, nb14_cf_energy_sum, lj_energy_sum, ee_ene)
            start = time.time()
            assert np.allclose(round(float(temperature.asnumpy()), 3), 0.000, rtol=0.1)
            assert np.allclose(round(float(total_potential_energy.asnumpy()), 3), 39327864.000, rtol=0.1)
            assert np.allclose(round(float(sigma_of_bond_ene.asnumpy()), 3), 418.748, rtol=0.1)
            assert np.allclose(round(float(sigma_of_angle_ene.asnumpy()), 3), 1351.111, rtol=0.1)
            assert np.allclose(round(float(sigma_of_dihedral_ene.asnumpy()), 3), 9382.757, rtol=0.1)
            assert np.allclose(round(float(nb14_lj_energy_sum.asnumpy()), 3), 3714.295, rtol=0.1)
            assert np.allclose(round(float(nb14_cf_energy_sum.asnumpy()), 3), 36175.125, rtol=0.1)
            assert np.allclose(round(float(lj_energy_sum.asnumpy()), 3), 39634900.000, rtol=0.1)
            assert np.allclose(round(float(ee_ene.asnumpy()), 3), -358078.625, rtol=0.1)
    end = time.time()

    assert ((end - start) / 9) < 0.1
