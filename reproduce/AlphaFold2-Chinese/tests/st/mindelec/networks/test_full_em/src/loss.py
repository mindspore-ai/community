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
loss
"""

import numpy as np
import mindspore.nn as nn
from mindspore.ops import functional as F
from src.config import config


class MyMSELoss(nn.LossBase):
    """mse loss function"""
    def construct(self, base, target):
        bs, _, _, _, _ = F.shape(target)
        x = F.square(base - target)
        return 2*bs*self.get_loss(x)


class EvaLMetric(nn.Metric):
    """eval  metric"""
    def __init__(self, length, scale, batch_size):
        super(EvaLMetric, self).__init__()
        self.clear()
        self.length = length
        self.batch_size = batch_size
        self.t = config.t_solution
        self.x = config.x_solution
        self.y = config.y_solution
        self.z = config.z_solution
        self.predict_real = np.zeros((self.length*self.t, self.x, self.y, self.z, 6), dtype=np.float32)
        self.label_real = np.zeros((self.length*self.t, self.x, self.y, self.z, 6), dtype=np.float32)
        self.scale = scale
        self.iter_idx = 0

    def clear(self):
        """clear"""
        self.iter_idx = 0

    def update(self, *inputs):
        """update"""
        y_pred = self._convert_data(inputs[0])
        y = self._convert_data(inputs[1])

        predict, label = y_pred, y
        self.predict_real[self.iter_idx*self.batch_size: self.iter_idx*self.batch_size + label.shape[0]] = predict
        self.label_real[self.iter_idx*self.batch_size: self.iter_idx*self.batch_size + label.shape[0]] = label
        self.iter_idx += 1

    def eval(self):
        """eval"""
        predict_real = np.reshape(self.predict_real, (self.length, self.t, self.x, self.y, self.z, 6))
        label_real = np.reshape(self.label_real, (self.length, self.t, self.x, self.y, self.z, 6))
        l2_time = 0.0
        for i in range(self.length):
            predict_real_temp = predict_real[i:i+1]
            label_real_temp = label_real[i:i+1]
            for j in range(self.t):
                predict_real_temp[0, j, :, :, :, 0] = predict_real_temp[0, j, :, :, :, 0] * self.scale[0][j]
                predict_real_temp[0, j, :, :, :, 1] = predict_real_temp[0, j, :, :, :, 1] * self.scale[1][j]
                predict_real_temp[0, j, :, :, :, 2] = predict_real_temp[0, j, :, :, :, 2] * self.scale[2][j]
                predict_real_temp[0, j, :, :, :, 3] = predict_real_temp[0, j, :, :, :, 3] * self.scale[3][j]
                predict_real_temp[0, j, :, :, :, 4] = predict_real_temp[0, j, :, :, :, 4] * self.scale[4][j]
                predict_real_temp[0, j, :, :, :, 5] = predict_real_temp[0, j, :, :, :, 5] * self.scale[5][j]
            l2_time += (np.sqrt(np.sum(np.square(label_real_temp - predict_real_temp))) /
                        np.sqrt(np.sum(np.square(label_real_temp))))
        return {'l2_error': l2_time / self.length}
