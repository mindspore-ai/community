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

"""structure module"""
import numpy as np
import mindspore.ops as ops
import mindspore.common.dtype as mstype
import mindspore.numpy as mnp
from mindspore import Parameter, ms_function, Tensor
from mindspore import nn
from commons import residue_constants
from commons.utils import generate_new_affine, to_tensor, from_tensor, vecs_to_tensor, atom14_to_atom37, \
    get_exp_atom_pos, get_exp_frames, pre_compose, scale_translation, to_tensor_new, l2_normalize, \
    torsion_angles_to_frames, frames_and_literature_positions_to_atom14_pos, apply_to_point, _invert_point

class InvariantPointAttention(nn.Cell):
    """Invariant Point attention module."""

    def __init__(self, config, global_config, pair_dim):
        """Initialize.

        Args:
          config: Structure Module Config
          global_config: Global Config of Model.
          pair_dim: pair representation dimension.
        """

        super().__init__()

        self._dist_epsilon = 1e-8
        self.config = config
        self.num_head = config.num_head
        self.num_scalar_qk = config.num_scalar_qk
        self.num_scalar_v = config.num_scalar_v
        self.num_point_v = config.num_point_v
        self.num_point_qk = config.num_point_qk
        self.num_channel = config.num_channel
        self.projection_num = self.num_head * self.num_scalar_v + self.num_head * self.num_point_v * 4 +\
            self.num_head * pair_dim

        self.global_config = global_config
        self.q_scalar = nn.Dense(config.num_channel, self.num_head*self.num_scalar_qk).to_float(mstype.float16)
        self.kv_scalar = nn.Dense(config.num_channel, self.num_head*(self.num_scalar_qk + self.num_scalar_v)
                                  ).to_float(mstype.float16)
        self.q_point_local = nn.Dense(config.num_channel, self.num_head * 3 * self.num_point_qk
                                      ).to_float(mstype.float16)
        self.kv_point_local = nn.Dense(config.num_channel, self.num_head * 3 * (self.num_point_qk + self.num_point_v)
                                       ).to_float(mstype.float16)
        self.soft_max = nn.Softmax()
        self.soft_plus = ops.Softplus()
        self.trainable_point_weights = Parameter(Tensor(np.ones((12,)), mstype.float32), name="trainable_point_weights")
        self.attention_2d = nn.Dense(pair_dim, self.num_head).to_float(mstype.float16)
        self.output_projection = nn.Dense(self.projection_num, self.num_channel, weight_init='zeros'
                                          ).to_float(mstype.float16)
        self.scalar_weights = np.sqrt(1.0 / (3 * 16))
        self.point_weights = np.sqrt(1.0 / (3 * 18))
        self.attention_2d_weights = np.sqrt(1.0 / 3)

    def construct(self, inputs_1d, inputs_2d, mask, rotation, translation):
        """Compute geometry-aware attention.

        Args:
          inputs_1d: (N, C) 1D input embedding that is the basis for the
            scalar queries.
          inputs_2d: (N, M, C') 2D input embedding, used for biases and values.
          mask: (N, 1) mask to indicate which elements of inputs_1d participate
            in the attention.
          rotation: describe the orientation of every element in inputs_1d
          translation: describe the position of every element in inputs_1d

        Returns:
          Transformation of the input embedding.
        """

        num_residues, _ = inputs_1d.shape

        # Improve readability by removing a large number of 'self's.
        num_head = self.num_head
        num_scalar_qk = self.num_scalar_qk
        num_point_qk = self.num_point_qk
        num_scalar_v = self.num_scalar_v
        num_point_v = self.num_point_v

        # Construct scalar queries of shape:
        q_scalar = self.q_scalar(inputs_1d)
        q_scalar = mnp.reshape(q_scalar, [num_residues, num_head, num_scalar_qk])

        # Construct scalar keys/values of shape:
        # [num_target_residues, num_head, num_points]
        kv_scalar = self.kv_scalar(inputs_1d)
        kv_scalar = mnp.reshape(kv_scalar, [num_residues, num_head, num_scalar_v + num_scalar_qk])
        k_scalar, v_scalar = mnp.split(kv_scalar, [num_scalar_qk], axis=-1)

        # Construct query points of shape:
        # [num_residues, num_head, num_point_qk]
        # First construct query points in local frame.
        q_point_local = self.q_point_local(inputs_1d)
        q_point_local = mnp.stack(mnp.split(q_point_local, 3, axis=-1), axis=0)

        # Project query points into global frame.
        q_point_global = apply_to_point(rotation, translation, q_point_local)

        # Reshape query point for later use.
        q_point0 = mnp.reshape(q_point_global[0], (num_residues, num_head, num_point_qk))
        q_point1 = mnp.reshape(q_point_global[1], (num_residues, num_head, num_point_qk))
        q_point2 = mnp.reshape(q_point_global[2], (num_residues, num_head, num_point_qk))

        # Construct key and value points.
        # Key points have shape [num_residues, num_head, num_point_qk]
        # Value points have shape [num_residues, num_head, num_point_v]

        # Construct key and value points in local frame.
        kv_point_local = self.kv_point_local(inputs_1d)

        kv_point_local = mnp.split(kv_point_local, 3, axis=-1)
        # Project key and value points into global frame.
        kv_point_global = apply_to_point(rotation, translation, kv_point_local)

        kv_point_global0 = mnp.reshape(kv_point_global[0], (num_residues, num_head, (num_point_qk + num_point_v)))
        kv_point_global1 = mnp.reshape(kv_point_global[1], (num_residues, num_head, (num_point_qk + num_point_v)))
        kv_point_global2 = mnp.reshape(kv_point_global[2], (num_residues, num_head, (num_point_qk + num_point_v)))

        # Split key and value points.
        k_point0, v_point0 = mnp.split(kv_point_global0, [num_point_qk,], axis=-1)
        k_point1, v_point1 = mnp.split(kv_point_global1, [num_point_qk,], axis=-1)
        k_point2, v_point2 = mnp.split(kv_point_global2, [num_point_qk,], axis=-1)

        trainable_point_weights = self.soft_plus(self.trainable_point_weights)
        point_weights = self.point_weights * mnp.expand_dims(trainable_point_weights, axis=1)

        v_point = [mnp.swapaxes(v_point0, -2, -3), mnp.swapaxes(v_point1, -2, -3), mnp.swapaxes(v_point2, -2, -3)]
        q_point = [mnp.swapaxes(q_point0, -2, -3), mnp.swapaxes(q_point1, -2, -3), mnp.swapaxes(q_point2, -2, -3)]
        k_point = [mnp.swapaxes(k_point0, -2, -3), mnp.swapaxes(k_point1, -2, -3), mnp.swapaxes(k_point2, -2, -3)]

        dist2 = mnp.square(q_point[0][:, :, None, :] - k_point[0][:, None, :, :]) + \
            mnp.square(q_point[1][:, :, None, :] - k_point[1][:, None, :, :]) + \
            mnp.square(q_point[2][:, :, None, :] - k_point[2][:, None, :, :])

        attn_qk_point = -0.5 * mnp.sum(
            point_weights[:, None, None, :] * dist2, axis=-1)

        v = mnp.swapaxes(v_scalar, -2, -3)
        q = mnp.swapaxes(self.scalar_weights * q_scalar, -2, -3)
        k = mnp.swapaxes(k_scalar, -2, -3)
        attn_qk_scalar = ops.matmul(q, mnp.swapaxes(k, -2, -1))
        attn_logits = attn_qk_scalar + attn_qk_point

        attention_2d = self.attention_2d(inputs_2d)
        attention_2d = mnp.transpose(attention_2d, [2, 0, 1])
        attention_2d = self.attention_2d_weights * attention_2d

        attn_logits += attention_2d

        mask_2d = mask * mnp.swapaxes(mask, -1, -2)
        attn_logits -= 1e5 * (1. - mask_2d)

        # [num_head, num_query_residues, num_target_residues]
        attn = self.soft_max(attn_logits)

        # [num_head, num_query_residues, num_head * num_scalar_v]
        result_scalar = ops.matmul(attn, v)

        result_point_global = [mnp.swapaxes(mnp.sum(attn[:, :, :, None] * v_point[0][:, None, :, :], axis=-2), -2, -3),
                               mnp.swapaxes(mnp.sum(attn[:, :, :, None] * v_point[1][:, None, :, :], axis=-2), -2, -3),
                               mnp.swapaxes(mnp.sum(attn[:, :, :, None] * v_point[2][:, None, :, :], axis=-2), -2, -3)
                               ]

        result_point_global = [mnp.reshape(result_point_global[0], [num_residues, num_head * num_point_v]),
                               mnp.reshape(result_point_global[1], [num_residues, num_head * num_point_v]),
                               mnp.reshape(result_point_global[2], [num_residues, num_head * num_point_v])]
        result_scalar = mnp.swapaxes(result_scalar, -2, -3)

        result_scalar = mnp.reshape(result_scalar, [num_residues, num_head * num_scalar_v])

        result_point_local = _invert_point(result_point_global, rotation, translation)

        output_feature1 = result_scalar
        output_feature20 = result_point_local[0]
        output_feature21 = result_point_local[1]
        output_feature22 = result_point_local[2]

        output_feature3 = mnp.sqrt(self._dist_epsilon +
                                   mnp.square(result_point_local[0]) +
                                   mnp.square(result_point_local[1]) +
                                   mnp.square(result_point_local[2]))

        result_attention_over_2d = ops.matmul(mnp.swapaxes(attn, 0, 1), inputs_2d)
        num_out = num_head * result_attention_over_2d.shape[-1]
        output_feature4 = mnp.reshape(result_attention_over_2d, [num_residues, num_out])

        final_act = mnp.concatenate([output_feature1, output_feature20, output_feature21,
                                     output_feature22, output_feature3, output_feature4], axis=-1)
        final_result = self.output_projection(final_act)
        return final_result


class MultiRigidSidechain(nn.Cell):
    """Class to make side chain atoms."""

    def __init__(self, config, global_config, single_repr_dim):
        super().__init__()
        self.config = config
        self.global_config = global_config
        self.input_projection = nn.Dense(single_repr_dim, config.num_channel, weight_init='normal'
                                         ).to_float(mstype.float16)
        self.input_projection_1 = nn.Dense(single_repr_dim, config.num_channel, weight_init='normal'
                                           ).to_float(mstype.float16)
        self.relu = nn.ReLU()
        self.resblock1 = nn.Dense(config.num_channel, config.num_channel, weight_init='normal').to_float(mstype.float16)
        self.resblock2 = nn.Dense(config.num_channel, config.num_channel, weight_init='zeros').to_float(mstype.float16)
        self.resblock1_1 = nn.Dense(config.num_channel, config.num_channel, weight_init='normal'
                                    ).to_float(mstype.float16)
        self.resblock2_1 = nn.Dense(config.num_channel, config.num_channel, weight_init='zeros'
                                    ).to_float(mstype.float16)
        self.unnormalized_angles = nn.Dense(config.num_channel, 14, weight_init='normal').to_float(mstype.float16)
        self.print = ops.Print()
        self.restype_atom14_to_rigid_group = Tensor(residue_constants.restype_atom14_to_rigid_group)
        self.restype_atom14_rigid_group_positions = Tensor(residue_constants.restype_atom14_rigid_group_positions)
        self.restype_atom14_mask = Tensor(residue_constants.restype_atom14_mask)
        self.restype_rigid_group_default_frame = Tensor(residue_constants.restype_rigid_group_default_frame)

    def construct(self, rotation, translation, act, initial_act, aatype):
        """Predict side chains using rotation and translation representations.

        Args:
          rotation: The rotation matrices.
          translation: A translation matrices.
          act: updated pair activations from structure module
          initial_act: initial act representations (input of structure module)
          aatype: Amino acid type representations

        Returns:
          angles, positions and new frames
        """

        act1 = self.input_projection(self.relu(act.astype(mstype.float32)))
        init_act1 = self.input_projection_1(self.relu(initial_act.astype(mstype.float32)))
        # Sum the activation list (equivalent to concat then Linear).
        act = act1 + init_act1

        # Mapping with some residual blocks.
        # for _ in range(self.config.num_residual_block):
        # resblock1
        old_act = act
        act = self.resblock1(self.relu(act.astype(mstype.float32)))
        act = self.resblock2(self.relu(act.astype(mstype.float32)))
        act += old_act
        # resblock2
        old_act = act
        act = self.resblock1_1(self.relu(act.astype(mstype.float32)))
        act = self.resblock2_1(self.relu(act.astype(mstype.float32)))
        act += old_act

        # Map activations to torsion angles. Shape: (num_res, 14).
        num_res = act.shape[0]
        unnormalized_angles = self.unnormalized_angles(self.relu(act.astype(mstype.float32)))

        unnormalized_angles = mnp.reshape(unnormalized_angles, [num_res, 7, 2])

        angles = l2_normalize(unnormalized_angles, axis=-1)

        backb_to_global = [rotation[0][0], rotation[0][1], rotation[0][2],
                           rotation[1][0], rotation[1][1], rotation[1][2],
                           rotation[2][0], rotation[2][1], rotation[2][2],
                           translation[0], translation[1], translation[2]]

        all_frames_to_global = torsion_angles_to_frames(aatype, backb_to_global, angles,
                                                        self.restype_rigid_group_default_frame)

        pred_positions = frames_and_literature_positions_to_atom14_pos(aatype, all_frames_to_global,
                                                                       self.restype_atom14_to_rigid_group,
                                                                       self.restype_atom14_rigid_group_positions,
                                                                       self.restype_atom14_mask)

        atom_pos = pred_positions
        frames = all_frames_to_global

        return angles, unnormalized_angles, atom_pos, frames


class FoldIteration(nn.Cell):
    """A single iteration of the main structure module loop."""

    def __init__(self, config, global_config, pair_dim, single_repr_dim):
        super().__init__()
        self.config = config
        self.global_config = global_config
        self.drop_out = nn.Dropout(keep_prob=0.9)
        self.attention_layer_norm = nn.LayerNorm([config.num_channel,], epsilon=1e-5)
        self.transition_layer_norm = nn.LayerNorm([config.num_channel,], epsilon=1e-5)
        self.transition = nn.Dense(config.num_channel, config.num_channel, weight_init='normal'
                                   ).to_float(mstype.float16)
        self.transition_1 = nn.Dense(config.num_channel, config.num_channel, weight_init='normal'
                                     ).to_float(mstype.float16)
        self.transition_2 = nn.Dense(config.num_channel, config.num_channel, weight_init='normal'
                                     ).to_float(mstype.float16)
        self.relu = nn.ReLU()
        self.affine_update = nn.Dense(config.num_channel, 6, weight_init='zeros').to_float(mstype.float16)
        self.attention_module = InvariantPointAttention(self.config, self.global_config, pair_dim)
        self.mu_side_chain = MultiRigidSidechain(config.sidechain, global_config, single_repr_dim)
        self.print = ops.Print()

    def construct(self, act, static_feat_2d, sequence_mask, quaternion, rotation, translation, initial_act, aatype):
        '''constuct'''
        # Attention
        attn = self.attention_module(act, static_feat_2d, sequence_mask, rotation, translation)
        act += attn
        act = self.drop_out(act)
        act = self.attention_layer_norm(act.astype(mstype.float32))
        # Transition
        input_act = act
        act = self.transition(act)
        act = self.relu(act.astype(mstype.float32))
        act = self.transition_1(act)
        act = self.relu(act.astype(mstype.float32))
        act = self.transition_2(act)

        act += input_act
        act = self.drop_out(act)
        act = self.transition_layer_norm(act.astype(mstype.float32))

        # This block corresponds to
        # Jumper et al. (2021) Alg. 23 "Backbone update"
        # Affine update
        affine_update = self.affine_update(act)

        quaternion, rotation, translation = pre_compose(quaternion, rotation, translation, affine_update)
        _, rotation1, translation1 = scale_translation(quaternion, translation, rotation, 10.0)

        angles_sin_cos, unnormalized_angles_sin_cos, atom_pos, frames =\
            self.mu_side_chain(rotation1, translation1, act, initial_act, aatype)

        affine_output = to_tensor_new(quaternion, translation)

        return act, quaternion, translation, rotation, affine_output, angles_sin_cos, unnormalized_angles_sin_cos, \
            atom_pos, frames


class StructureModule(nn.Cell):
    """StructureModule as a network head."""

    def __init__(self, config, single_repr_dim, pair_dim, global_config=None, compute_loss=True):
        super(StructureModule, self).__init__()
        self.config = config
        self.global_config = global_config
        self.compute_loss = compute_loss
        self.fold_iteration = FoldIteration(self.config, global_config, pair_dim, single_repr_dim)
        self.single_layer_norm = nn.LayerNorm([single_repr_dim,], epsilon=1e-5)
        self.initial_projection = nn.Dense(single_repr_dim, self.config.num_channel).to_float(mstype.float16)
        self.pair_layer_norm = nn.LayerNorm([pair_dim,], epsilon=1e-5)
        self.num_layer = config.num_layer
        self.indice0 = Tensor(
            np.arange(global_config.seq_length).reshape((-1, 1, 1)).repeat(37, axis=1).astype("int32"))

    @ms_function
    def construct(self, single, pair, seq_mask, aatype, residx_atom37_to_atom14=None, atom37_atom_exists=None):
        '''construct'''
        sequence_mask = seq_mask[:, None]
        act = self.single_layer_norm(single.astype(mstype.float32))
        initial_act = act
        act = self.initial_projection(act)
        quaternion, rotation, translation = generate_new_affine(sequence_mask)
        aff_to_tensor = to_tensor(quaternion, mnp.transpose(translation))
        act_2d = self.pair_layer_norm(pair.astype(mstype.float32))
        # folder iteration
        quaternion, rotation, translation = from_tensor(aff_to_tensor)

        act_new, atom_pos, _, _, _, _ =\
            self.iteration_operation(act, act_2d, sequence_mask, quaternion, rotation, translation, initial_act, aatype)
        atom14_pred_positions = vecs_to_tensor(atom_pos)[-1]

        atom37_pred_positions = atom14_to_atom37(atom14_pred_positions,
                                                 residx_atom37_to_atom14,
                                                 atom37_atom_exists,
                                                 self.indice0)

        final_atom_positions = atom37_pred_positions
        final_atom_mask = atom37_atom_exists
        rp_structure_module = act_new
        return final_atom_positions, final_atom_mask, rp_structure_module

    def iteration_operation(self, act, act_2d, sequence_mask, quaternion, rotation, translation, initial_act,
                            aatype):
        '''iteration operation'''
        affine_init = ()
        angles_sin_cos_init = ()
        um_angles_sin_cos_init = ()
        atom_pos = ()
        frames = ()

        for _ in range(self.num_layer):
            act, quaternion, translation, rotation, affine_output, angles_sin_cos, unnormalized_angles_sin_cos, \
                atom_pos, frames = \
                self.fold_iteration(act, act_2d, sequence_mask, quaternion, rotation, translation, initial_act, aatype)
            affine_init = affine_init + (affine_output[None, ...],)
            angles_sin_cos_init = angles_sin_cos_init + (angles_sin_cos[None, ...],)
            um_angles_sin_cos_init = um_angles_sin_cos_init + (unnormalized_angles_sin_cos[None, ...],)
            atom_pos = get_exp_atom_pos(atom_pos)
            frames = get_exp_frames(frames)
        affine_output_new = mnp.concatenate(affine_init, axis=0)
        angles_sin_cos_new = mnp.concatenate(angles_sin_cos_init, axis=0)
        um_angles_sin_cos_new = mnp.concatenate(um_angles_sin_cos_init, axis=0)

        return act, atom_pos, affine_output_new, angles_sin_cos_new, um_angles_sin_cos_new, frames


class PredictedLDDTHead(nn.Cell):
    """Head to predict the per-residue LDDT to be used as a confidence measure."""
    def __init__(self, config, global_config, seq_channel):
        super().__init__()
        self.config = config
        self.global_config = global_config
        self.input_layer_norm = nn.LayerNorm([seq_channel,], epsilon=1e-5)
        self.act_0 = nn.Dense(seq_channel, self.config.num_channels, weight_init='zeros'
                              ).to_float(mstype.float16)
        self.act_1 = nn.Dense(self.config.num_channels, self.config.num_channels, weight_init='zeros'
                              ).to_float(mstype.float16)
        self.logits = nn.Dense(self.config.num_channels, self.config.num_bins, weight_init='zeros'
                               ).to_float(mstype.float16)
        self.relu = nn.ReLU()

    def construct(self, rp_structure_module):
        """Builds ExperimentallyResolvedHead module."""
        act = rp_structure_module
        act = self.input_layer_norm(act.astype(mstype.float32))
        act = self.act_0(act)
        act = self.relu(act.astype(mstype.float32))
        act = self.act_1(act)
        act = self.relu(act.astype(mstype.float32))
        logits = self.logits(act)
        return logits
