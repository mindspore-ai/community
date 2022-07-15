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
"""metrics"""

import numpy as np
import mindspore.nn as nn
from mindspore.ops import functional as F

class MyMSELoss(nn.LossBase):
    """mse loss function"""
    def construct(self, base, target):
        bs, _, _, _, _ = F.shape(target)
        x = F.square(base - target)
        return 2*bs*self.get_loss(x)


class EvalMetric(nn.Metric):
    """eval metric"""

    def __init__(self, length):
        super(EvalMetric, self).__init__()
        self.clear()
        self.length = length

    def clear(self):
        self.error_sum_l2_error = 0
        self.error_mean_l1_error = 0

    def update(self, *inputs):
        test_predict = self._convert_data(inputs[0])
        test_label = self._convert_data(inputs[1])

        for i in range(len(test_label)):
            self.error_mean_l1_error += np.mean(np.abs(test_label[i] - test_predict[i]))

    def eval(self):
        return {'mean_l1_error': self.error_mean_l1_error / self.length}
