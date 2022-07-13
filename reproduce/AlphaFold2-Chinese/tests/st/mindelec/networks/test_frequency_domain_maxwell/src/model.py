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
feedforward neural network
"""

import mindspore.nn as nn
from mindelec.architecture import get_activation, LinearBlock


class FFNN(nn.Cell):
    """
    Full-connect networks.

    Args:
    input_dim (int): the input dimensions.
    output_dim (int): the output dimensions.
    hidden_layer (int): number of hidden layers.
    activation (str or Cell): activation functions.
    """

    def __init__(self, input_dim, output_dim, hidden_layer=64, activation="sin"):
        super(FFNN, self).__init__()
        self.activation = get_activation(activation)
        self.fc1 = LinearBlock(input_dim, hidden_layer)
        self.fc2 = LinearBlock(hidden_layer, hidden_layer)
        self.fc3 = LinearBlock(hidden_layer, hidden_layer)
        self.fc4 = LinearBlock(hidden_layer, hidden_layer)
        self.fc5 = LinearBlock(hidden_layer, output_dim)

    def construct(self, *inputs):
        """fc network"""
        x = inputs[0]
        out = self.fc1(x)
        out = self.activation(out)
        out = self.fc2(out)
        out = self.activation(out)
        out = self.fc3(out)
        out = self.activation(out)
        out = self.fc4(out)
        out = self.activation(out)
        out = self.fc5(out)
        return out
