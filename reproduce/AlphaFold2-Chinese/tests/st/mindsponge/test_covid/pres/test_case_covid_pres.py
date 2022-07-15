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
"""Test case covid pres"""

import time
import numpy as np
import pytest
from mindspore import context, Tensor
import mindspore.common.dtype as mstype
from mindsponge.md.npt import NPT as Simulation


class ArgsOpt():
    """ArgsOpt"""
    def __init__(self):
        self.amber_parm = '/home/workspace/mindspore_dataset/mindsponge_data/pres/s1ace2.parm7'
        self.box = ''
        self.c = '/home/workspace/mindspore_dataset/mindsponge_data/pres/s1ace2_heat.rst7'
        self.checkpoint = ''
        self.device_id = 0
        self.i = '/home/workspace/mindspore_dataset/mindsponge_data/pres/pres.in'
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
    for i in range(1, 11):
        print_step = 1 if i % simulation.ntwx == 0 or i == 1 or i == simulation.md_info.step_limit else 0
        update_step = 1 if (i != 1 and i % simulation.update_interval == 0) else 0
        temperature, total_potential_energy, sigma_of_bond_ene, sigma_of_angle_ene, sigma_of_dihedral_ene, \
        nb14_lj_energy_sum, nb14_cf_energy_sum, lj_energy_sum, ee_ene, _, _, _, _, _, _, _, _ = \
        simulation(Tensor(i), Tensor(print_step), Tensor(update_step, mstype.int32))
        if i == 1:
            start = time.time()
            print(temperature, total_potential_energy, sigma_of_bond_ene, sigma_of_angle_ene, sigma_of_dihedral_ene, \
                  nb14_lj_energy_sum, nb14_cf_energy_sum, lj_energy_sum, ee_ene)
            assert np.allclose(round(float(temperature.asnumpy()), 3), 298.406, rtol=0.1)
            assert np.allclose(round(float(total_potential_energy.asnumpy()), 3), -320432.750, rtol=0.1)
            assert np.allclose(round(float(sigma_of_bond_ene.asnumpy()), 3), 4228.548, rtol=0.1)
            assert np.allclose(round(float(sigma_of_angle_ene.asnumpy()), 3), 6081.921, rtol=0.1)
            assert np.allclose(round(float(sigma_of_dihedral_ene.asnumpy()), 3), 10484.753, rtol=0.1)
            assert np.allclose(round(float(nb14_lj_energy_sum.asnumpy()), 3), 2990.386, rtol=0.1)
            assert np.allclose(round(float(nb14_cf_energy_sum.asnumpy()), 3), 34394.328, rtol=0.1)
            assert np.allclose(round(float(lj_energy_sum.asnumpy()), 3), 36317.559, rtol=0.1)
            assert np.allclose(round(float(ee_ene.asnumpy()), 3), -414930.250, rtol=0.1)
    end = time.time()
    assert ((end - start) / 9) < 0.1
