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
maxwell S11 model
"""

import mindspore.nn as nn


class S11Predictor(nn.Cell):
    """
    maxwell S11 model define
    """
    def __init__(self, input_dimension):
        super(S11Predictor, self).__init__()
        self.fc1 = nn.Dense(input_dimension, 128)
        self.fc2 = nn.Dense(128, 128)
        self.fc3 = nn.Dense(128, 128)
        self.fc4 = nn.Dense(128, 128)
        self.fc5 = nn.Dense(128, 128)
        self.fc6 = nn.Dense(128, 128)
        self.fc7 = nn.Dense(128, 1001)
        self.relu = nn.ReLU()

    def construct(self, x):
        """forward"""
        x0 = x
        x1 = self.relu(self.fc1(x0))
        x2 = self.relu(self.fc2(x1))
        x3 = self.relu(self.fc3(x1 + x2))
        x4 = self.relu(self.fc4(x1 + x2 + x3))
        x5 = self.relu(self.fc5(x1 + x2 + x3 + x4))
        x6 = self.relu(self.fc6(x1 + x2 + x3 + x4 + x5))
        x = self.fc7(x1 + x2 + x3 + x4 + x5 + x6)
        return x
