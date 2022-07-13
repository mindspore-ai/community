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
"""visualization of field quantities"""
import os

import copy
import io
import cv2
import PIL
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size


plt.rcParams['figure.dpi'] = 300

def visual_result(input_data, label, predict, path, name):
    """visulization of original field and normalized field"""
    input_data = copy.deepcopy(input_data)
    label = copy.deepcopy(label)
    predict = copy.deepcopy(predict)
    visual(input_data, label, predict, path, name)

    # normalize
    ex_min = label[:, :, :, 0].min()
    ex_max = label[:, :, :, 0].max()
    ey_min = label[:, :, :, 1].min()
    ey_max = label[:, :, :, 1].max()
    hz_min = label[:, :, :, 2].min()
    hz_max = label[:, :, :, 2].max()
    if ex_min == ex_max:
        ex_min = ex_min - 1
        ex_max = ex_max + 1
    if ey_min == ey_max:
        ey_min = ey_min - 1
        ey_max = ey_max + 1
    if hz_min == hz_max:
        hz_min = hz_min - 1
        hz_max = hz_max + 1

    label[:, :, :, 0] = 2 * (label[:, :, :, 0] - np.mean([ex_max, ex_min])) / (ex_max - ex_min)
    label[:, :, :, 1] = 2 * (label[:, :, :, 1] - np.mean([ey_max, ey_min])) / (ey_max - ey_min)
    label[:, :, :, 2] = 2 * (label[:, :, :, 2] - np.mean([hz_max, hz_min])) / (hz_max - hz_min)

    predict[:, :, :, 0] = 2 * (predict[:, :, :, 0] - np.mean([ex_max, ex_min])) / (ex_max - ex_min)
    predict[:, :, :, 1] = 2 * (predict[:, :, :, 1] - np.mean([ey_max, ey_min])) / (ey_max - ey_min)
    predict[:, :, :, 2] = 2 * (predict[:, :, :, 2] - np.mean([hz_max, hz_min])) / (hz_max - hz_min)
    visual(input_data, label, predict, path, str(name) + "_normlize")

def visual(input_data, label, predict, path, name):
    """visulization of ex/ey/hz"""
    [sample_t, sample_x, sample_y, _] = np.shape(input_data)

    # 将label、predict归一化
    ex_vmin, ex_vmax = np.percentile(label[:, :, :, 0], [0.5, 99.5])
    ey_vmin, ey_vmax = np.percentile(label[:, :, :, 1], [0.5, 99.5])
    hz_vmin, hz_vmax = np.percentile(label[:, :, :, 2], [0.5, 99.5])

    vmin_list = [ex_vmin, ey_vmin, hz_vmin]
    vmax_list = [ex_vmax, ey_vmax, hz_vmax]

    mean_abs_ex_label = 1.0
    mean_abs_ey_label = 1.0
    mean_abs_hz_label = 1.0

    output_names = ["Ex", "Ey", "Hz"]

    if not os.path.isdir(path):
        os.makedirs(path)

    fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
    fps = 10
    size = (1920, 1440)
    video = cv2.VideoWriter(os.path.join(path, "EH_" + str(name) + ".avi"), fourcc, fps, size)

    t_set = []
    if sample_t < 100:
        t_set = np.arange(sample_t, dtype=np.int32)
    else:
        for t in range(sample_t):
            if t % int(sample_t / 20) == 0 or t == sample_t - 1:
                t_set.append(t)

    for t in t_set:
        ex_label = label[t, :, :, 0]
        ey_label = label[t, :, :, 1]
        hz_label = label[t, :, :, 2]

        ex_predict = predict[t, :, :, 0]
        ey_predict = predict[t, :, :, 1]
        hz_predict = predict[t, :, :, 2]

        ex_label_2d = np.reshape(np.array(ex_label), (sample_x, sample_y))
        ey_label_2d = np.reshape(np.array(ey_label), (sample_x, sample_y))
        hz_label_2d = np.reshape(np.array(hz_label), (sample_x, sample_y))

        ex_predict_2d = np.reshape(np.array(ex_predict), (sample_x, sample_y))
        ey_predict_2d = np.reshape(np.array(ey_predict), (sample_x, sample_y))
        hz_predict_2d = np.reshape(np.array(hz_predict), (sample_x, sample_y))

        ex_error_2d = np.abs(ex_predict_2d - ex_label_2d) / mean_abs_ex_label
        ey_error_2d = np.abs(ey_predict_2d - ey_label_2d) / mean_abs_ey_label
        hz_error_2d = np.abs(hz_predict_2d - hz_label_2d) / mean_abs_hz_label

        label_2d = [ex_label_2d, ey_label_2d, hz_label_2d]
        predict_2d = [ex_predict_2d, ey_predict_2d, hz_predict_2d]
        error_2d = [ex_error_2d, ey_error_2d, hz_error_2d]

        lpe_2d = [label_2d, predict_2d, error_2d]
        lpe_names = ["label", "predict", "error"]

        fig = plt.figure()

        gs = gridspec.GridSpec(3, 3)

        title = "t={:d}".format(t)
        plt.suptitle(title, fontsize=14)

        gs_idx = int(0)

        for i, data_2d in enumerate(lpe_2d):
            for j, data in enumerate(data_2d):
                ax = fig.add_subplot(gs[gs_idx])
                gs_idx += 1

                if lpe_names[i] == "error":
                    img = ax.imshow(data.T, vmin=0, vmax=1,
                                    cmap=plt.get_cmap("jet"), origin='lower')
                else:
                    img = ax.imshow(data.T, vmin=vmin_list[j], vmax=vmax_list[j],
                                    cmap=plt.get_cmap("jet"), origin='lower')

                ax.set_title(output_names[j] + " " + lpe_names[i], fontsize=4)
                plt.xticks(size=4)
                plt.yticks(size=4)

                aspect = 20
                pad_fraction = 0.5
                divider = make_axes_locatable(ax)
                width = axes_size.AxesY(ax, aspect=1/aspect)
                pad = axes_size.Fraction(pad_fraction, width)
                cax = divider.append_axes("right", size=width, pad=pad)
                cb = plt.colorbar(img, cax=cax)
                cb.ax.tick_params(labelsize=4)

        gs.tight_layout(fig, pad=0.4, w_pad=0.4, h_pad=0.4)

        # save image to memory buffer
        buffer_ = io.BytesIO()
        fig.savefig(buffer_, format="jpg")
        buffer_.seek(0)
        image = PIL.Image.open(buffer_)

        video.write(np.asarray(image))

        buffer_.close()

        plt.close()

    video.release()
