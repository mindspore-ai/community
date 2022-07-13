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
# ==============================================================================
"""Visualization of the results 3D VTK form"""

import pytest
import numpy as np
from mindelec.vision import vtk_structure

def vtk_structure_all():
    """vtk_structure_all"""
    grid = np.random.rand(20, 10, 10, 10, 4).astype(np.float32)
    eh = np.random.rand(20, 10, 10, 10, 6).astype(np.float32)
    vtk_structure(grid, eh, './result_vtk')


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_body():
    """test_body"""
    vtk_structure_all()
