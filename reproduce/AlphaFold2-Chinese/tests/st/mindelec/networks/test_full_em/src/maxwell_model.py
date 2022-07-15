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
"""
maxwell 3d model
"""

import mindspore.nn as nn
from mindspore.ops import operations as P
import mindspore.ops.functional as F
from mindelec.architecture import get_activation


class Maxwell3D(nn.Cell):
    """maxwell3d"""
    def __init__(self, output_dim):
        super(Maxwell3D, self).__init__()

        self.output_dim = output_dim
        width = 64
        self.net0 = ModelHead(4, width)
        self.net1 = ModelHead(4, width)
        self.net2 = ModelHead(4, width)
        self.net3 = ModelHead(4, width)
        self.net4 = ModelHead(4, width)

        self.fc0 = nn.Dense(width+33, 128)
        self.net = ModelOut(128, output_dim, (2, 2, 1), (2, 2, 1))
        self.cat = P.Concat(axis=-1)

    def construct(self, x):
        """forward"""
        x_location = x[..., :4]
        x_media = x[..., 4:]
        out1 = self.net0(x_location)
        out2 = self.net1(2*x_location)
        out3 = self.net2(4*x_location)
        out4 = self.net3(8*x_location)
        out5 = self.net4(16.0*x_location)
        out = out1 + out2 + out3 + out4 + out5
        out = self.cat((out, x_media))
        out = self.fc0(out)
        out = self.net(out)
        return out


class ModelHead(nn.Cell):
    """model_head"""
    def __init__(self, input_dim, output_dim):
        super(ModelHead, self).__init__()
        self.output_dim = output_dim
        self.fc0 = nn.Dense(input_dim, output_dim)
        self.fc1 = nn.Dense(output_dim, output_dim)
        self.act0 = get_activation('srelu')
        self.act1 = get_activation('srelu')

    def construct(self, x):
        """forward"""
        x = self.fc0(x)
        x = self.act0(x)
        x = self.fc1(x)
        x = self.act1(x)

        return x


class ModelOut(nn.Cell):
    """model out"""
    def __init__(self, input_dim, output_dim, kernel_size=2, strides=2):
        super(ModelOut, self).__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.base_channels = 64
        self.inc = DoubleConv(self.input_dim, self.base_channels)
        self.down1 = Down(self.base_channels, self.base_channels * 2, kernel_size, strides)
        self.down2 = Down(self.base_channels * 2, self.base_channels * 4, kernel_size, strides)
        self.down3 = Down(self.base_channels * 4, self.base_channels * 8, kernel_size, strides)
        self.down4 = Down(self.base_channels * 8, self.base_channels * 16, kernel_size, strides)
        self.up1 = Up(self.base_channels * 16, self.base_channels * 8, kernel_size, strides)
        self.up2 = Up(self.base_channels * 8, self.base_channels * 4, kernel_size, strides)
        self.up3 = Up(self.base_channels * 4, self.base_channels * 2, kernel_size, strides)
        self.up4 = Up(self.base_channels * 2, self.base_channels, kernel_size, strides)

        self.fc1 = nn.Dense(self.base_channels+128, 64)
        self.fc2 = nn.Dense(64, output_dim)
        self.relu = nn.ReLU()
        self.transpose = P.Transpose()
        self.cat = P.Concat(axis=1)

    def construct(self, x):
        """forward"""
        x0 = self.transpose(x, (0, 4, 1, 2, 3))
        x1 = self.inc(x0)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)
        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        x = self.cat((x, x0))
        x = self.transpose(x, (0, 2, 3, 4, 1))
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)

        return x


class DoubleConv(nn.Cell):
    """double conv"""
    def __init__(self, input_dim, out_channels, mid_channels=None):
        super().__init__()
        if not mid_channels:
            mid_channels = out_channels
        self.double_conv = nn.SequentialCell(
            nn.Conv3d(input_dim, mid_channels, kernel_size=3),
            nn.BatchNorm3d(mid_channels),
            nn.ReLU(),
            nn.Conv3d(mid_channels, out_channels, kernel_size=3),
            nn.BatchNorm3d(out_channels),
            nn.ReLU()
        )

    def construct(self, x):
        """forward"""
        return self.double_conv(x)


class Down(nn.Cell):
    """down"""
    def __init__(self, input_dim, out_channels, kernel_size=2, strides=2):
        super().__init__()
        self.conv = DoubleConv(input_dim, out_channels)
        self.maxpool = P.MaxPool3D(kernel_size=kernel_size, strides=strides)

    def construct(self, x):
        """forward"""
        x = self.maxpool(x)
        return self.conv(x)


class Up(nn.Cell):
    """up"""
    def __init__(self, input_dim, out_channels, kernel_size=2, strides=2):
        super().__init__()
        self.up = nn.Conv3dTranspose(input_dim, input_dim // 2, kernel_size=kernel_size, stride=strides)
        self.conv = DoubleConv(input_dim, out_channels)
        self.cat = P.Concat(axis=1)

    def construct(self, x1, x2):
        """forward"""
        x1 = self.up(x1)

        _, _, h1, w1, c1 = F.shape(x1)
        _, _, h2, w2, c2 = F.shape(x2)
        diff_z = c2 - c1
        diff_y = w2 - w1
        diff_x = h2 - h1

        x1 = P.Pad(((0, 0), (0, 0), (diff_x // 2, diff_x - diff_x // 2), (diff_y // 2, diff_y - diff_y // 2),
                    (diff_z // 2, diff_z - diff_z // 2)))(x1)
        x = self.cat((x2, x1))
        return self.conv(x)
