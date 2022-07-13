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
"""Visualization of the results in graph 1d 2d"""

import os
import numpy as np
import pytest
from mindelec.vision import print_graph_1d, print_graph_2d


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_print_scatter():
    """test print scatter"""
    print_graph_1d("output.jpg", np.ones(10), "./graph_1d")
    print_graph_2d("output.jpg", np.ones(10), np.ones(10), "./graph_2d")
    assert os.path.exists("./graph_1d/output.jpg")
    assert os.path.exists("./graph_2d/output.jpg")
