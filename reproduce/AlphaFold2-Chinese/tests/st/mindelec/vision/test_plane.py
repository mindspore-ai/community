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
"""Visualization of the results in 2D image form"""

import numpy as np
import pytest
from mindelec.vision import plot_s11, plot_eh


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_plane_plot_s11():
    """test plane plot S11"""
    s11 = np.random.rand(1001, 2).astype(np.float32)
    s11[:, 0] = np.linspace(0, 4 * 10 ** 9, 1001)
    s11 = s11.astype(np.float32)
    plot_s11(s11, './result_s11', 's11')


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_plane_plot_eh():
    """test plane plot eh"""
    eh = np.random.rand(20, 10, 10, 10, 6).astype(np.float32)
    plot_eh(eh, './result_eh', 5, 300)
