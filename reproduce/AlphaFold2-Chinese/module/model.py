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
"""AlphaFold Model"""

import numpy as np

import mindspore.nn as nn
import mindspore.common.dtype as mstype
import mindspore.numpy as mnp
from mindspore.common.tensor import Tensor
from mindspore import Parameter
from mindspore.ops import functional as F

from commons import residue_constants
from commons.utils import get_chi_atom_indices, pseudo_beta_fn, dgram_from_positions, atom37_to_torsion_angles
from module.evoformer_module import TemplateEmbedding, EvoformerIteration
from module.structure_module import StructureModule, PredictedLDDTHead

class AlphaFold(nn.Cell):
    """AlphaFold Model"""
    def __init__(self, config, global_config):
        super(AlphaFold, self).__init__()
        self.config = config.model.embeddings_and_evoformer
        self.preprocess_1d = nn.Dense(22, self.config.msa_channel).to_float(mstype.float16)
        self.preprocess_msa = nn.Dense(49, self.config.msa_channel).to_float(mstype.float16)
        self.left_single = nn.Dense(22, self.config.pair_channel).to_float(mstype.float16)
        self.right_single = nn.Dense(22, self.config.pair_channel).to_float(mstype.float16)
        self.prev_pos_linear = nn.Dense(15, self.config.pair_channel).to_float(mstype.float16)
        self.pair_activations = nn.Dense(65, self.config.pair_channel).to_float(mstype.float16)
        self.prev_msa_first_row_norm = nn.LayerNorm([256,], epsilon=1e-5)
        self.prev_pair_norm = nn.LayerNorm([128,], epsilon=1e-5)
        self.one_hot = nn.OneHot(depth=self.config.max_relative_feature * 2 + 1, axis=-1)
        self.extra_msa_activations = nn.Dense(25, self.config.extra_msa_channel).to_float(mstype.float16)
        self.template_single_embedding = nn.Dense(57, self.config.msa_channel).to_float(mstype.float16)
        self.template_projection = nn.Dense(self.config.msa_channel, self.config.msa_channel).to_float(mstype.float16)
        self.single_activations = nn.Dense(self.config.msa_channel, self.config.seq_channel).to_float(mstype.float16)
        self.relu = nn.ReLU()
        self.recycle_pos = self.config.recycle_pos
        self.recycle_features = self.config.recycle_features
        self.template_enable = self.config.template.enabled
        self.max_relative_feature = self.config.max_relative_feature
        self.template_enabled = self.config.template.enabled
        self.template_embed_torsion_angles = self.config.template.embed_torsion_angles
        self.num_bins = self.config.prev_pos.num_bins
        self.min_bin = self.config.prev_pos.min_bin
        self.max_bin = self.config.prev_pos.max_bin
        self.extra_msa_one_hot = nn.OneHot(depth=23, axis=-1)
        self.template_aatype_one_hot = nn.OneHot(depth=22, axis=-1)
        self.template_embedding = TemplateEmbedding(self.config.template,
                                                    global_config.template_embedding.slice_num,
                                                    global_config=global_config)
        self.extra_msa_stack_iteration = EvoformerIteration(self.config.evoformer,
                                                            msa_act_dim=64,
                                                            pair_act_dim=128,
                                                            is_extra_msa=True,
                                                            batch_size=self.config.extra_msa_stack_num_block,
                                                            global_config=global_config)

        self.evoformer_iteration = EvoformerIteration(self.config.evoformer,
                                                      msa_act_dim=256,
                                                      pair_act_dim=128,
                                                      is_extra_msa=False,
                                                      batch_size=self.config.evoformer_num_block,
                                                      global_config=global_config)

        self.structure_module = StructureModule(config.model.heads.structure_module,
                                                self.config.seq_channel,
                                                self.config.pair_channel,
                                                global_config=global_config)

        self.module_lddt = PredictedLDDTHead(config.model.heads.predicted_lddt,
                                             global_config,
                                             self.config.seq_channel)
        self._init_tensor(global_config)

    def _init_tensor(self, global_config):
        "initialization of tensors and parameters"
        self.chi_atom_indices = Tensor(get_chi_atom_indices(), mstype.int32)
        chi_angles_mask = list(residue_constants.chi_angles_mask)
        chi_angles_mask.append([0.0, 0.0, 0.0, 0.0])
        self.chi_angles_mask = Tensor(chi_angles_mask, mstype.float32)
        self.mirror_psi_mask = Tensor(np.asarray([1., 1., -1., 1., 1., 1., 1.])[None, None, :, None], mstype.float32)
        self.chi_pi_periodic = Tensor(residue_constants.chi_pi_periodic, mstype.float32)

        indices0 = np.arange(4).reshape((-1, 1, 1, 1, 1)).astype("int64") # 4 batch
        indices0 = indices0.repeat(global_config.seq_length, axis=1) # seq_length sequence length
        indices0 = indices0.repeat(4, axis=2) # 4 chis
        self.indices0 = Tensor(indices0.repeat(4, axis=3)) # 4 atoms

        indices1 = np.arange(global_config.seq_length).reshape((1, -1, 1, 1, 1)).astype("int64")
        indices1 = indices1.repeat(4, axis=0)
        indices1 = indices1.repeat(4, axis=2)
        self.indices1 = Tensor(indices1.repeat(4, axis=3))

        self.idx_extra_msa_stack = Parameter(Tensor(0, mstype.int32), requires_grad=False)
        self.extra_msa_stack_num_block = self.config.extra_msa_stack_num_block

        self.idx_evoformer_block = Parameter(Tensor(0, mstype.int32), requires_grad=False)
        self.evoformer_num_block = Tensor(self.config.evoformer_num_block, mstype.int32)

    def construct(self, target_feat, msa_feat, msa_mask, seq_mask, aatype,
                  template_aatype, template_all_atom_masks, template_all_atom_positions,
                  template_mask, template_pseudo_beta_mask, template_pseudo_beta,
                  _, extra_msa, extra_has_deletion,
                  extra_deletion_value, extra_msa_mask,
                  atom14_atom_exists, atom37_atom_exists, residue_index,
                  prev_pos, prev_msa_first_row, prev_pair):
        """construct"""

        preprocess_1d = self.preprocess_1d(target_feat)
        preprocess_msa = self.preprocess_msa(msa_feat)
        msa_activations1 = mnp.expand_dims(preprocess_1d, axis=0) + preprocess_msa

        left_single = self.left_single(target_feat)
        right_single = self.right_single(target_feat)

        pair_activations = left_single[:, None] + right_single[None]
        mask_2d = seq_mask[:, None] * seq_mask[None, :]

        if self.recycle_pos:
            prev_pseudo_beta = pseudo_beta_fn(aatype, prev_pos, None)
            dgram = dgram_from_positions(prev_pseudo_beta, self.num_bins, self.min_bin, self.max_bin)
            pair_activations += self.prev_pos_linear(dgram)
        # return pair_activations, msa_activations1
        prev_msa_first_row = F.depend(prev_msa_first_row, pair_activations)
        if self.recycle_features:
            prev_msa_first_row = self.prev_msa_first_row_norm(prev_msa_first_row)
            msa_activations1 = mnp.concatenate(
                (mnp.expand_dims(prev_msa_first_row + msa_activations1[0, ...], 0),
                 msa_activations1[1:, ...]), 0)
            pair_activations += self.prev_pair_norm(prev_pair.astype(mstype.float32))

        if self.max_relative_feature:
            offset = residue_index[:, None] - residue_index[None, :]
            rel_pos = self.one_hot(mnp.clip(offset + self.max_relative_feature, 0, 2 * self.max_relative_feature))
            pair_activations += self.pair_activations(rel_pos)

        template_pair_representation = 0
        if self.template_enable:
            template_pair_representation = self.template_embedding(pair_activations, template_aatype,
                                                                   template_all_atom_masks, template_all_atom_positions,
                                                                   template_mask, template_pseudo_beta_mask,
                                                                   template_pseudo_beta, mask_2d)
            pair_activations += template_pair_representation

        msa_1hot = self.extra_msa_one_hot(extra_msa)
        extra_msa_feat = mnp.concatenate((msa_1hot, extra_has_deletion[..., None], extra_deletion_value[..., None]),
                                         axis=-1)
        extra_msa_activations = self.extra_msa_activations(extra_msa_feat)
        msa_act = extra_msa_activations
        pair_act = pair_activations

        msa_act = msa_act.astype(mstype.float32)
        pair_act = pair_act.astype(mstype.float32)
        extra_msa_mask = extra_msa_mask.astype(mstype.float32)
        mask_2d = mask_2d.astype(mstype.float32)

        self.idx_extra_msa_stack = 0
        idx_extra_msa_stack_int = 0
        while idx_extra_msa_stack_int < self.extra_msa_stack_num_block:
            msa_act, pair_act = \
            self.extra_msa_stack_iteration(msa_act, pair_act, extra_msa_mask, mask_2d, self.idx_extra_msa_stack)
            self.idx_extra_msa_stack += 1
            idx_extra_msa_stack_int += 1
            msa_act = F.depend(msa_act, self.idx_extra_msa_stack)
            pair_act = F.depend(pair_act, self.idx_extra_msa_stack)

        msa_activations2 = None
        if self.template_enabled and self.template_embed_torsion_angles:
            num_templ, num_res = template_aatype.shape
            aatype_one_hot = self.template_aatype_one_hot(template_aatype)
            torsion_angles_sin_cos, alt_torsion_angles_sin_cos, torsion_angles_mask = atom37_to_torsion_angles(
                template_aatype, template_all_atom_positions, template_all_atom_masks, self.chi_atom_indices,
                self.chi_angles_mask, self.mirror_psi_mask, self.chi_pi_periodic, self.indices0, self.indices1)
            template_features = mnp.concatenate([aatype_one_hot,
                                                 mnp.reshape(torsion_angles_sin_cos, [num_templ, num_res, 14]),
                                                 mnp.reshape(alt_torsion_angles_sin_cos, [num_templ, num_res, 14]),
                                                 torsion_angles_mask], axis=-1)
            template_activations = self.template_single_embedding(template_features)
            template_activations = self.relu(template_activations.astype(mstype.float32))
            template_activations = self.template_projection(template_activations)
            msa_activations2 = mnp.concatenate([msa_activations1, template_activations], axis=0)
            torsion_angle_mask = torsion_angles_mask[:, :, 2]
            torsion_angle_mask = torsion_angle_mask.astype(msa_mask.dtype)
            msa_mask = mnp.concatenate([msa_mask, torsion_angle_mask], axis=0)

        msa_activations2 = msa_activations2.astype(mstype.float16)
        pair_activations = pair_act.astype(mstype.float16)
        msa_mask = msa_mask.astype(mstype.float16)
        mask_2d = mask_2d.astype(mstype.float16)
        # return msa_activations2, pair_activations, msa_mask, mask_2d
        self.idx_evoformer_block = self.idx_evoformer_block * 0
        while self.idx_evoformer_block < self.evoformer_num_block:
            msa_activations2, pair_activations = \
            self.evoformer_iteration(msa_activations2,
                                     pair_activations,
                                     msa_mask,
                                     mask_2d,
                                     self.idx_evoformer_block)
            self.idx_evoformer_block += 1

        single_activations = self.single_activations(msa_activations2[0])
        msa_first_row = msa_activations2[0]

        # return single_activations, msa, msa_first_row
        final_atom_positions, final_atom_mask, rp_structure_module = \
            self.structure_module(single_activations,
                                  pair_activations,
                                  seq_mask,
                                  aatype,
                                  atom14_atom_exists,
                                  atom37_atom_exists)

        predicted_lddt_logits = self.module_lddt(rp_structure_module)

        prev_pos = final_atom_positions.astype(mstype.float16)
        prev_msa_first_row = msa_first_row.astype(mstype.float16)
        prev_pair = pair_activations.astype(mstype.float16)

        final_atom_positions = final_atom_positions.astype(mstype.float16)
        final_atom_mask = final_atom_mask.astype(mstype.float16)

        return final_atom_positions, final_atom_mask, predicted_lddt_logits, prev_pos, prev_msa_first_row, prev_pair
