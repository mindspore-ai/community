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

"""Evoformer module"""
import numpy as np
import mindspore.nn as nn
import mindspore.common.dtype as mstype
import mindspore.numpy as mnp
from mindspore.ops import operations as P
from mindspore.ops import functional as F
from mindspore.common.tensor import Tensor
from mindspore import Parameter

from commons import residue_constants
from commons.utils import dgram_from_positions, batch_make_transform_from_reference, batch_quat_affine, \
    batch_invert_point, batch_rot_to_quat
from module.basic_module import Attention, MSARowAttentionWithPairBias, MSAColumnAttention, MSAColumnGlobalAttention, \
    Transition, OuterProductMean, TriangleMultiplication, TriangleAttention
class EvoformerIteration(nn.Cell):
    '''evoformer iteration'''
    def __init__(self, config, msa_act_dim, pair_act_dim, is_extra_msa, batch_size, global_config):
        super(EvoformerIteration, self).__init__()
        self.config = config
        self.is_extra_msa = is_extra_msa
        if not self.is_extra_msa:
            self.msa_row_attention_with_pair_bias = MSARowAttentionWithPairBias(
                self.config.msa_row_attention_with_pair_bias, msa_act_dim, pair_act_dim, batch_size,
                global_config.evoformer_iteration.msa_row_attention_with_pair_bias.slice_num)
            self.attn_mod = MSAColumnAttention(self.config.msa_column_attention, msa_act_dim, batch_size,
                                               global_config.evoformer_iteration.msa_column_attention.slice_num)
            self.msa_transition = Transition(self.config.msa_transition, msa_act_dim, batch_size,
                                             global_config.evoformer_iteration.msa_transition.slice_num)
            self.outer_product_mean = OuterProductMean(self.config.outer_product_mean, msa_act_dim, pair_act_dim,
                                                       batch_size,
                                                       global_config.evoformer_iteration.outer_product_mean.slice_num)
            self.triangle_attention_starting_node = \
                TriangleAttention(self.config.triangle_attention_starting_node,
                                  pair_act_dim, batch_size,
                                  global_config.evoformer_iteration.triangle_attention_starting_node.slice_num)
            self.triangle_attention_ending_node = \
                TriangleAttention(self.config.triangle_attention_ending_node,
                                  pair_act_dim, batch_size,
                                  global_config.evoformer_iteration.triangle_attention_ending_node.slice_num)
            self.pair_transition = Transition(self.config.pair_transition, pair_act_dim, batch_size,
                                              global_config.evoformer_iteration.pair_transition.slice_num)
        else:
            self.msa_row_attention_with_pair_bias = MSARowAttentionWithPairBias(
                self.config.msa_row_attention_with_pair_bias, msa_act_dim, pair_act_dim, batch_size,
                global_config.extra_msa_stack.msa_row_attention_with_pair_bias.slice_num)
            self.attn_mod = \
                MSAColumnGlobalAttention(self.config.msa_column_attention, msa_act_dim, batch_size,
                                         global_config.extra_msa_stack.msa_column_global_attention.slice_num)
            self.msa_transition = Transition(self.config.msa_transition, msa_act_dim, batch_size,
                                             global_config.extra_msa_stack.msa_transition.slice_num)
            self.outer_product_mean = OuterProductMean(self.config.outer_product_mean, msa_act_dim, pair_act_dim,
                                                       batch_size,
                                                       global_config.extra_msa_stack.outer_product_mean.slice_num)
            self.triangle_attention_starting_node = \
                TriangleAttention(self.config.triangle_attention_starting_node,
                                  pair_act_dim, batch_size,
                                  global_config.extra_msa_stack.triangle_attention_starting_node.slice_num)
            self.triangle_attention_ending_node = \
                TriangleAttention(self.config.triangle_attention_ending_node,
                                  pair_act_dim, batch_size,
                                  global_config.extra_msa_stack.triangle_attention_ending_node.slice_num)
            self.pair_transition = Transition(self.config.pair_transition, pair_act_dim, batch_size,
                                              global_config.extra_msa_stack.pair_transition.slice_num)

        self.triangle_multiplication_outgoing = TriangleMultiplication(self.config.triangle_multiplication_outgoing,
                                                                       pair_act_dim, batch_size)
        self.triangle_multiplication_incoming = TriangleMultiplication(self.config.triangle_multiplication_incoming,
                                                                       pair_act_dim, batch_size)

    def construct(self, msa_act, pair_act, msa_mask, pair_mask, index):
        '''construct'''
        msa_act = msa_act + self.msa_row_attention_with_pair_bias(msa_act, msa_mask, pair_act, index)
        msa_act = msa_act + self.attn_mod(msa_act, msa_mask, index)
        msa_act = msa_act + self.msa_transition(msa_act, index)
        pair_act = pair_act + self.outer_product_mean(msa_act, msa_mask, index)
        pair_act = pair_act + self.triangle_multiplication_outgoing(pair_act, pair_mask, index)
        pair_act = pair_act + self.triangle_multiplication_incoming(pair_act, pair_mask, index)
        pair_act = pair_act + self.triangle_attention_starting_node(pair_act, pair_mask, index)
        pair_act = pair_act + self.triangle_attention_ending_node(pair_act, pair_mask, index)
        pair_act = pair_act + self.pair_transition(pair_act, index)
        return msa_act.astype(mstype.float16), pair_act.astype(mstype.float16)


class TemplatePairStack(nn.Cell):
    '''template pair stack'''
    def __init__(self, config, global_config=None):
        super(TemplatePairStack, self).__init__()
        self.config = config
        self.global_config = global_config
        self.num_block = self.config.num_block
        # self.seq_length = global_config.step_size

        self.triangle_attention_starting_node = \
            TriangleAttention(self.config.triangle_attention_starting_node,
                              64, self.num_block,
                              global_config.template_pair_stack.triangle_attention_starting_node.slice_num)
        self.triangle_attention_ending_node = \
            TriangleAttention(self.config.triangle_attention_ending_node,
                              64, self.num_block,
                              global_config.template_pair_stack.triangle_attention_ending_node.slice_num)
        # Hard Code
        self.pair_transition = Transition(self.config.pair_transition, 64, self.num_block,
                                          global_config.template_pair_stack.pair_transition.slice_num)
        self.triangle_multiplication_outgoing = TriangleMultiplication(self.config.triangle_multiplication_outgoing,
                                                                       layer_norm_dim=64, batch_size=self.num_block)
        self.triangle_multiplication_incoming = TriangleMultiplication(self.config.triangle_multiplication_incoming,
                                                                       layer_norm_dim=64, batch_size=self.num_block)

    def construct(self, pair_act, pair_mask, index):
        if not self.num_block:
            return pair_act

        pair_act = pair_act + self.triangle_attention_starting_node(pair_act, pair_mask, index)
        pair_act = pair_act + self.triangle_attention_ending_node(pair_act, pair_mask, index)
        pair_act = pair_act + self.triangle_multiplication_outgoing(pair_act, pair_mask, index)
        pair_act = pair_act + self.triangle_multiplication_incoming(pair_act, pair_mask, index)
        pair_act = pair_act + self.pair_transition(pair_act, index)
        return pair_act.astype(mstype.float16)


class SingleTemplateEmbedding(nn.Cell):
    '''single template embedding'''
    def __init__(self, config, global_config=None):
        super(SingleTemplateEmbedding, self).__init__()
        self.config = config
        # self.seq_length = global_config.step_size
        self.num_channels = (self.config.template_pair_stack.triangle_attention_ending_node.value_dim)
        self.embedding2d = nn.Dense(88, self.num_channels).to_float(mstype.float16)
        self.template_pair_stack = TemplatePairStack(self.config.template_pair_stack, global_config)
        self.num_bins = self.config.dgram_features.num_bins
        self.min_bin = self.config.dgram_features.min_bin
        self.max_bin = self.config.dgram_features.max_bin

        self.one_hot = nn.OneHot(depth=22, axis=-1)
        self.n, self.ca, self.c = [residue_constants.atom_order[a] for a in ('N', 'CA', 'C')]

        self.use_template_unit_vector = self.config.use_template_unit_vector
        layer_norm_dim = 64
        self.output_layer_norm = nn.LayerNorm([layer_norm_dim,], epsilon=1e-5)

        self.idx_num_block = Parameter(Tensor(0, mstype.int32), requires_grad=False)
        self.idx_batch_loop = Parameter(Tensor(0, mstype.int32), requires_grad=False)
        # self.num_block = Tensor(self.template_pair_stack.num_block, mstype.int32)
        # self.batch_block = Tensor(4, mstype.int32)
        self.num_block = self.template_pair_stack.num_block
        self.batch_block = 4
        self._act = Parameter(
            Tensor(np.zeros([global_config.seq_length, global_config.seq_length, 64]).astype(np.float16)),
            requires_grad=False)

    def construct(self, query_embedding, mask_2d, template_aatype, template_all_atom_masks, template_all_atom_positions,
                  template_pseudo_beta_mask, template_pseudo_beta):
        '''construct'''
        num_res = template_aatype[0, ...].shape[0]
        template_mask_2d_temp = P.Cast()(template_pseudo_beta_mask[:, :, None] * template_pseudo_beta_mask[:, None, :],
                                         query_embedding.dtype)
        template_dgram_temp = dgram_from_positions(template_pseudo_beta, self.num_bins, self.min_bin, self.max_bin)
        template_dgram_temp = P.Cast()(template_dgram_temp, query_embedding.dtype)

        to_concat_temp = (template_dgram_temp, template_mask_2d_temp[:, :, :, None])
        aatype_temp = self.one_hot(template_aatype)
        to_concat_temp = to_concat_temp + (mnp.tile(aatype_temp[:, None, :, :], (1, num_res, 1, 1)),
                                           mnp.tile(aatype_temp[:, :, None, :], (1, 1, num_res, 1)))
        rot_temp, trans_temp = batch_make_transform_from_reference(template_all_atom_positions[:, :, self.n],
                                                                   template_all_atom_positions[:, :, self.ca],
                                                                   template_all_atom_positions[:, :, self.c])

        _, rotation_tmp, translation_tmp = batch_quat_affine(
            batch_rot_to_quat(rot_temp, unstack_inputs=True), translation=trans_temp, rotation=rot_temp,
            unstack_inputs=True)
        points_tmp = mnp.expand_dims(translation_tmp, axis=-2)
        affine_vec_tmp = batch_invert_point(points_tmp, rotation_tmp, translation_tmp, extra_dims=1)
        inv_distance_scalar_tmp = P.Rsqrt()(1e-6 + mnp.sum(mnp.square(affine_vec_tmp), axis=1))
        template_mask_tmp = (template_all_atom_masks[:, :, self.n] *
                             template_all_atom_masks[:, :, self.ca] *
                             template_all_atom_masks[:, :, self.c])
        template_mask_2d_tmp = template_mask_tmp[:, :, None] * template_mask_tmp[:, None, :]

        inv_distance_scalar_tmp = inv_distance_scalar_tmp * template_mask_2d_tmp.astype(inv_distance_scalar_tmp.dtype)
        unit_vector_tmp = P.Transpose()((affine_vec_tmp * inv_distance_scalar_tmp[:, None, ...]), (0, 2, 3, 1))
        template_mask_2d_tmp = P.Cast()(template_mask_2d_tmp, query_embedding.dtype)
        if not self.use_template_unit_vector:
            unit_vector_tmp = mnp.zeros_like(unit_vector_tmp)
        to_concat_temp = to_concat_temp + (unit_vector_tmp, template_mask_2d_tmp[..., None],)
        act_tmp = mnp.concatenate(to_concat_temp, axis=-1)
        act_tmp = act_tmp * template_mask_2d_tmp[..., None]
        act_tmp = self.embedding2d(act_tmp)

        idx_batch_loop = self.idx_batch_loop
        output = []
        idx_batch_loop_int = 0
        self.idx_num_block = 0

        while idx_batch_loop_int < self.batch_block:
            self.idx_num_block = 0
            idx_num_block_int = 0
            self._act = P.Gather()(act_tmp, idx_batch_loop, 0)
            while idx_num_block_int < self.num_block:
                self._act = self.template_pair_stack(self._act, mask_2d, self.idx_num_block)
                self.idx_num_block += 1
                idx_num_block_int += 1
            temp_act = P.Reshape()(self._act, ((1,) + P.Shape()(self._act)))
            output.append(temp_act)
            idx_batch_loop += 1
            idx_batch_loop_int += 1

        act_tmp_loop = P.Concat()(output)
        act_tmp = self.output_layer_norm(act_tmp_loop.astype(mstype.float32))
        return act_tmp


class TemplateEmbedding(nn.Cell):
    '''template embedding'''
    def __init__(self, config, slice_num, global_config=None):
        super(TemplateEmbedding, self).__init__()
        self.config = config
        self.global_config = global_config
        self.num_channels = (self.config.template_pair_stack.triangle_attention_ending_node.value_dim)
        self.template_embedder = SingleTemplateEmbedding(self.config, self.global_config)
        self.template_pointwise_attention = Attention(self.config.attention, q_data_dim=128, m_data_dim=64,
                                                      output_dim=128)
        self.slice_num = slice_num
        if slice_num == 0:
            slice_num = 1
        self._flat_query_slice = Parameter(
            Tensor(np.zeros((int(global_config.seq_length * global_config.seq_length / slice_num), 1, 128)),
                   dtype=mstype.float16), requires_grad=False)
        self._flat_templates_slice = Parameter(
            Tensor(np.zeros((int(global_config.seq_length * global_config.seq_length / slice_num), 4, 64)),
                   dtype=mstype.float16), requires_grad=False)

    def construct(self, query_embedding, template_aatype, template_all_atom_masks, template_all_atom_positions,
                  template_mask, template_pseudo_beta_mask, template_pseudo_beta, mask_2d):
        '''construct'''
        num_templates = template_mask.shape[0]
        num_channels = self.num_channels
        num_res = query_embedding.shape[0]
        query_num_channels = query_embedding.shape[-1]
        template_mask = P.Cast()(template_mask, query_embedding.dtype)

        mask_2d = F.depend(mask_2d, query_embedding)
        template_pair_representation = self.template_embedder(query_embedding, mask_2d, template_aatype,
                                                              template_all_atom_masks, template_all_atom_positions,
                                                              template_pseudo_beta_mask,
                                                              template_pseudo_beta)

        template_pair_representation = template_pair_representation.astype(mstype.float32)
        flat_query = mnp.reshape(query_embedding, [num_res * num_res, 1, query_num_channels])
        flat_templates = mnp.reshape(
            mnp.transpose(template_pair_representation.astype(mstype.float16), [1, 2, 0, 3]),
            [num_res * num_res, num_templates, num_channels]).astype(mstype.float32)
        bias = (1e9 * (template_mask[None, None, None, :] - 1.))
        flat_query, flat_templates, bias = flat_query.astype(mstype.float32), flat_templates.astype(
            mstype.float32), bias.astype(mstype.float32)

        if self.slice_num:
            slice_shape = (self.slice_num, -1)
            flat_query_shape = P.Shape()(flat_query)
            flat_query = P.Reshape()(flat_query, slice_shape + flat_query_shape[1:]).astype(mstype.float16)
            flat_templates_shape = P.Shape()(flat_templates)
            flat_templates = P.Reshape()(flat_templates, slice_shape + flat_templates_shape[1:]).astype(mstype.float16)
            slice_idx = 0
            embedding_tuple = ()
            while slice_idx < self.slice_num:
                self._flat_query_slice = flat_query[slice_idx]
                self._flat_templates_slice = flat_templates[slice_idx]
                embedding_slice = self.template_pointwise_attention(self._flat_query_slice, self._flat_templates_slice,
                                                                    bias, index=None, nonbatched_bias=None)
                embedding_slice = P.Reshape()(embedding_slice, ((1,) + P.Shape()(embedding_slice)))
                embedding_tuple = embedding_tuple + (embedding_slice,)
                slice_idx += 1
            embedding = P.Concat()(embedding_tuple)

            embedding = embedding.astype(mstype.float32)
            embedding = mnp.reshape(embedding, [num_res, num_res, query_num_channels])
            # No gradients if no templates.
            template_mask = template_mask.astype(embedding.dtype)
            embedding = embedding * (mnp.sum(template_mask) > 0.).astype(embedding.dtype)
            return embedding

        embedding = self.template_pointwise_attention(flat_query, flat_templates, bias, index=None,
                                                      nonbatched_bias=None)
        embedding = embedding.astype(mstype.float32)
        embedding = mnp.reshape(embedding, [num_res, num_res, query_num_channels])
        # No gradients if no templates.
        template_mask = template_mask.astype(embedding.dtype)
        embedding = embedding * (mnp.sum(template_mask) > 0.).astype(embedding.dtype)
        return embedding
