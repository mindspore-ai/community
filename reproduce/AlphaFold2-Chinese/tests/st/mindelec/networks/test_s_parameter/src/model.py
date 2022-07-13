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
"""S parameter prediction model"""

import mindspore.nn as nn
import mindspore.ops as ops


class S11Predictor(nn.Cell):
    """
    S11Predictor architecture for MindElec.

    Args:
        input_dim (int): input channel.

    Returns:
        Tensor, output tensor.

    Examples:
        >>> S11Predictor(input_dim=128)
    """

    def __init__(self, input_dim):
        super(S11Predictor, self).__init__()
        # input shape is [20, 40, 3]
        self.conv1 = nn.Conv3d(input_dim, 512, kernel_size=(3, 3, 1))
        self.conv2 = nn.Conv3d(512, 512, kernel_size=(3, 3, 1))
        self.conv3 = nn.Conv3d(512, 512, kernel_size=(3, 3, 1))
        self.conv4 = nn.Conv3d(512, 512, kernel_size=(2, 1, 3), pad_mode='pad', padding=0)

        self.down1 = ops.MaxPool3D(kernel_size=(2, 3, 1), strides=(2, 3, 1))
        self.down2 = ops.MaxPool3D(kernel_size=(2, 3, 1), strides=(2, 3, 1))
        self.down3 = ops.MaxPool3D(kernel_size=(2, 3, 1), strides=(2, 3, 1))

        self.down_1_1 = ops.MaxPool3D(kernel_size=(1, 13, 1), strides=(1, 13, 1))
        self.down_1_2 = nn.MaxPool2d(kernel_size=(10, 3))

        self.down_2 = nn.MaxPool2d((5, 4*3))

        self.fc1 = nn.Dense(1536, 2048)
        self.fc2 = nn.Dense(2048, 2048)
        self.fc3 = nn.Dense(2048, 1001)

        self.concat = ops.Concat(axis=1)
        self.relu = nn.ReLU()


    def construct(self, x):
        """forward"""
        bs = x.shape[0]

        x = self.conv1(x)
        x = self.relu(x)
        x = self.down1(x)
        x_1 = self.down_1_1(x)
        x_1 = self.down_1_2(x_1.view(bs, x_1.shape[1], x_1.shape[2], -1)).view((bs, -1))

        x = self.conv2(x)
        x = self.relu(x)
        x = self.down2(x)
        x_2 = self.down_2(x.view(bs, x.shape[1], x.shape[2], -1)).view((bs, -1))

        x = self.conv3(x)
        x = self.relu(x)
        x = self.down3(x)

        x = self.conv4(x)
        x = self.relu(x).view((bs, -1))

        x = self.concat([x, x_1, x_2])
        x = self.relu(x).view(bs, -1)

        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)

        return x
