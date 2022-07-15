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
"""Test case polypeptide"""

import time
import numpy as np
import pytest
from mindspore import context, Tensor
from mindsponge.md.simulation import Simulation

class ArgsOpt():
    """ArgsOpt"""
    def __init__(self):
        self.amber_parm = '/home/workspace/mindspore_dataset/mindsponge_data/ala/WATER_ALA.parm7'
        self.box = ''
        self.c = '/home/workspace/mindspore_dataset/mindsponge_data/ala/WATER_ALA_350_cool_290.rst7'
        self.checkpoint = ''
        self.device_id = 0
        self.i = '/home/workspace/mindspore_dataset/mindsponge_data/ala/NVT_290_10ns.in'
        self.o = ''
        self.r = ''
        self.u = False
        self.x = ''

@pytest.mark.level0
@pytest.mark.platform_x86_gpu_training
@pytest.mark.env_onecard
def test_case_poly():
    """test_case_poly"""
    context.set_context(mode=context.GRAPH_MODE, device_target="GPU", save_graphs=False)
    args_opt = ArgsOpt()
    simulation = Simulation(args_opt)
    for steps in range(10):
        print_step = steps % simulation.ntwx
        temperature, total_potential_energy, sigma_of_bond_ene, sigma_of_angle_ene, sigma_of_dihedral_ene, \
        nb14_lj_energy_sum, nb14_cf_energy_sum, lj_energy_sum, ee_ene, _, _, _, _ = \
        simulation(Tensor(steps), Tensor(print_step))
        if steps == 0:
            start = time.time()
            assert np.allclose(round(float(temperature.asnumpy()), 3), 0.788, rtol=0.1)
            assert np.allclose(round(float(total_potential_energy.asnumpy()), 3), -5836.541, rtol=0.1)
            assert np.allclose(round(float(sigma_of_bond_ene.asnumpy()), 3), 48.745, rtol=0.1)
            assert np.allclose(round(float(sigma_of_angle_ene.asnumpy()), 3), 0.891, rtol=0.1)
            assert np.allclose(round(float(sigma_of_dihedral_ene.asnumpy()), 3), 14.904, rtol=0.1)
            assert np.allclose(round(float(nb14_lj_energy_sum.asnumpy()), 3), 9.041, rtol=0.1)
            assert np.allclose(round(float(nb14_cf_energy_sum.asnumpy()), 3), 194.479, rtol=0.1)
            assert np.allclose(round(float(lj_energy_sum.asnumpy()), 3), 763.169, rtol=0.1)
            assert np.allclose(round(float(ee_ene.asnumpy()), 3), -6867.770, rtol=0.1)
    end = time.time()

    assert ((end - start) / 9) < 0.007
