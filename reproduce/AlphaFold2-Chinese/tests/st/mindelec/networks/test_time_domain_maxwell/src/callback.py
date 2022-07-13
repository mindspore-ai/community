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
"""
call back functions
"""
import time
import copy

import numpy as np
from mindspore.train.callback import Callback
from mindspore.train.summary import SummaryRecord
from mindspore import Tensor
import mindspore.common.dtype as mstype

class PredictCallback(Callback):
    """
    Monitor the prediction accuracy in training.

    Args:
        model (Cell): Prediction network cell.
        inputs (Array): Input data of prediction.
        label (Array): Label data of prediction.
        config (dict): config info of prediction.
        visual_fn (dict): Visualization function. Default: None.
    """
    def __init__(self, model, inputs, label, config, visual_fn=None):
        super(PredictCallback, self).__init__()
        self.model = model
        self.inputs = inputs
        self.label = label
        self.label_shape = label.shape
        self.visual_fn = visual_fn
        self.vision_path = config.get("vision_path", "./vision")
        self.summary_dir = config.get("summary_path", "./summary")

        self.output_size = config.get("output_size", 3)
        self.input_size = config.get("input_size", 3)
        self.output_scale = np.array(config["output_scale"], dtype=np.float32)
        self.predict_interval = config.get("predict_interval", 10)
        self.batch_size = config.get("test_batch_size", 8192*4)

        self.dx = inputs[0, 1, 0, 0] - inputs[0, 0, 0, 0]
        self.dy = inputs[0, 0, 1, 1] - inputs[0, 0, 0, 1]
        self.dt = inputs[1, 0, 0, 2] - inputs[0, 0, 0, 2]
        print("check yee delta: {}, {}, {}".format(self.dx, self.dy, self.dt))

        self.ex_inputs = copy.deepcopy(inputs)
        self.ey_inputs = copy.deepcopy(inputs)
        self.hz_inputs = copy.deepcopy(inputs)
        self.ex_inputs = self.ex_inputs.reshape(-1, self.input_size)
        self.ey_inputs = self.ey_inputs.reshape(-1, self.input_size)
        self.hz_inputs = self.hz_inputs.reshape(-1, self.input_size)
        self.ex_inputs[:, 1] += self.dy / 2.0
        self.ex_inputs[:, 2] += self.dt / 2.0
        self.ey_inputs[:, 0] += self.dx / 2.0
        self.ey_inputs[:, 2] += self.dt / 2.0
        self.inputs_each = [self.ex_inputs, self.ey_inputs, self.hz_inputs]
        self._step_counter = 0
        self.l2_error = (1.0, 1.0, 1.0)

    def __enter__(self):
        self.summary_record = SummaryRecord(self.summary_dir)
        return self

    def __exit__(self, *exc_args):
        self.summary_record.close()

    def epoch_end(self, run_context):
        """
        Evaluate the model at the end of epoch.

        Args:
            run_context (RunContext): Context of the train running.
        """
        cb_params = run_context.original_args()
        if cb_params.cur_epoch_num % self.predict_interval == 0:
            # predict each quantity
            index = 0
            prediction_each = np.zeros(self.label_shape)
            prediction_each = prediction_each.reshape((-1, self.output_size))
            time_beg = time.time()
            while index < len(self.inputs_each[0]):
                index_end = min(index + self.batch_size, len(self.inputs_each[0]))
                for i in range(self.output_size):
                    test_batch = Tensor(self.inputs_each[i][index: index_end, :], mstype.float32)
                    predict = self.model(test_batch)
                    predict = predict.asnumpy()
                    prediction_each[index: index_end, i] = predict[:, i] * self.output_scale[i]
                index = index_end
            print("==================================================================================================")
            print("predict total time: {} s".format(time.time() - time_beg))
            prediction = prediction_each.reshape(self.label_shape)
            if self.visual_fn is not None:
                self.visual_fn(self.inputs, self.label, prediction, path=self.vision_path,
                               name="epoch" + str(cb_params.cur_epoch_num))

            label = self.label.reshape((-1, self.output_size))
            prediction = prediction.reshape((-1, self.output_size))
            self.l2_error = self._calculate_error(label, prediction)

    def _calculate_error(self, label, prediction):
        """calculate l2-error to evaluate accuracy"""
        self._step_counter += 1
        error = label - prediction
        l2_error_ex = np.sqrt(np.sum(np.square(error[..., 0]))) / np.sqrt(np.sum(np.square(label[..., 0])))
        l2_error_ey = np.sqrt(np.sum(np.square(error[..., 1]))) / np.sqrt(np.sum(np.square(label[..., 1])))
        l2_error_hz = np.sqrt(np.sum(np.square(error[..., 2]))) / np.sqrt(np.sum(np.square(label[..., 2])))
        print("l2_error, Ex: ", l2_error_ex, ", Ey: ", l2_error_ey, ", Hz: ", l2_error_hz)
        self.summary_record.add_value('scalar', 'l2_ex', Tensor(l2_error_ex))
        self.summary_record.add_value('scalar', 'l2_ey', Tensor(l2_error_ey))
        self.summary_record.add_value('scalar', 'l2_hz', Tensor(l2_error_hz))
        return l2_error_ex, l2_error_ey, l2_error_hz

    def get_l2_error(self):
        return self.l2_error
