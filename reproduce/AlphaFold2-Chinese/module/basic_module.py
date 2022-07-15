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

"""basic module"""

import mindspore.nn as nn
import mindspore.common.dtype as mstype
import mindspore.numpy as mnp
from mindspore.ops import operations as P
from mindspore.ops import functional as F
from mindspore.common.tensor import Tensor
from mindspore import Parameter
import numpy as np
from commons.utils import mask_mean


class Attention(nn.Cell):
    '''attention module'''
    def __init__(self, config, q_data_dim, m_data_dim, output_dim, batch_size=None):
        super(Attention, self).__init__()
        self.config = config
        self.q_data_dim = q_data_dim
        self.m_data_dim = m_data_dim
        self.output_dim = output_dim
        self.num_head = self.config.num_head
        self.gating = self.config.gating
        self.key_dim = self.config.get('key_dim', int(q_data_dim))
        self.value_dim = self.config.get('value_dim', int(m_data_dim))
        self.key_dim = self.key_dim // self.num_head
        self.value_dim = self.value_dim // self.num_head
        self.batch_size = batch_size
        self.matmul = P.MatMul(transpose_b=True)
        self.batch_matmul_trans_b = P.BatchMatMul(transpose_b=True)
        self.softmax = nn.Softmax()
        self.sigmoid = nn.Sigmoid()
        self.batch_size = batch_size
        self._init_parameter()

    def _init_parameter(self):
        '''init parameter'''
        if self.batch_size:
            self.linear_q_weights = Parameter(Tensor(np.zeros([self.batch_size, self.num_head * self.key_dim,
                                                               self.q_data_dim]), mstype.float32))
            self.linear_k_weights = Parameter(Tensor(np.zeros([self.batch_size, self.num_head * self.key_dim,
                                                               self.m_data_dim]), mstype.float32))
            self.linear_v_weights = Parameter(Tensor(np.zeros([self.batch_size, self.num_head * self.value_dim,
                                                               self.m_data_dim]), mstype.float32))
            self.linear_output_weights = Parameter(Tensor(np.zeros([self.batch_size, self.output_dim,
                                                                    self.num_head * self.value_dim]), mstype.float32))
            self.o_biases = Parameter(Tensor(np.zeros([self.batch_size, self.output_dim]), mstype.float32))
            if self.gating:
                self.linear_gating_weights = Parameter(Tensor(np.zeros([self.batch_size, self.num_head * self.value_dim,
                                                                        self.q_data_dim]), mstype.float32))
                self.gating_biases = Parameter(Tensor(np.zeros((self.batch_size, self.num_head, self.value_dim)),
                                                      mstype.float32), name="gating_b")
        else:
            self.linear_q_weights = Parameter(Tensor(np.zeros([self.num_head * self.key_dim, self.q_data_dim]),
                                                     mstype.float32))
            self.linear_k_weights = Parameter(Tensor(np.zeros([self.num_head * self.key_dim, self.m_data_dim]),
                                                     mstype.float32))
            self.linear_v_weights = Parameter(Tensor(np.zeros([self.num_head * self.value_dim, self.m_data_dim]),
                                                     mstype.float32))
            self.linear_output_weights = Parameter(Tensor(np.zeros([self.output_dim, self.num_head * self.value_dim]),
                                                          mstype.float32))
            self.o_biases = Parameter(Tensor(np.zeros([self.output_dim]), mstype.float32))
            if self.gating:
                self.linear_gating_weights = Parameter(Tensor(np.zeros([self.num_head * self.value_dim,
                                                                        self.q_data_dim]), mstype.float32))
                self.gating_biases = Parameter(Tensor(np.zeros((self.num_head, self.value_dim)), mstype.float32),
                                               name="gating_b")

    def construct(self, q_data, m_data, bias, index=None, nonbatched_bias=None):
        '''construct'''
        if self.batch_size:
            linear_q_weight = P.Gather()(self.linear_q_weights, index, 0)
            linear_k_weight = P.Gather()(self.linear_k_weights, index, 0)
            linear_v_weight = P.Gather()(self.linear_v_weights, index, 0)
            linear_output_weight = P.Gather()(self.linear_output_weights, index, 0)
            o_bias = P.Gather()(self.o_biases, index, 0)
            linear_gating_weight = 0
            gating_bias = 0
            if self.gating:
                linear_gating_weight = P.Gather()(self.linear_gating_weights, index, 0)
                gating_bias = P.Gather()(self.gating_biases, index, 0)
        else:
            linear_q_weight = self.linear_q_weights
            linear_k_weight = self.linear_k_weights
            linear_v_weight = self.linear_v_weights
            linear_output_weight = self.linear_output_weights
            o_bias = self.o_biases
            linear_gating_weight = 0
            gating_bias = 0
            if self.gating:
                linear_gating_weight = self.linear_gating_weights
                gating_bias = self.gating_biases

        q_data, m_data, bias = q_data.astype(mstype.float32), m_data.astype(mstype.float32), bias.astype(mstype.float32)
        dim_b, dim_q, dim_a = q_data.shape
        _, dim_k, dim_c = m_data.shape
        dim_h = self.num_head

        q_data = P.Reshape()(q_data, (-1, dim_a))
        m_data = P.Reshape()(m_data, (-1, dim_c))

        q = self.matmul(q_data.astype(mstype.float16), linear_q_weight.astype(mstype.float16)). \
                astype(mstype.float32) * self.key_dim ** (-0.5)
        k = self.matmul(m_data.astype(mstype.float16), linear_k_weight.astype(mstype.float16))
        v = self.matmul(m_data.astype(mstype.float16), linear_v_weight.astype(mstype.float16))

        q = P.Reshape()(q, (dim_b, dim_q, dim_h, -1))
        k = P.Reshape()(k, (dim_b, dim_k, dim_h, -1))
        v = P.Reshape()(v, (dim_b, dim_k, dim_h, -1))

        tmp_q = P.Reshape()(P.Transpose()(q.astype(mstype.float16), (0, 2, 1, 3)), (dim_b * dim_h, dim_q, -1))
        tmp_k = P.Reshape()(P.Transpose()(k.astype(mstype.float16), (0, 2, 1, 3)), (dim_b * dim_h, dim_k, -1))
        logits = P.Reshape()(self.batch_matmul_trans_b(tmp_q.astype(mstype.float16),
                                                       tmp_k.astype(mstype.float16)),
                             (dim_b, dim_h, dim_q, dim_k)) + bias.astype(mstype.float16)

        if nonbatched_bias is not None:
            logits += mnp.expand_dims(nonbatched_bias, axis=0)
        weights = self.softmax(logits.astype(mstype.float32))
        tmp_v = P.Reshape()(P.Transpose()(v, (0, 2, 3, 1)), (dim_b * dim_h, -1, dim_k))
        tmp_weights = P.Reshape()(weights, (dim_b * dim_h, dim_q, -1))
        weighted_avg = P.Transpose()(P.Reshape()(self.batch_matmul_trans_b(tmp_weights.astype(mstype.float16),
                                                                           tmp_v.astype(mstype.float16)),
                                                 (dim_b, dim_h, dim_q, -1)),
                                     (0, 2, 1, 3)).astype(mstype.float32)

        if self.gating:
            gate_values = P.Reshape()(
                self.matmul(q_data.astype(mstype.float16), linear_gating_weight.astype(mstype.float16)),
                (dim_b, dim_q, dim_h, -1)) + gating_bias[None, None, ...].astype(mstype.float16)
            gate_values = self.sigmoid(gate_values.astype(mstype.float32))
            weighted_avg = P.Reshape()(weighted_avg * gate_values, (dim_b * dim_q, -1))

        weighted_avg = P.Reshape()(weighted_avg, (dim_b * dim_q, -1))
        output = P.Reshape()(
            self.matmul(weighted_avg.astype(mstype.float16), linear_output_weight.astype(mstype.float16)),
            (dim_b, dim_q, -1)) + o_bias[None, ...].astype(mstype.float16)
        return output


class MSARowAttentionWithPairBias(nn.Cell):
    '''MSA row attention'''
    def __init__(self, config, msa_act_dim, pair_act_dim, batch_size=None, slice_num=0):
        super(MSARowAttentionWithPairBias, self).__init__()
        self.config = config
        self.num_head = self.config.num_head
        self.batch_size = batch_size
        self.norm = P.LayerNorm(begin_norm_axis=-1, begin_params_axis=-1, epsilon=1e-5)
        self.matmul = P.MatMul(transpose_b=True)
        self.attn_mod = Attention(self.config, msa_act_dim, msa_act_dim, msa_act_dim, batch_size)
        self.msa_act_dim = msa_act_dim
        self.pair_act_dim = pair_act_dim
        self.batch_size = batch_size
        self.slice_num = slice_num
        self.idx = Tensor(0, mstype.int32)
        self._init_parameter()

    def _init_parameter(self):
        '''init parameter'''
        self.query_norm_gammas = Parameter(Tensor(np.zeros([self.batch_size, self.msa_act_dim,]), mstype.float32))
        self.query_norm_betas = Parameter(Tensor(np.zeros([self.batch_size, self.msa_act_dim,]), mstype.float32))
        self.feat_2d_norm_gammas = Parameter(Tensor(np.zeros([self.batch_size, self.pair_act_dim,]), mstype.float32))
        self.feat_2d_norm_betas = Parameter(Tensor(np.zeros([self.batch_size, self.pair_act_dim,]), mstype.float32))
        self.feat_2d_weights = Parameter(
            Tensor(np.zeros([self.batch_size, self.num_head, self.pair_act_dim]), mstype.float32))

    def construct(self, msa_act, msa_mask, pair_act, index):
        '''construct'''
        query_norm_gamma = P.Gather()(self.query_norm_gammas, index, 0)
        query_norm_beta = P.Gather()(self.query_norm_betas, index, 0)
        feat_2d_norm_gamma = P.Gather()(self.feat_2d_norm_gammas, index, 0)
        feat_2d_norm_beta = P.Gather()(self.feat_2d_norm_betas, index, 0)
        feat_2d_weight = P.Gather()(self.feat_2d_weights, index, 0)

        q, k, _ = pair_act.shape
        bias = (1e9 * (msa_mask - 1.))[:, None, None, :]
        msa_act, _, _ = self.norm(msa_act.astype(mstype.float32), query_norm_gamma.astype(mstype.float32),
                                  query_norm_beta.astype(mstype.float32))
        pair_act, _, _ = self.norm(pair_act.astype(mstype.float32), feat_2d_norm_gamma.astype(mstype.float32),
                                   feat_2d_norm_beta.astype(mstype.float32))
        pair_act = P.Reshape()(pair_act, (-1, pair_act.shape[-1]))
        nonbatched_bias = P.Transpose()(
            P.Reshape()(self.matmul(pair_act.astype(mstype.float16), feat_2d_weight.astype(mstype.float16)),
                        (q, k, self.num_head)), (2, 0, 1))

        if self.slice_num:
            msa_act_ori_shape = P.Shape()(msa_act)
            slice_shape = (self.slice_num, -1) + msa_act_ori_shape[1:]
            msa_act = P.Reshape()(msa_act, slice_shape).astype(mstype.float16)
            bias_shape = P.Shape()(bias)
            bias = P.Reshape()(bias, slice_shape[:2] + bias_shape[1:])
            slice_idx = 0
            slice_idx_tensor = self.idx
            msa_act_tuple = ()

            msa_act_slice = P.Gather()(msa_act, slice_idx_tensor, 0)
            bias_slice = P.Gather()(bias, slice_idx_tensor, 0)
            msa_act_slice = self.attn_mod(msa_act_slice, msa_act_slice, bias_slice, index, nonbatched_bias)
            msa_act_slice = P.Reshape()(msa_act_slice, ((1,) + P.Shape()(msa_act_slice)))
            msa_act_tuple = msa_act_tuple + (msa_act_slice,)
            slice_idx += 1
            slice_idx_tensor += 1

            while slice_idx < self.slice_num:
                msa_act_slice = P.Gather()(msa_act, slice_idx_tensor, 0)
                msa_act_slice = F.depend(msa_act_slice, msa_act_tuple[-1])
                bias_slice = P.Gather()(bias, slice_idx_tensor, 0)
                msa_act_slice = self.attn_mod(msa_act_slice, msa_act_slice, bias_slice, index, nonbatched_bias)
                msa_act_slice = P.Reshape()(msa_act_slice, ((1,) + P.Shape()(msa_act_slice)))
                msa_act_tuple = msa_act_tuple + (msa_act_slice,)
                slice_idx += 1
                slice_idx_tensor += 1

            msa_act = P.Concat()(msa_act_tuple)
            msa_act = P.Reshape()(msa_act, msa_act_ori_shape)
            return msa_act

        msa_act = self.attn_mod(msa_act, msa_act, bias, index, nonbatched_bias)
        return msa_act


class MSAColumnAttention(nn.Cell):
    '''MSA column attention'''
    def __init__(self, config, msa_act_dim, batch_size=None, slice_num=0):
        super(MSAColumnAttention, self).__init__()
        self.config = config
        self.query_norm = P.LayerNorm(begin_norm_axis=-1, begin_params_axis=-1, epsilon=1e-5)
        self.attn_mod = Attention(self.config, msa_act_dim, msa_act_dim, msa_act_dim, batch_size)
        self.batch_size = batch_size
        self.slice_num = slice_num
        self.msa_act_dim = msa_act_dim
        self.idx = Tensor(0, mstype.int32)
        self._init_parameter()

    def _init_parameter(self):
        self.query_norm_gammas = Parameter(Tensor(np.zeros([self.batch_size, self.msa_act_dim]), mstype.float32))
        self.query_norm_betas = Parameter(Tensor(np.zeros([self.batch_size, self.msa_act_dim]), mstype.float32))

    def construct(self, msa_act, msa_mask, index):
        '''construct'''
        query_norm_gamma = P.Gather()(self.query_norm_gammas, index, 0)
        query_norm_beta = P.Gather()(self.query_norm_betas, index, 0)
        msa_act = mnp.swapaxes(msa_act, -2, -3)
        msa_mask = mnp.swapaxes(msa_mask, -1, -2)
        bias = (1e9 * (msa_mask - 1.))[:, None, None, :]
        msa_act, _, _ = self.query_norm(msa_act.astype(mstype.float32), query_norm_gamma.astype(mstype.float32),
                                        query_norm_beta.astype(mstype.float32))
        if self.slice_num:
            msa_act_ori_shape = P.Shape()(msa_act)
            slice_shape = (self.slice_num, -1) + msa_act_ori_shape[1:]
            msa_act = P.Reshape()(msa_act, slice_shape).astype(mstype.float16)
            bias_shape = P.Shape()(bias)
            bias = P.Reshape()(bias, slice_shape[:2] + bias_shape[1:])

            slice_idx = 0
            slice_idx_tensor = self.idx
            msa_act_tuple = ()

            msa_act_slice = P.Gather()(msa_act, slice_idx_tensor, 0)
            bias_slice = P.Gather()(bias, slice_idx_tensor, 0)
            msa_act_slice = self.attn_mod(msa_act_slice, msa_act_slice, bias_slice, index)
            msa_act_slice = P.Reshape()(msa_act_slice, ((1,) + P.Shape()(msa_act_slice)))
            msa_act_tuple = msa_act_tuple + (msa_act_slice,)
            slice_idx += 1
            slice_idx_tensor += 1

            while slice_idx < self.slice_num:
                msa_act_slice = P.Gather()(msa_act, slice_idx_tensor, 0)
                msa_act_slice = F.depend(msa_act_slice, msa_act_tuple[-1])
                bias_slice = P.Gather()(bias, slice_idx_tensor, 0)
                msa_act_slice = self.attn_mod(msa_act_slice, msa_act_slice, bias_slice, index)
                msa_act_slice = P.Reshape()(msa_act_slice, ((1,) + P.Shape()(msa_act_slice)))
                msa_act_tuple = msa_act_tuple + (msa_act_slice,)
                slice_idx += 1
                slice_idx_tensor += 1

            msa_act = P.Concat()(msa_act_tuple)
            msa_act = P.Reshape()(msa_act, msa_act_ori_shape)
            msa_act = mnp.swapaxes(msa_act, -2, -3)
            return msa_act

        msa_act = self.attn_mod(msa_act, msa_act, bias, index)
        msa_act = mnp.swapaxes(msa_act, -2, -3)
        return msa_act


class GlobalAttention(nn.Cell):
    '''global attention'''
    def __init__(self, config, key_dim, value_dim, output_dim, batch_size=None):
        super(GlobalAttention, self).__init__()
        self.config = config
        self.key_dim = key_dim
        self.ori_key_dim = key_dim
        self.value_dim = value_dim
        self.ori_value_dim = value_dim
        self.num_head = self.config.num_head
        self.key_dim = self.key_dim // self.num_head
        self.value_dim = self.value_dim // self.num_head
        self.output_dim = output_dim
        self.matmul_trans_b = P.MatMul(transpose_b=True)
        self.batch_matmul = P.BatchMatMul()
        self.batch_matmul_trans_b = P.BatchMatMul(transpose_b=True)
        self.matmul = P.MatMul()
        self.softmax = nn.Softmax()
        self.sigmoid = nn.Sigmoid()
        self.gating = self.config.gating

        self.batch_size = batch_size
        self._init_parameter()

    def _init_parameter(self):
        '''init parameter'''
        self.linear_q_weights = Parameter(
            Tensor(np.zeros((self.batch_size, self.ori_key_dim, self.num_head, self.key_dim)), mstype.float32))
        self.linear_k_weights = Parameter(
            Tensor(np.zeros((self.batch_size, self.ori_value_dim, self.key_dim)), mstype.float32))
        self.linear_v_weights = Parameter(
            Tensor(np.zeros((self.batch_size, self.ori_value_dim, self.value_dim)), mstype.float32))
        self.linear_output_weights = Parameter(
            Tensor(np.zeros((self.batch_size, self.output_dim, self.num_head * self.value_dim)), mstype.float32))
        self.o_biases = Parameter(Tensor(np.zeros((self.batch_size, self.output_dim)), mstype.float32))
        if self.gating:
            self.linear_gating_weights = Parameter(
                Tensor(np.zeros((self.batch_size, self.num_head * self.value_dim, self.ori_key_dim)), mstype.float32))
            self.gating_biases = Parameter(Tensor(np.zeros((self.batch_size, self.ori_key_dim)), mstype.float32))

    def construct(self, q_data, m_data, q_mask, bias, index):
        '''construct'''
        q_weights = P.Gather()(self.linear_q_weights, index, 0)
        k_weights = P.Gather()(self.linear_k_weights, index, 0)
        v_weights = P.Gather()(self.linear_v_weights, index, 0)
        output_weights = P.Gather()(self.linear_output_weights, index, 0)
        output_bias = P.Gather()(self.o_biases, index, 0)
        gating_weights = 0
        gating_bias = 0
        if self.gating:
            gating_weights = P.Gather()(self.linear_gating_weights, index, 0)
            gating_bias = P.Gather()(self.gating_biases, index, 0)
        b, _, _ = m_data.shape
        v_weights = v_weights[None, ...]
        v_weights = mnp.broadcast_to(v_weights, (b, self.value_dim * self.num_head, self.value_dim))
        v = self.batch_matmul(m_data.astype(mstype.float16), v_weights.astype(mstype.float16))
        q_avg = mask_mean(q_mask, q_data, axis=1)
        q_weights = P.Reshape()(q_weights, (-1, self.num_head * self.key_dim))
        q = P.Reshape()(self.matmul(q_avg.astype(mstype.float16), q_weights.astype(mstype.float16)),
                        (-1, self.num_head, self.key_dim)) * (self.key_dim ** (-0.5))

        k_weights = k_weights[None, ...]
        k_weights = mnp.broadcast_to(k_weights, (b, self.value_dim * self.num_head, self.key_dim))

        k = self.batch_matmul(m_data.astype(mstype.float16), k_weights.astype(mstype.float16))

        bias = (1e9 * (q_mask[:, None, :, 0] - 1.))

        logits = self.batch_matmul_trans_b(q.astype(mstype.float16), k.astype(mstype.float16)) + bias.astype(
            mstype.float16)
        weights = self.softmax(logits.astype(mstype.float32))
        weighted_avg = self.batch_matmul(weights.astype(mstype.float16), v.astype(mstype.float16))

        if self.gating:
            # gate_values = self.linear_gating(q_data).astype(mstype.float32)
            q_data_shape = P.Shape()(q_data)
            if len(q_data_shape) != 2:
                q_data = P.Reshape()(q_data, (-1, q_data_shape[-1]))
            out_shape = q_data_shape[:-1] + (-1,)
            gate_values = P.Reshape()(self.matmul_trans_b(q_data.astype(mstype.float16),
                                                          gating_weights.astype(mstype.float16)) +
                                      gating_bias.astype(mstype.float16), out_shape)

            gate_values = P.Reshape()(self.sigmoid(gate_values.astype(mstype.float32)),
                                      (b, -1, self.num_head, self.value_dim))
            weighted_avg = P.Reshape()(weighted_avg[:, None] * gate_values, (-1, self.num_head * self.value_dim))
            weighted_avg_shape = P.Shape()(weighted_avg)
            if len(weighted_avg_shape) != 2:
                weighted_avg = P.Reshape()(weighted_avg, (-1, weighted_avg_shape[-1]))
            output = P.Reshape()(self.matmul_trans_b(weighted_avg.astype(mstype.float16),
                                                     output_weights.astype(mstype.float16))
                                 + output_bias.astype(mstype.float16), (b, -1, self.output_dim))

        else:
            weighted_avg = P.Reshape()(weighted_avg, (-1, self.num_head * self.value_dim))
            # output = self.linear_gating(weighted_avg)
            weighted_avg_shape = P.Shape()(weighted_avg)
            if len(weighted_avg_shape) != 2:
                weighted_avg = P.Reshape()(weighted_avg, (-1, weighted_avg_shape[-1]))
            out_shape = weighted_avg_shape[:-1] + (-1,)
            output = P.Reshape()(self.matmul_trans_b(weighted_avg.astype(mstype.float16),
                                                     output_weights.astype(mstype.float16)) +
                                 output_bias.astype(mstype.float16), out_shape)
            output = output[:, None]
        return output


class MSAColumnGlobalAttention(nn.Cell):
    '''MSA column global attention'''
    def __init__(self, config, msa_act_dim, batch_size=None, slice_num=0):
        super(MSAColumnGlobalAttention, self).__init__()
        self.config = config
        self.attn_mod = GlobalAttention(self.config, msa_act_dim, msa_act_dim, msa_act_dim, batch_size)
        self.query_norm = P.LayerNorm(begin_norm_axis=-1, begin_params_axis=-1, epsilon=1e-5)
        self.batch_size = batch_size
        self.slice_num = slice_num
        self.msa_act_dim = msa_act_dim
        self.idx = Tensor(0, mstype.int32)
        self._init_parameter()

    def _init_parameter(self):
        '''init parameter'''
        self.query_norm_gammas = Parameter(Tensor(np.zeros((self.batch_size, self.msa_act_dim)), mstype.float32))
        self.query_norm_betas = Parameter(Tensor(np.zeros((self.batch_size, self.msa_act_dim)), mstype.float32))

    def construct(self, msa_act, msa_mask, index):
        '''construct'''
        query_norm_gamma = P.Gather()(self.query_norm_gammas, index, 0)
        query_norm_beta = P.Gather()(self.query_norm_betas, index, 0)
        msa_act = mnp.swapaxes(msa_act, -2, -3)
        msa_mask = mnp.swapaxes(msa_mask, -1, -2)
        bias = (1e9 * (msa_mask - 1.))[:, None, None, :]
        msa_act, _, _ = self.query_norm(msa_act.astype(mstype.float32),
                                        query_norm_gamma.astype(mstype.float32),
                                        query_norm_beta.astype(mstype.float32))
        msa_mask = mnp.expand_dims(msa_mask, axis=-1)

        if self.slice_num:
            msa_act_ori_shape = P.Shape()(msa_act)
            slice_shape = (self.slice_num, -1) + msa_act_ori_shape[1:]
            msa_act = P.Reshape()(msa_act, slice_shape).astype(mstype.float16)
            bias_shape = P.Shape()(bias)
            bias = P.Reshape()(bias, slice_shape[:2] + bias_shape[1:])
            msa_mask_shape = P.Shape()(msa_mask)
            msa_mask = P.Reshape()(msa_mask, slice_shape[:2] + msa_mask_shape[1:])

            slice_idx = 0
            slice_idx_tensor = self.idx
            msa_act_tuple = ()

            msa_act_slice = P.Gather()(msa_act, slice_idx_tensor, 0)
            msa_mask_slice = P.Gather()(msa_mask, slice_idx_tensor, 0)
            bias_slice = P.Gather()(bias, slice_idx_tensor, 0)
            msa_act_slice = self.attn_mod(msa_act_slice, msa_act_slice, msa_mask_slice, bias_slice, index)
            msa_act_slice = P.Reshape()(msa_act_slice, ((1,) + P.Shape()(msa_act_slice)))
            msa_act_tuple = msa_act_tuple + (msa_act_slice,)
            slice_idx += 1
            slice_idx_tensor += 1

            while slice_idx < self.slice_num:
                msa_act_slice = P.Gather()(msa_act, slice_idx_tensor, 0)
                msa_act_slice = F.depend(msa_act_slice, msa_act_tuple[-1])
                msa_mask_slice = P.Gather()(msa_mask, slice_idx_tensor, 0)
                bias_slice = P.Gather()(bias, slice_idx_tensor, 0)

                msa_act_slice = self.attn_mod(msa_act_slice, msa_act_slice, msa_mask_slice, bias_slice, index)
                msa_act_slice = P.Reshape()(msa_act_slice, ((1,) + P.Shape()(msa_act_slice)))
                msa_act_tuple = msa_act_tuple + (msa_act_slice,)
                slice_idx += 1
                slice_idx_tensor += 1

            msa_act = P.Concat()(msa_act_tuple)
            msa_act = P.Reshape()(msa_act, msa_act_ori_shape)
            msa_act = mnp.swapaxes(msa_act, -2, -3)
            return msa_act

        msa_act = self.attn_mod(msa_act, msa_act, msa_mask, bias, index)
        msa_act = mnp.swapaxes(msa_act, -2, -3)
        return msa_act


class Transition(nn.Cell):
    '''transition'''
    def __init__(self, config, layer_norm_dim, batch_size=None, slice_num=0):
        super(Transition, self).__init__()
        self.config = config
        self.input_layer_norm = P.LayerNorm(begin_norm_axis=-1, begin_params_axis=-1, epsilon=1e-5)
        self.matmul = P.MatMul(transpose_b=True)
        self.layer_norm_dim = layer_norm_dim
        self.num_intermediate = int(layer_norm_dim * self.config.num_intermediate_factor)
        self.batch_size = batch_size
        self.slice_num = slice_num
        self.relu = nn.ReLU()
        self.idx = Tensor(0, mstype.int32)
        self._init_parameter()

    def _init_parameter(self):
        '''init parameter'''
        self.input_layer_norm_gammas = Parameter(
            Tensor(np.zeros((self.batch_size, self.layer_norm_dim)), mstype.float32))
        self.input_layer_norm_betas = Parameter(
            Tensor(np.zeros((self.batch_size, self.layer_norm_dim)), mstype.float32))
        self.transition1_weights = Parameter(
            Tensor(np.zeros((self.batch_size, self.num_intermediate, self.layer_norm_dim)), mstype.float32))
        self.transition1_biases = Parameter(Tensor(np.zeros((self.batch_size, self.num_intermediate)), mstype.float32))
        self.transition2_weights = Parameter(
            Tensor(np.zeros((self.batch_size, self.layer_norm_dim, self.num_intermediate)), mstype.float32))
        self.transition2_biases = Parameter(Tensor(np.zeros((self.batch_size, self.layer_norm_dim)), mstype.float32))

    def construct(self, act, index):
        '''construct'''
        input_layer_norm_gamma = P.Gather()(self.input_layer_norm_gammas, index, 0)
        input_layer_norm_beta = P.Gather()(self.input_layer_norm_betas, index, 0)
        transition1_weight = P.Gather()(self.transition1_weights, index, 0)
        transition1_bias = P.Gather()(self.transition1_biases, index, 0)
        transition2_weight = P.Gather()(self.transition2_weights, index, 0)
        transition2_bias = P.Gather()(self.transition2_biases, index, 0)
        act, _, _ = self.input_layer_norm(act.astype(mstype.float32), input_layer_norm_gamma.astype(mstype.float32),
                                          input_layer_norm_beta.astype(mstype.float32))
        if self.slice_num:
            act_ori_shape = P.Shape()(act)
            slice_shape = (self.slice_num, -1) + act_ori_shape[1:]
            act = P.Reshape()(act, slice_shape).astype(mstype.float16)

            slice_idx = 0
            slice_idx_tensor = self.idx
            act_tuple = ()

            act_slice = P.Gather()(act, slice_idx_tensor, 0)
            act_shape = P.Shape()(act_slice)
            if len(act_shape) != 2:
                act_slice = P.Reshape()(act_slice, (-1, act_shape[-1]))
            act_slice = self.relu(
                P.BiasAdd()(self.matmul(act_slice.astype(mstype.float16), transition1_weight.astype(mstype.float16)),
                            transition1_bias.astype(mstype.float16)).astype(mstype.float32))
            act_slice = P.BiasAdd()(
                self.matmul(act_slice.astype(mstype.float16), transition2_weight.astype(mstype.float16)),
                transition2_bias.astype(mstype.float16))
            act_slice = P.Reshape()(act_slice, act_shape)
            act_slice = P.Reshape()(act_slice, ((1,) + P.Shape()(act_slice)))
            act_tuple = act_tuple + (act_slice,)
            slice_idx += 1
            slice_idx_tensor += 1

            while slice_idx < self.slice_num:
                act_slice = P.Gather()(act, slice_idx_tensor, 0)
                act_slice = F.depend(act_slice, act_tuple[-1])
                act_shape = P.Shape()(act_slice)
                if len(act_shape) != 2:
                    act_slice = P.Reshape()(act_slice, (-1, act_shape[-1]))
                act_slice = self.relu(P.BiasAdd()(
                    self.matmul(act_slice.astype(mstype.float16), transition1_weight.astype(mstype.float16)),
                    transition1_bias.astype(mstype.float16)).astype(mstype.float32))
                act_slice = P.BiasAdd()(
                    self.matmul(act_slice.astype(mstype.float16), transition2_weight.astype(mstype.float16)),
                    transition2_bias.astype(mstype.float16))
                act_slice = P.Reshape()(act_slice, act_shape)
                act_slice = P.Reshape()(act_slice, ((1,) + P.Shape()(act_slice)))
                act_tuple = act_tuple + (act_slice,)
                slice_idx += 1
                slice_idx_tensor += 1

            act = P.Concat()(act_tuple)
            act = P.Reshape()(act, act_ori_shape)
            return act

        act_shape = P.Shape()(act)
        if len(act_shape) != 2:
            act = P.Reshape()(act, (-1, act_shape[-1]))
        act = self.relu(
            P.BiasAdd()(self.matmul(act.astype(mstype.float16), transition1_weight.astype(mstype.float16)),
                        transition1_bias.astype(mstype.float16)).astype(mstype.float32))
        act = P.BiasAdd()(self.matmul(act.astype(mstype.float16), transition2_weight.astype(mstype.float16)),
                          transition2_bias.astype(mstype.float16))
        act = P.Reshape()(act, act_shape)
        return act


class OuterProductMean(nn.Cell):
    '''outerproduct mean'''
    def __init__(self, config, act_dim, num_output_channel, batch_size=None, slice_num=0):
        super(OuterProductMean, self).__init__()
        self.num_output_channel = num_output_channel
        self.config = config
        self.layer_norm_input = P.LayerNorm(begin_norm_axis=-1, begin_params_axis=-1, epsilon=1e-5)
        self.matmul_trans_b = P.MatMul(transpose_b=True)
        self.matmul = P.MatMul()
        self.batch_matmul_trans_b = P.BatchMatMul(transpose_b=True)
        self.act_dim = act_dim
        self.batch_size = batch_size
        self.slice_num = slice_num
        self.idx = Tensor(0, mstype.int32)
        self._init_parameter()

    def _init_parameter(self):
        '''init parameter'''
        self.layer_norm_input_gammas = Parameter(Tensor(np.zeros((self.batch_size, self.act_dim)), mstype.float32))
        self.layer_norm_input_betas = Parameter(Tensor(np.zeros((self.batch_size, self.act_dim)), mstype.float32))
        self.left_projection_weights = Parameter(
            Tensor(np.zeros((self.batch_size, self.config.num_outer_channel, self.act_dim)), mstype.float32))
        self.left_projection_biases = Parameter(
            Tensor(np.zeros((self.batch_size, self.config.num_outer_channel)), mstype.float32))
        self.right_projection_weights = Parameter(
            Tensor(np.zeros((self.batch_size, self.config.num_outer_channel, self.act_dim)), mstype.float32))
        self.right_projection_biases = Parameter(
            Tensor(np.zeros((self.batch_size, self.config.num_outer_channel)), mstype.float32))
        self.linear_output_weights = Parameter(Tensor(np.zeros(
            (self.batch_size, self.num_output_channel, self.config.num_outer_channel *
             self.config.num_outer_channel)), mstype.float32))
        self.o_biases = Parameter(Tensor(np.zeros((self.batch_size, self.num_output_channel)), mstype.float32))

    def construct(self, act, mask, index):
        '''construct'''
        layer_norm_input_gamma = P.Gather()(self.layer_norm_input_gammas, index, 0)
        layer_norm_input_beta = P.Gather()(self.layer_norm_input_betas, index, 0)
        left_projection_weight = P.Gather()(self.left_projection_weights, index, 0)
        left_projection_bias = P.Gather()(self.left_projection_biases, index, 0)
        right_projection_weight = P.Gather()(self.right_projection_weights, index, 0)
        right_projection_bias = P.Gather()(self.right_projection_biases, index, 0)
        linear_output_weight = P.Gather()(self.linear_output_weights, index, 0)
        linear_output_bias = P.Gather()(self.o_biases, index, 0)
        mask = mask[..., None]
        act, _, _ = self.layer_norm_input(act.astype(mstype.float32),
                                          layer_norm_input_gamma.astype(mstype.float32),
                                          layer_norm_input_beta.astype(mstype.float32))
        act_shape = P.Shape()(act)
        if len(act_shape) != 2:
            act = P.Reshape()(act, (-1, act_shape[-1]))
        out_shape = act_shape[:-1] + (-1,)
        left_act = mask * P.Reshape()(P.BiasAdd()(self.matmul_trans_b(act.astype(mstype.float16),
                                                                      left_projection_weight.astype(mstype.float16)),
                                                  left_projection_bias.astype(mstype.float16)), out_shape)
        right_act = mask * P.Reshape()(P.BiasAdd()(self.matmul_trans_b(act.astype(mstype.float16),
                                                                       right_projection_weight.astype(mstype.float16)),
                                                   right_projection_bias.astype(mstype.float16)), out_shape)
        _, d, e = right_act.shape
        if self.slice_num:
            left_act_shape = P.Shape()(left_act)
            slice_shape = (left_act_shape[0],) + (self.slice_num, -1) + (left_act_shape[-1],)
            left_act = P.Reshape()(left_act, slice_shape)
            slice_idx = 0
            slice_idx_tensor = self.idx
            act_tuple = ()
            left_act_slice = P.Gather()(left_act, slice_idx_tensor, 1)
            a, b, c = left_act_slice.shape
            left_act_slice = P.Reshape()(mnp.transpose(left_act_slice.astype(mstype.float16), [2, 1, 0]), (-1, a))
            right_act = P.Reshape()(right_act, (a, -1))
            act_slice = P.Reshape()(P.Transpose()(P.Reshape()(self.matmul(left_act_slice.astype(mstype.float16),
                                                                          right_act.astype(mstype.float16)),
                                                              (c, b, d, e)), (2, 1, 0, 3)), (d, b, c * e))
            act_slice_shape = P.Shape()(act_slice)
            if len(act_shape) != 2:
                act_slice = P.Reshape()(act_slice, (-1, act_slice_shape[-1]))
            act_slice = P.Reshape()(P.BiasAdd()(self.matmul_trans_b(act_slice.astype(mstype.float16),
                                                                    linear_output_weight.astype(mstype.float16)),
                                                linear_output_bias.astype(mstype.float16)), (d, b, -1))
            act_slice = mnp.transpose(act_slice.astype(mstype.float16), [1, 0, 2])
            act_slice = P.Reshape()(act_slice, ((1,) + P.Shape()(act_slice)))
            act_tuple = act_tuple + (act_slice,)
            slice_idx += 1
            slice_idx_tensor += 1
            while slice_idx < self.slice_num:
                left_act_slice = P.Gather()(left_act, slice_idx_tensor, 1)
                left_act_slice = F.depend(left_act_slice, act_tuple[-1])
                a, b, c = left_act_slice.shape
                left_act_slice = P.Reshape()(mnp.transpose(left_act_slice.astype(mstype.float16), [2, 1, 0]), (-1, a))
                right_act = P.Reshape()(right_act, (a, -1))
                act_slice = P.Reshape()(P.Transpose()(P.Reshape()(self.matmul(left_act_slice.astype(mstype.float16),
                                                                              right_act.astype(mstype.float16)),
                                                                  (c, b, d, e)), (2, 1, 0, 3)), (d, b, c * e))
                act_slice_shape = P.Shape()(act_slice)
                if len(act_shape) != 2:
                    act_slice = P.Reshape()(act_slice, (-1, act_slice_shape[-1]))
                act_slice = P.Reshape()(P.BiasAdd()(self.matmul_trans_b(act_slice.astype(mstype.float16),
                                                                        linear_output_weight.astype(mstype.float16)),
                                                    linear_output_bias.astype(mstype.float16)), (d, b, -1))
                act_slice = mnp.transpose(act_slice.astype(mstype.float16), [1, 0, 2])
                act_slice = P.Reshape()(act_slice, ((1,) + P.Shape()(act_slice)))
                act_tuple = act_tuple + (act_slice,)
                slice_idx += 1
                slice_idx_tensor += 1
            act = P.Concat()(act_tuple)
            act_shape = P.Shape()(act)
            act = P.Reshape()(act, (-1, act_shape[-2], act_shape[-1]))
            epsilon = 1e-3
            tmp_mask = P.Transpose()(mask.astype(mstype.float16), (2, 1, 0))
            norm = P.Transpose()(self.batch_matmul_trans_b(tmp_mask.astype(mstype.float16),
                                                           tmp_mask.astype(mstype.float16)),
                                 (1, 2, 0)).astype(mstype.float32)
            act /= epsilon + norm
            return act

        a, b, c = left_act.shape
        left_act = P.Reshape()(mnp.transpose(left_act.astype(mstype.float16), [2, 1, 0]), (-1, a))
        right_act = P.Reshape()(right_act, (a, -1))
        act = P.Reshape()(P.Transpose()(P.Reshape()(self.matmul(left_act.astype(mstype.float16),
                                                                right_act.astype(mstype.float16)),
                                                    (c, b, d, e)), (2, 1, 0, 3)), (d, b, c * e))
        act_shape = P.Shape()(act)
        if len(act_shape) != 2:
            act = P.Reshape()(act, (-1, act_shape[-1]))
        act = P.Reshape()(P.BiasAdd()(self.matmul_trans_b(act.astype(mstype.float16),
                                                          linear_output_weight.astype(mstype.float16)),
                                      linear_output_bias.astype(mstype.float16)), (d, b, -1))
        act = mnp.transpose(act.astype(mstype.float16), [1, 0, 2])
        epsilon = 1e-3
        tmp_mask = P.Transpose()(mask.astype(mstype.float16), (2, 1, 0))
        norm = P.Transpose()(self.batch_matmul_trans_b(tmp_mask.astype(mstype.float16),
                                                       tmp_mask.astype(mstype.float16)),
                             (1, 2, 0)).astype(mstype.float32)
        act /= epsilon + norm
        return act

class TriangleMultiplication(nn.Cell):
    '''triangle multiplication'''
    def __init__(self, config, layer_norm_dim, batch_size):
        super(TriangleMultiplication, self).__init__()
        self.config = config
        self.layer_norm = P.LayerNorm(begin_norm_axis=-1, begin_params_axis=-1, epsilon=1e-5)
        self.matmul = P.MatMul(transpose_b=True)
        self.sigmoid = nn.Sigmoid()
        self.batch_matmul_trans_b = P.BatchMatMul(transpose_b=True)
        equation = ["ikc,jkc->ijc", "kjc,kic->ijc"]
        if self.config.equation not in equation:
            print("TriangleMultiplication Not Suppl")
        if self.config.equation == "ikc,jkc->ijc":
            self.equation = True
        elif self.config.equation == "kjc,kic->ijc":
            self.equation = False
        else:
            self.equation = None
        self.batch_size = batch_size
        self.layer_norm_dim = layer_norm_dim
        self._init_parameter()

    def _init_parameter(self):
        '''init parameter'''
        self.layer_norm_input_gammas = Parameter(
            Tensor(np.zeros((self.batch_size, self.layer_norm_dim)), mstype.float32))
        self.layer_norm_input_betas = Parameter(
            Tensor(np.zeros((self.batch_size, self.layer_norm_dim)), mstype.float32))
        self.left_projection_weights = Parameter(
            Tensor(np.zeros((self.batch_size, self.config.num_intermediate_channel, self.layer_norm_dim)),
                   mstype.float32))
        self.left_projection_biases = Parameter(
            Tensor(np.zeros((self.batch_size, self.config.num_intermediate_channel)), mstype.float32))
        self.right_projection_weights = Parameter(
            Tensor(np.zeros((self.batch_size, self.config.num_intermediate_channel, self.layer_norm_dim)),
                   mstype.float32))
        self.right_projection_biases = Parameter(
            Tensor(np.zeros((self.batch_size, self.config.num_intermediate_channel)), mstype.float32))
        self.left_gate_weights = Parameter(
            Tensor(np.zeros((self.batch_size, self.config.num_intermediate_channel, self.layer_norm_dim)),
                   mstype.float32))
        self.left_gate_biases = Parameter(
            Tensor(np.zeros((self.batch_size, self.config.num_intermediate_channel)), mstype.float32))
        self.right_gate_weights = Parameter(
            Tensor(np.zeros((self.batch_size, self.config.num_intermediate_channel, self.layer_norm_dim)),
                   mstype.float32))
        self.right_gate_biases = Parameter(
            Tensor(np.zeros((self.batch_size, self.config.num_intermediate_channel)), mstype.float32))
        self.center_layer_norm_gammas = Parameter(
            Tensor(np.zeros((self.batch_size, self.layer_norm_dim)), mstype.float32))
        self.center_layer_norm_betas = Parameter(
            Tensor(np.zeros((self.batch_size, self.layer_norm_dim)), mstype.float32))
        self.output_projection_weights = Parameter(
            Tensor(np.zeros((self.batch_size, self.layer_norm_dim, self.layer_norm_dim)), mstype.float32))
        self.output_projection_biases = Parameter(
            Tensor(np.zeros((self.batch_size, self.layer_norm_dim)), mstype.float32))
        self.gating_linear_weights = Parameter(
            Tensor(np.zeros((self.batch_size, self.layer_norm_dim, self.layer_norm_dim)), mstype.float32))
        self.gating_linear_biases = Parameter(Tensor(np.zeros((self.batch_size, self.layer_norm_dim)), mstype.float32))

    def construct(self, act, mask, index):
        '''construct'''
        layer_norm_input_gamma = P.Gather()(self.layer_norm_input_gammas, index, 0)
        layer_norm_input_beta = P.Gather()(self.layer_norm_input_betas, index, 0)
        left_projection_weight = P.Gather()(self.left_projection_weights, index, 0)
        left_projection_bias = P.Gather()(self.left_projection_biases, index, 0)
        right_projection_weight = P.Gather()(self.right_projection_weights, index, 0)
        right_projection_bias = P.Gather()(self.right_projection_biases, index, 0)
        left_gate_weight = P.Gather()(self.left_gate_weights, index, 0)
        left_gate_bias = P.Gather()(self.left_gate_biases, index, 0)
        right_gate_weight = P.Gather()(self.right_gate_weights, index, 0)
        right_gate_bias = P.Gather()(self.right_gate_biases, index, 0)
        center_layer_norm_gamma = P.Gather()(self.center_layer_norm_gammas, index, 0)
        center_layer_norm_beta = P.Gather()(self.center_layer_norm_betas, index, 0)
        output_projection_weight = P.Gather()(self.output_projection_weights, index, 0)
        output_projection_bias = P.Gather()(self.output_projection_biases, index, 0)
        gating_linear_weight = P.Gather()(self.gating_linear_weights, index, 0)
        gating_linear_bias = P.Gather()(self.gating_linear_biases, index, 0)

        mask = mask[..., None]
        act, _, _ = self.layer_norm(act.astype(mstype.float32),
                                    layer_norm_input_gamma.astype(mstype.float32),
                                    layer_norm_input_beta.astype(mstype.float32))
        input_act = act
        act_shape = P.Shape()(act)
        if len(act_shape) != 2:
            act = P.Reshape()(act, (-1, act_shape[-1]))
        out_shape = act_shape[:-1] + (-1,)
        left_projection = mask * P.Reshape()(
            P.BiasAdd()(self.matmul(act.astype(mstype.float16), left_projection_weight.astype(mstype.float16)),
                        left_projection_bias.astype(mstype.float16)), out_shape)
        left_projection = left_projection.astype(mstype.float16)
        act = F.depend(act, left_projection)

        left_gate_values = self.sigmoid(P.Reshape()(
            P.BiasAdd()(self.matmul(act.astype(mstype.float16), left_gate_weight.astype(mstype.float16)),
                        left_gate_bias.astype(mstype.float16)), out_shape).astype(mstype.float32))
        left_proj_act = left_projection * left_gate_values
        act = F.depend(act, left_proj_act)

        right_projection = mask * P.Reshape()(
            P.BiasAdd()(self.matmul(act.astype(mstype.float16), right_projection_weight.astype(mstype.float16)),
                        right_projection_bias.astype(mstype.float16)), out_shape)
        right_projection = right_projection.astype(mstype.float16)
        act = F.depend(act, right_projection)

        right_gate_values = self.sigmoid(P.Reshape()(
            P.BiasAdd()(self.matmul(act.astype(mstype.float16), right_gate_weight.astype(mstype.float16)),
                        right_gate_bias.astype(mstype.float16)), out_shape).astype(mstype.float32))
        right_proj_act = right_projection * right_gate_values
        left_proj_act = F.depend(left_proj_act, right_proj_act)

        if self.equation is not None:
            if self.equation:
                left_proj_act_tmp = P.Transpose()(left_proj_act.astype(mstype.float16), (2, 0, 1))
                right_proj_act_tmp = P.Transpose()(right_proj_act.astype(mstype.float16), (2, 0, 1))
                act = self.batch_matmul_trans_b(left_proj_act_tmp, right_proj_act_tmp)
                act = P.Transpose()(act, (1, 2, 0)).astype(mstype.float32)
            else:
                left_proj_act_tmp = P.Transpose()(left_proj_act.astype(mstype.float16), (2, 1, 0))
                right_proj_act_tmp = P.Transpose()(right_proj_act.astype(mstype.float16), (2, 1, 0))
                act = self.batch_matmul_trans_b(left_proj_act_tmp, right_proj_act_tmp)
                act = P.Transpose()(act, (2, 1, 0)).astype(mstype.float32)
        act, _, _ = self.layer_norm(act.astype(mstype.float32),
                                    center_layer_norm_gamma.astype(mstype.float32),
                                    center_layer_norm_beta.astype(mstype.float32))
        act_shape = P.Shape()(act)
        if len(act_shape) != 2:
            act = P.Reshape()(act, (-1, act_shape[-1]))
        out_shape = act_shape[:-1] + (-1,)
        act = P.Reshape()(
            P.BiasAdd()(self.matmul(act.astype(mstype.float16), output_projection_weight.astype(mstype.float16)),
                        output_projection_bias.astype(mstype.float16)), out_shape)
        input_act_shape = P.Shape()(input_act)
        if len(input_act_shape) != 2:
            input_act = P.Reshape()(input_act, (-1, input_act_shape[-1]))
        out_shape = input_act_shape[:-1] + (-1,)
        gate_values = self.sigmoid(P.Reshape()(
            P.BiasAdd()(self.matmul(input_act.astype(mstype.float16), gating_linear_weight.astype(mstype.float16)),
                        gating_linear_bias.astype(mstype.float16)), out_shape).astype(mstype.float32))
        act = act * gate_values
        return act


class TriangleAttention(nn.Cell):
    '''triangle attention'''
    def __init__(self, config, layer_norm_dim, batch_size=None, slice_num=0):
        super(TriangleAttention, self).__init__()
        self.config = config
        self.orientation_is_per_column = (self.config.orientation == 'per_column')
        self.init_factor = Tensor(1. / np.sqrt(layer_norm_dim), mstype.float32)
        self.query_norm = P.LayerNorm(begin_norm_axis=-1, begin_params_axis=-1, epsilon=1e-5)
        self.matmul = P.MatMul(transpose_b=True)
        self.attn_mod = Attention(self.config, layer_norm_dim, layer_norm_dim, layer_norm_dim, batch_size)
        self.batch_size = batch_size
        self.slice_num = slice_num
        self.layer_norm_dim = layer_norm_dim
        self.idx = Tensor(0, mstype.int32)
        self._init_parameter()

    def _init_parameter(self):
        '''init parameter'''
        self.query_norm_gammas = Parameter(Tensor(np.zeros((self.batch_size, self.layer_norm_dim)), mstype.float32))
        self.query_norm_betas = Parameter(Tensor(np.zeros((self.batch_size, self.layer_norm_dim)), mstype.float32))
        self.feat_2d_weights = Parameter(
            Tensor(np.zeros((self.batch_size, self.config.num_head, self.layer_norm_dim)), mstype.float32))

    def construct(self, pair_act, pair_mask, index):
        '''construct'''
        query_norm_gamma = P.Gather()(self.query_norm_gammas, index, 0)
        query_norm_beta = P.Gather()(self.query_norm_betas, index, 0)
        feat_2d_weight = P.Gather()(self.feat_2d_weights, index, 0)
        if self.orientation_is_per_column:
            pair_act = mnp.swapaxes(pair_act, -2, -3)
            pair_mask = mnp.swapaxes(pair_mask, -1, -2)
        bias = (1e9 * (pair_mask - 1.))[:, None, None, :]
        pair_act, _, _ = self.query_norm(pair_act.astype(mstype.float32),
                                         query_norm_gamma.astype(mstype.float32),
                                         query_norm_beta.astype(mstype.float32))
        q, k, _ = pair_act.shape
        nonbatched_bias = self.matmul(P.Reshape()(pair_act.astype(mstype.float16), (-1, pair_act.shape[-1])),
                                      feat_2d_weight.astype(mstype.float16))
        nonbatched_bias = P.Transpose()(P.Reshape()(nonbatched_bias, (q, k, -1)), (2, 0, 1))
        if self.slice_num:
            pair_act_ori_shape = P.Shape()(pair_act)
            slice_shape = (self.slice_num, -1) + pair_act_ori_shape[1:]
            pair_act = P.Reshape()(pair_act, slice_shape).astype(mstype.float16)
            bias_shape = P.Shape()(bias)
            bias = P.Reshape()(bias, slice_shape[:2] + bias_shape[1:])

            slice_idx = 0
            slice_idx_tensor = self.idx
            pair_act_tuple = ()

            pair_act_slice = P.Gather()(pair_act, slice_idx_tensor, 0)
            bias_slice = P.Gather()(bias, slice_idx_tensor, 0)
            pair_act_slice = self.attn_mod(pair_act_slice, pair_act_slice, bias_slice, index, nonbatched_bias)
            pair_act_slice = P.Reshape()(pair_act_slice, ((1,) + P.Shape()(pair_act_slice)))
            pair_act_tuple = pair_act_tuple + (pair_act_slice,)
            slice_idx += 1
            slice_idx_tensor += 1

            while slice_idx < self.slice_num:
                pair_act_slice = P.Gather()(pair_act, slice_idx_tensor, 0)
                pair_act_slice = F.depend(pair_act_slice, pair_act_tuple[-1])
                bias_slice = P.Gather()(bias, slice_idx_tensor, 0)
                pair_act_slice = self.attn_mod(pair_act_slice, pair_act_slice, bias_slice, index, nonbatched_bias)
                pair_act_slice = P.Reshape()(pair_act_slice, ((1,) + P.Shape()(pair_act_slice)))
                pair_act_tuple = pair_act_tuple + (pair_act_slice,)
                slice_idx += 1
                slice_idx_tensor += 1
            pair_act = P.Concat()(pair_act_tuple)
            pair_act = P.Reshape()(pair_act, pair_act_ori_shape)

            if self.orientation_is_per_column:
                pair_act = mnp.swapaxes(pair_act, -2, -3)
            return pair_act

        pair_act = self.attn_mod(pair_act, pair_act, bias, index, nonbatched_bias)
        if self.orientation_is_per_column:
            pair_act = mnp.swapaxes(pair_act, -2, -3)
        return pair_act
