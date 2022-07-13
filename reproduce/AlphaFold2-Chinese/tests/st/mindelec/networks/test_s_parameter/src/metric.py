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

import os
import shutil
import mindspore.nn as nn
from mindspore.ops import functional as F
import matplotlib.pyplot as plt
import numpy as np
import cv2

class MyMSELoss(nn.LossBase):
    """mse loss function"""
    def construct(self, base, target):
        x = F.square(base - target)
        return self.get_loss(x)


class EvalMetric(nn.Metric):
    """
    eval metric
    """

    def __init__(self, scale_s11, length, frequency, show_pic_number, file_path):
        super(EvalMetric, self).__init__()
        self.clear()
        self.scale_s11 = scale_s11
        self.length = length
        self.frequency = frequency
        self.show_pic_number = show_pic_number
        self.file_path = file_path
        self.show_pic_id = np.random.choice(length, self.show_pic_number, replace=False)

        if not os.path.exists(self.file_path):
            os.mkdir(self.file_path)
        else:
            shutil.rmtree(self.file_path)
            os.mkdir(self.file_path)

    def clear(self):
        """
        clear error
        """
        self.error_sum_l2_error = 0
        self.error_sum_loss_error = 0
        self.pic_res = None
        self.index = 0

    def update(self, *inputs):
        """
        update error
        """

        y_pred = self._convert_data(inputs[0])
        y_label = self._convert_data(inputs[1])

        test_predict, test_label = y_pred, y_label
        test_predict[:, :] = test_predict[:, :] * self.scale_s11
        test_label[:, :] = test_label[:, :] * self.scale_s11
        test_predict[:, :] = 1.0 - np.power(10, test_predict[:, :])
        test_label[:, :] = 1.0 - np.power(10, test_label[:, :])
        self.pic_res = []

        for i in range(len(test_label)):
            self.index += 1
            predict_real_temp = test_predict[i]
            label_real_temp = test_label[i]
            l2_error_temp = np.sqrt(np.sum(np.square(label_real_temp - predict_real_temp))) / \
                            np.sqrt(np.sum(np.square(label_real_temp)))
            self.error_sum_l2_error += l2_error_temp
            self.error_sum_loss_error += np.mean((label_real_temp - predict_real_temp) ** 2)

            s11_label, s11_predict = label_real_temp, predict_real_temp
            plt.figure(dpi=250)
            plt.plot(self.frequency, s11_predict, '-', label='AI Model', linewidth=2)
            plt.plot(self.frequency, s11_label, '--', label='CST', linewidth=1)
            plt.title('s11(dB)')
            plt.xlabel('frequency(GHz) l2_s11:' + str(l2_error_temp)[:10])
            plt.ylabel('dB')
            plt.legend()
            plt.savefig(self.file_path + '/' + str(self.index) + '_' + str(l2_error_temp)[:10] + '.jpg')
            plt.close()
            if i in self.show_pic_id:
                self.pic_res.append(cv2.imread(
                    self.file_path + '/' + str(i) + '_' + str(l2_error_temp)[:10] + '.jpg'))

        self.pic_res = np.array(self.pic_res).astype(np.float32)

    def eval(self):
        """
        compute final error
        """
        return {'l2_error': self.error_sum_l2_error / self.length,
                'loss_error': self.error_sum_loss_error / self.length,
                'pic_res': self.pic_res}
