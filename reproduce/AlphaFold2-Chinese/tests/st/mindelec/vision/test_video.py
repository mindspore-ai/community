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

import os
import pytest
import numpy as np
from mindelec.vision import plot_eh, image_to_video


def image_to_video_temp():
    """image to video test"""
    path_image = './image'
    eh = np.random.rand(5, 10, 10, 10, 6).astype(np.float32)
    plot_eh(eh, path_image, 5, 300)

    path_video = './result_video'
    video_name = 'video.avi'
    fps = 20
    image_to_video(path_image, path_video, video_name, fps)

    assert os.path.exists(path_video)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_image_to_video():
    """test image to video"""
    image_to_video_temp()
