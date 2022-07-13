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
"""EncoderDecoder for MindElec."""

import mindspore.nn as nn
import mindspore.ops as ops


class EncoderDecoder(nn.Cell):
    """
    EncoderDecoder architecture for MindElec.

    Args:
        input_dim (int): input channel.
        target_shape (list or tuple): Output DWH shape.
        base_channels (int): base channel, all intermediate layers' channels are multiple of this value.
        decoding (bool): Enable Decoder, True if the reconstructed input is need,
                         for example, the training. Default: False

    Returns:
        Tensor, output tensor, compressed encodings (encoding=False) or reconstructed input (encoding=True).

    Examples:
        >>> training encoder: Encoder_Decoder(input_dim=4, target_shape=[25, 50, 25], base_channels=8, decoding=True)
        >>> applying encoder(data compression): Encoder_Decoder(input_dim=4,
        ...                                                     target_shape=[25, 50, 25],
        ...                                                     base_channels=8,
        ...                                                     decoding=False)
    """

    def __init__(self, input_dim, target_shape, base_channels=8, decoding=False):
        super(EncoderDecoder, self).__init__()
        self.decoding = decoding
        self.encoder = Encoder(input_dim, base_channels)
        if self.decoding:
            self.decoder = Decoder(input_dim, target_shape, base_channels)

    def construct(self, x):
        encoding = self.encoder(x)
        if self.decoding:
            output = self.decoder(encoding)
        else:
            output = encoding
        return output


class Encoder(nn.Cell):
    """
    Encoder architecture.

    Args:
        input_dim (int): input channel.
        base_channels (int): base channel, all intermediate layers' channels are multiple of this value.

    Returns:
        Tensor, output tensor.

    Examples:
        >>> Encoder(input_dim=4, base_channels=8)
    """

    def __init__(self, input_dim, base_channels):
        super(Encoder, self).__init__()
        print("BASE_CHANNELS: %d" %base_channels)
        self.input_dim = input_dim
        self.channels = base_channels

        self.conv0 = nn.Conv3d(self.input_dim, self.channels*2, kernel_size=3, pad_mode='pad', padding=1)
        self.conv0_1 = nn.Conv3d(self.channels*2, self.channels*2, kernel_size=3, pad_mode='pad', padding=1)
        self.conv1 = nn.Conv3d(self.channels*2, self.channels*4, kernel_size=3, pad_mode='pad', padding=1)
        self.conv1_1 = nn.Conv3d(self.channels*4, self.channels*4, kernel_size=3, pad_mode='pad', padding=1)
        self.conv2 = nn.Conv3d(self.channels*4, self.channels*8, kernel_size=3, pad_mode='pad', padding=1)
        self.conv2_1 = nn.Conv3d(self.channels*8, self.channels*8, kernel_size=3, pad_mode='pad', padding=1)
        self.conv3 = nn.Conv3d(self.channels*8, self.channels*16, kernel_size=(2, 3, 2))
        self.conv4 = nn.Conv2d(self.channels*16, self.channels*32, kernel_size=(1, 3), pad_mode='pad', padding=0)

        self.bn0 = nn.BatchNorm3d(self.channels*2)
        self.bn1 = nn.BatchNorm3d(self.channels*4)
        self.bn2 = nn.BatchNorm3d(self.channels*8)
        self.bn3 = nn.BatchNorm3d(self.channels*16)
        self.bn4 = nn.BatchNorm2d(self.channels*32)

        self.down1 = ops.MaxPool3D(kernel_size=(2, 2, 2), strides=(2, 2, 2))
        self.down2 = ops.MaxPool3D(kernel_size=(2, 2, 2), strides=(2, 2, 2))
        self.down3 = ops.MaxPool3D(kernel_size=(2, 2, 2), strides=(2, 2, 2))
        self.down4 = nn.MaxPool2d(kernel_size=(2, 6), stride=(2, 6))

        self.down_1_1 = ops.MaxPool3D(kernel_size=(4, 5, 4), strides=(4, 5, 4))
        self.down_1 = nn.MaxPool2d(kernel_size=(3, 5*3))

        self.down_2_1 = ops.MaxPool3D(kernel_size=(3, 4, 3), strides=(3, 4, 3))
        self.down_2 = nn.MaxPool2d(kernel_size=(2, 3*2))

        self.down_3 = nn.MaxPool2d(kernel_size=(3, 18))

        self.act = nn.Sigmoid()

        self.concat = ops.Concat(axis=1)
        self.expand_dims = ops.ExpandDims()

    def construct(self, x):
        """forward"""
        bs = x.shape[0]

        x = self.conv0(x)
        x = self.conv0_1(x)
        x = self.bn0(x)
        x = self.act(x)
        x = self.down1(x)
        x_1 = self.down_1_1(x)
        x_1 = self.down_1(x_1.view(bs, x_1.shape[1], x_1.shape[2], -1))

        x = self.conv1(x)
        x = self.conv1_1(x)
        x = self.bn1(x)
        x = self.act(x)
        x = self.down2(x)
        x_2 = self.down_2_1(x)
        x_2 = self.down_2(x_2.view(bs, x_2.shape[1], x_2.shape[2], -1))

        x = self.conv2(x)
        x = self.conv2_1(x)
        x = self.bn2(x)
        x = self.act(x)
        x = self.down3(x)
        x_3 = self.down_3(x.view(bs, x.shape[1], x.shape[2], -1))

        x = self.act(self.bn3(self.conv3(x)))
        x = x.view((bs, x.shape[1], x.shape[2], -1))
        x = self.down4(x)

        x = self.act(self.bn4(self.conv4(x)))
        x = self.concat((x, x_1, x_2, x_3))
        x = self.expand_dims(x, 3)

        return x


class Decoder(nn.Cell):
    """
    Decoder architecture.

    Args:
        output_dim (int): output channel.
        target_shape (list or tuple): Output DWH shape.
        base_channels (int): base channel, all intermediate layers' channels are multiple of this value.

    Returns:
        Tensor, output tensor.

    Examples:
        >>> Decoder(output_dim=4, target_shape=[25, 50, 25], base_channels=8)
    """

    def __init__(self, output_dim, target_shape, base_channels):
        super(Decoder, self).__init__()

        self.output_dim = output_dim
        self.base_channels = base_channels
        self.up0 = Up((32 + 8 + 4 + 2) * self.base_channels,
                      self.base_channels * 32,
                      [1, 1, 1],
                      [x // 8 for x in target_shape],
                      pad=True)
        self.up1 = Up(self.base_channels * 32,
                      self.base_channels * 16,
                      [x // 8 for x in target_shape],
                      [x // 4 for x in target_shape],
                      pad=False)
        self.up2 = Up(self.base_channels * 16,
                      self.base_channels* 4,
                      [x // 4 for x in target_shape],
                      [x // 2 for x in target_shape],
                      pad=False)
        self.up3 = Up(self.base_channels * 4,
                      self.output_dim,
                      [x // 2 for x in target_shape],
                      target_shape,
                      pad=False)

    def construct(self, x):
        x = self.up0(x)
        x = self.up1(x)
        x = self.up2(x)
        x = self.up3(x)

        return x


class DoubleConvTranspose(nn.Cell):
    """
    DoubleConvTranspose architecture

    Args:
        input_dim (int): Input channel.
        out_channel (int): Output channel.
        mid_channels (int): Mid channels. Default: None.

    Returns:
        Tensor, output tensor.

    Examples:
        >>> DoubleConvTranspose(input_dim=4, out_channels=8)
    """

    def __init__(self, input_dim, out_channels, mid_channels=None):
        super(DoubleConvTranspose, self).__init__()
        if not mid_channels:
            mid_channels = out_channels
        self.conv = nn.Conv3dTranspose(input_dim, out_channels, kernel_size=3)
        self.conv1 = nn.Conv3dTranspose(out_channels, out_channels, kernel_size=3)
        self.bn = nn.BatchNorm3d(out_channels)
        self.relu = nn.ReLU()
        self.act = nn.Sigmoid()

    def construct(self, x):
        x = self.conv(x)
        x = self.conv1(x)
        x = self.bn(x)
        x = self.act(x)
        return x


def calculate_difference(input_shape, target_shape):
    """calculate difference of the target shape and the output shape of previous Conv3dTranspose
    and the according padding sizes"""

    target_shape = target_shape

    # calculating output shape of Conv3dTranspose
    input_shape = [(dim - 1)*2 - 2*0 + 1*(2 - 1) + 0 + 1 for dim in input_shape]

    diff = [x - y for x, y in zip(target_shape, input_shape)]
    paddings = [(0, 0), (0, 0)]
    for i in range(3):
        paddings.append((diff[i], 0))
    return tuple(diff), tuple(paddings)


class Up(nn.Cell):
    """
    Upscaling then apply Conv3dTranspose to decode

    Args:
        in_channel (int): Input channel.
        out_channel (int): Output channel.
        input_shape (list or tuple): Input DWH shape. Default: None.
        target_shape (list or tuple): Output DWH shape. Default: None.
        pad (bool): Enable manual padding, only needed in the first layer of the Decoder. Default: True.

    Returns:
        Tensor, output tensor.

    Examples:
        >>> Up(8,4, input_shape=[10, 10, 10], target_shape=[20, 20, 20], pad=False)

    """

    def __init__(self, input_dim, out_channels, input_shape=None, target_shape=None, pad=True):
        super(Up, self).__init__()
        self.pad = pad

        diff, paddings = calculate_difference(input_shape, target_shape)
        if self.pad:
            self.pad = ops.Pad(paddings)
            self.up = nn.Conv3dTranspose(input_dim, input_dim // 2, kernel_size=2, stride=2, pad_mode='pad', padding=0)

        else:
            self.up = nn.Conv3dTranspose(input_dim,
                                         input_dim // 2,
                                         kernel_size=2,
                                         stride=2,
                                         pad_mode='pad',
                                         padding=0,
                                         output_padding=diff)

        self.conv = DoubleConvTranspose(input_dim // 2, out_channels)


    def construct(self, x):
        x = self.up(x)
        if self.pad:
            x = self.pad(x)
        x = self.conv(x)

        return x
