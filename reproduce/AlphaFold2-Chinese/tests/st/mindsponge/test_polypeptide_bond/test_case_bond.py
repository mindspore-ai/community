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

import numpy as np
import pytest
from mindspore import context
from simulation_poly_bond import Simulation

context.set_context(mode=context.GRAPH_MODE, device_target="GPU", device_id=0, save_graphs=False)


@pytest.mark.level0
@pytest.mark.platform_x86_gpu_training
@pytest.mark.env_onecard
def test_case_poly():
    """test_case_poly"""
    args_opt = {'amber_parm': '/home/workspace/mindspore_dataset/polypeptide/ala.parm7', 'box': 'mdbox',
                'c': '/home/workspace/mindspore_dataset/polypeptide/ala.rst7', 'checkpoint': '',
                'device_id': 0, 'i': '/home/workspace/mindspore_dataset/polypeptide/nvt.in',
                'o': '', 'r': 'restrt', 'u': False, 'x': ''}
    simulation = Simulation(args_opt)
    sigma_of_bond_ene = simulation()

    assert np.allclose(round(float(sigma_of_bond_ene.asnumpy()), 3), 0.037)
