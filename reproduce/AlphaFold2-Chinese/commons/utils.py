"""utils module"""

import numpy as np
from scipy.special import softmax

from mindspore.ops import operations as P
import mindspore.numpy as mnp
import mindspore.nn as nn
from mindspore.common.tensor import Tensor

from commons import residue_constants
import commons.r3 as r3


QUAT_TO_ROT = np.zeros((4, 4, 3, 3), dtype=np.float32)

QUAT_TO_ROT[0, 0] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]  # rr
QUAT_TO_ROT[1, 1] = [[1, 0, 0], [0, -1, 0], [0, 0, -1]]  # ii
QUAT_TO_ROT[2, 2] = [[-1, 0, 0], [0, 1, 0], [0, 0, -1]]  # jj
QUAT_TO_ROT[3, 3] = [[-1, 0, 0], [0, -1, 0], [0, 0, 1]]  # kk

QUAT_TO_ROT[1, 2] = [[0, 2, 0], [2, 0, 0], [0, 0, 0]]  # ij
QUAT_TO_ROT[1, 3] = [[0, 0, 2], [0, 0, 0], [2, 0, 0]]  # ik
QUAT_TO_ROT[2, 3] = [[0, 0, 0], [0, 0, 2], [0, 2, 0]]  # jk

QUAT_TO_ROT[0, 1] = [[0, 0, 0], [0, 0, -2], [0, 2, 0]]  # ir
QUAT_TO_ROT[0, 2] = [[0, 0, 2], [0, 0, 0], [-2, 0, 0]]  # jr
QUAT_TO_ROT[0, 3] = [[0, -2, 0], [2, 0, 0], [0, 0, 0]]  # kr

QUAT_TO_ROT = Tensor(QUAT_TO_ROT)


def pseudo_beta_fn(aatype, all_atom_positions, all_atom_masks):
    """Create pseudo beta features."""

    is_gly = mnp.equal(aatype, residue_constants.restype_order['G'])
    ca_idx = residue_constants.atom_order['CA']
    cb_idx = residue_constants.atom_order['CB']
    pseudo_beta = mnp.where(
        mnp.tile(is_gly[..., None].astype("int32"), [1,] * len(is_gly.shape) + [3,]).astype("bool"),
        all_atom_positions[..., ca_idx, :],
        all_atom_positions[..., cb_idx, :])
    if all_atom_masks is not None:
        pseudo_beta_mask = mnp.where(is_gly, all_atom_masks[..., ca_idx], all_atom_masks[..., cb_idx])
        pseudo_beta_mask = pseudo_beta_mask.astype(mnp.float32)
        return pseudo_beta, pseudo_beta_mask
    return pseudo_beta


def dgram_from_positions(positions, num_bins, min_bin, max_bin):
    """Compute distogram from amino acid positions.

    Arguments:
    positions: [N_res, 3] Position coordinates.
    num_bins: The number of bins in the distogram.
    min_bin: The left edge of the first bin.
    max_bin: The left edge of the final bin. The final bin catches
    everything larger than `max_bin`.

    Returns:
    Distogram with the specified number of bins.
    """

    def squared_difference(x, y):
        return mnp.square(x - y)

    lower_breaks = mnp.linspace(min_bin, max_bin, num_bins)
    lower_breaks = mnp.square(lower_breaks)
    upper_breaks = mnp.concatenate([lower_breaks[1:], mnp.array([1e8], dtype=mnp.float32)], axis=-1)
    dist2 = mnp.sum(squared_difference(mnp.expand_dims(positions, axis=-2),
                                       mnp.expand_dims(positions, axis=-3)), axis=-1, keepdims=True)
    dgram = ((dist2 > lower_breaks).astype(mnp.float32) * (dist2 < upper_breaks).astype(mnp.float32))
    return dgram


def _multiply(a, b):
    return mnp.stack([mnp.concatenate([(a[0][0] * b[0][0] + a[0][1] * b[1][0] + a[0][2] * b[2][0])[None, ...],
                                       (a[0][0] * b[0][1] + a[0][1] * b[1][1] + a[0][2] * b[2][1])[None, ...],
                                       (a[0][0] * b[0][2] + a[0][1] * b[1][2] + a[0][2] * b[2][2])[None, ...]], axis=0),
                      mnp.concatenate([(a[1][0] * b[0][0] + a[1][1] * b[1][0] + a[1][2] * b[2][0])[None, ...],
                                       (a[1][0] * b[0][1] + a[1][1] * b[1][1] + a[1][2] * b[2][1])[None, ...],
                                       (a[1][0] * b[0][2] + a[1][1] * b[1][2] + a[1][2] * b[2][2])[None, ...]], axis=0),
                      mnp.concatenate([(a[2][0] * b[0][0] + a[2][1] * b[1][0] + a[2][2] * b[2][0])[None, ...],
                                       (a[2][0] * b[0][1] + a[2][1] * b[1][1] + a[2][2] * b[2][1])[None, ...],
                                       (a[2][0] * b[0][2] + a[2][1] * b[1][2] + a[2][2] * b[2][2])[None, ...]],
                                      axis=0)])


def apply_rot_to_vec(rot, vec, unstack=False):
    """Multiply rotation matrix by a vector."""
    if unstack:
        x, y, z = vec[:, 0], vec[:, 1], vec[:, 2]
    else:
        x, y, z = vec
    return [rot[0][0] * x + rot[0][1] * y + rot[0][2] * z,
            rot[1][0] * x + rot[1][1] * y + rot[1][2] * z,
            rot[2][0] * x + rot[2][1] * y + rot[2][2] * z]


def make_canonical_transform(n_xyz, ca_xyz, c_xyz):
    """Returns translation and rotation matrices to canonicalize residue atoms.

    Note that this method does not take care of symmetries. If you provide the
    atom positions in the non-standard way, the N atom will end up not at
    [-0.527250, 1.359329, 0.0] but instead at [-0.527250, -1.359329, 0.0]. You
    need to take care of such cases in your code.

    Args:
    n_xyz: An array of shape [batch, 3] of nitrogen xyz coordinates.
    ca_xyz: An array of shape [batch, 3] of carbon alpha xyz coordinates.
    c_xyz: An array of shape [batch, 3] of carbon xyz coordinates.

    Returns:
    A tuple (translation, rotation) where:
      translation is an array of shape [batch, 3] defining the translation.
      rotation is an array of shape [batch, 3, 3] defining the rotation.
    After applying the translation and rotation to all atoms in a residue:
      * All atoms will be shifted so that CA is at the origin,
      * All atoms will be rotated so that C is at the x-axis,
      * All atoms will be shifted so that N is in the xy plane.
    """

    # Place CA at the origin.
    translation = -ca_xyz
    n_xyz = n_xyz + translation
    c_xyz = c_xyz + translation

    # Place C on the x-axis.
    c_x, c_y, c_z = c_xyz[:, 0], c_xyz[:, 1], c_xyz[:, 2]
    # Rotate by angle c1 in the x-y plane (around the z-axis).
    sin_c1 = -c_y / mnp.sqrt(1e-20 + c_x ** 2 + c_y ** 2)
    cos_c1 = c_x / mnp.sqrt(1e-20 + c_x ** 2 + c_y ** 2)
    zeros = mnp.zeros_like(sin_c1).astype("float32")
    ones = mnp.ones_like(sin_c1).astype("float32")
    # # pylint: disable=bad-whitespace
    c1_rot_matrix = mnp.stack([mnp.concatenate((cos_c1[None, ...], (-sin_c1)[None, ...], zeros[None, ...]), axis=0),
                               mnp.concatenate((sin_c1[None, ...], cos_c1[None, ...], zeros[None, ...]), axis=0),
                               mnp.concatenate((zeros[None, ...], zeros[None, ...], ones[None, ...]), axis=0)])
    # # Rotate by angle c2 in the x-z plane (around the y-axis).
    sin_c2 = c_z / mnp.sqrt(1e-20 + c_x ** 2 + c_y ** 2 + c_z ** 2)
    cos_c2 = mnp.sqrt(c_x ** 2 + c_y ** 2) / mnp.sqrt(1e-20 + c_x ** 2 + c_y ** 2 + c_z ** 2)
    c2_rot_matrix = mnp.stack([mnp.concatenate((cos_c2[None, ...], zeros[None, ...], sin_c2[None, ...]), axis=0),
                               mnp.concatenate((zeros[None, ...], ones[None, ...], zeros[None, ...]), axis=0),
                               mnp.concatenate(((-sin_c2)[None, ...], zeros[None, ...], cos_c2[None, ...]), axis=0)])
    c_rot_matrix = _multiply(c2_rot_matrix, c1_rot_matrix)
    n_xyz = mnp.stack(apply_rot_to_vec(c_rot_matrix, n_xyz, unstack=True)).T
    # Place N in the x-y plane.
    _, n_y, n_z = n_xyz[:, 0], n_xyz[:, 1], n_xyz[:, 2]
    # Rotate by angle alpha in the y-z plane (around the x-axis).
    sin_n = -n_z / mnp.sqrt(1e-20 + n_y ** 2 + n_z ** 2)
    cos_n = n_y / mnp.sqrt(1e-20 + n_y ** 2 + n_z ** 2)
    n_rot_matrix = mnp.stack([mnp.concatenate([ones[None, ...], zeros[None, ...], zeros[None, ...]], axis=0),
                              mnp.concatenate([zeros[None, ...], cos_n[None, ...], (-sin_n)[None, ...]], axis=0),
                              mnp.concatenate([zeros[None, ...], sin_n[None, ...], cos_n[None, ...]], axis=0)])
    return translation, mnp.transpose(_multiply(n_rot_matrix, c_rot_matrix), [2, 0, 1])


def make_transform_from_reference(n_xyz, ca_xyz, c_xyz):
    """Returns rotation and translation matrices to convert from reference.

    Note that this method does not take care of symmetries. If you provide the
    atom positions in the non-standard way, the N atom will end up not at
    [-0.527250, 1.359329, 0.0] but instead at [-0.527250, -1.359329, 0.0]. You
    need to take care of such cases in your code.

    Args:
    n_xyz: An array of shape [batch, 3] of nitrogen xyz coordinates.
    ca_xyz: An array of shape [batch, 3] of carbon alpha xyz coordinates.
    c_xyz: An array of shape [batch, 3] of carbon xyz coordinates.

    Returns:
    A tuple (rotation, translation) where:
    rotation is an array of shape [batch, 3, 3] defining the rotation.
    translation is an array of shape [batch, 3] defining the translation.
    After applying the translation and rotation to the reference backbone,
    the coordinates will approximately equal to the input coordinates.

    The order of translation and rotation differs from make_canonical_transform
    because the rotation from this function should be applied before the
    translation, unlike make_canonical_transform.
    """
    translation, rotation = make_canonical_transform(n_xyz, ca_xyz, c_xyz)
    return mnp.transpose(rotation, (0, 2, 1)), -translation


def rot_to_quat(rot, unstack_inputs=False):
    """Convert rotation matrix to quaternion.

    Note that this function calls self_adjoint_eig which is extremely expensive on
    the GPU. If at all possible, this function should run on the CPU.

    Args:
    rot: rotation matrix (see below for format).
    unstack_inputs:  If true, rotation matrix should be shape (..., 3, 3)
    otherwise the rotation matrix should be a list of lists of tensors.

    Returns:
    Quaternion as (..., 4) tensor.
    """

    if unstack_inputs:
        rot = mnp.transpose(rot, [2, 1, 0])
    xx, xy, xz = rot[0][0], rot[0][1], rot[0][2]
    yx, yy, yz = rot[1][0], rot[1][1], rot[1][2]
    zx, zy, zz = rot[2][0], rot[2][1], rot[2][2]
    k = mnp.stack((mnp.stack((xx + yy + zz, zy - yz, xz - zx, yx - xy), axis=-1),
                   mnp.stack((zy - yz, xx - yy - zz, xy + yx, xz + zx), axis=-1),
                   mnp.stack((xz - zx, xy + yx, yy - xx - zz, yz + zy), axis=-1),
                   mnp.stack((yx - xy, xz + zx, yz + zy, zz - xx - yy), axis=-1)), axis=-2)
    k = (1. / 3.) * k

    k = k[:, :, 0]
    return k


def quat_to_rot(normalized_quat):
    """Convert a normalized quaternion to a rotation matrix."""
    rot_tensor = mnp.sum(mnp.reshape(QUAT_TO_ROT, (4, 4, 9)) * normalized_quat[..., :, None, None] *
                         normalized_quat[..., None, :, None], axis=(-3, -2))
    rot = mnp.moveaxis(rot_tensor, -1, 0)  # Unstack.
    return [[rot[0], rot[1], rot[2]],
            [rot[3], rot[4], rot[5]],
            [rot[6], rot[7], rot[8]]]


def quat_affine(quaternion, translation, rotation=None, normalize=True, unstack_inputs=False):
    """create quat affine representations"""

    if unstack_inputs and rotation is not None:
        rotation = mnp.transpose(rotation, [2, 1, 0])
    translation = mnp.moveaxis(translation, -1, 0)  # Unstack.
    if normalize and quaternion is not None:
        quaternion = quaternion / mnp.norm(quaternion, axis=-1, keepdims=True)

    if rotation is None:
        rotation = quat_to_rot(quaternion)

    return quaternion, rotation, translation


def apply_inverse_rot_to_vec(rot, vec):
    """Multiply the inverse of a rotation matrix by a vector."""
    # Inverse rotation is just transpose
    return mnp.concatenate(((rot[0][0] * vec[0] + rot[1][0] * vec[1] + rot[2][0] * vec[2])[None, ...],
                            (rot[0][1] * vec[0] + rot[1][1] * vec[1] + rot[2][1] * vec[2])[None, ...],
                            (rot[0][2] * vec[0] + rot[1][2] * vec[1] + rot[2][2] * vec[2])[None, ...]), axis=0)


def invert_point(transformed_point, rotation, translation, extra_dims=0):
    """Apply inverse of transformation to a point.

    Args:
    transformed_point: List of 3 tensors to apply affine
    extra_dims:  Number of dimensions at the end of the transformed_point
    shape that are not present in the rotation and translation.  The most
    common use is rotation N points at once with extra_dims=1 for use in a
    network.

    Returns:
    Transformed point after applying affine.
    """
    for _ in range(extra_dims):
        rotation = mnp.expand_dims(rotation, axis=-1)
        translation = mnp.expand_dims(translation, axis=-1)
    rot_point = transformed_point - translation
    return apply_inverse_rot_to_vec(rotation, rot_point)


def _invert_point(transformed_point, rotation, translation):
    """Apply inverse of transformation to a point.

    Args:
    transformed_point: List of 3 tensors to apply affine
    extra_dims:  Number of dimensions at the end of the transformed_point
    shape that are not present in the rotation and translation.  The most
    common use is rotation N points at once with extra_dims=1 for use in a
    network.

    Returns:
    Transformed point after applying affine.
    """
    r00 = mnp.expand_dims(rotation[0][0], axis=-1)
    r01 = mnp.expand_dims(rotation[0][1], axis=-1)
    r02 = mnp.expand_dims(rotation[0][2], axis=-1)
    r10 = mnp.expand_dims(rotation[1][0], axis=-1)
    r11 = mnp.expand_dims(rotation[1][1], axis=-1)
    r12 = mnp.expand_dims(rotation[1][2], axis=-1)
    r20 = mnp.expand_dims(rotation[2][0], axis=-1)
    r21 = mnp.expand_dims(rotation[2][1], axis=-1)
    r22 = mnp.expand_dims(rotation[2][2], axis=-1)

    t0 = mnp.expand_dims(translation[0], axis=-1)
    t1 = mnp.expand_dims(translation[1], axis=-1)
    t2 = mnp.expand_dims(translation[2], axis=-1)

    rot_point = [transformed_point[0] - t0, transformed_point[1] - t1, transformed_point[2] - t2]

    result = [r00 * rot_point[0] + r10 * rot_point[1] + r20 * rot_point[2],
              r01 * rot_point[0] + r11 * rot_point[1] + r21 * rot_point[2],
              r02 * rot_point[0] + r12 * rot_point[1] + r22 * rot_point[2]]
    return result


def mask_mean(mask, value, axis=None, drop_mask_channel=False, eps=1e-10):
    """Masked mean."""
    if drop_mask_channel:
        mask = mask[..., 0]
    mask_shape = mask.shape
    value_shape = value.shape
    broadcast_factor = 1.
    value_size = value_shape[axis]
    mask_size = mask_shape[axis]
    if mask_size == 1:
        broadcast_factor *= value_size
    return mnp.sum(mask * value, axis=axis) / (mnp.sum(mask, axis=axis) * broadcast_factor + eps)


def atom37_to_torsion_angles(
        aatype,  # (B, N)
        all_atom_pos,  # (B, N, 37, 3)
        all_atom_mask,  # (B, N, 37)
        chi_atom_indices,
        chi_angles_mask,
        mirror_psi_mask,
        chi_pi_periodic,
        indices0,
        indices1
):
    """Computes the 7 torsion angles (in sin, cos encoding) for each residue.

    The 7 torsion angles are in the order
    '[pre_omega, phi, psi, chi_1, chi_2, chi_3, chi_4]',
    here pre_omega denotes the omega torsion angle between the given amino acid
    and the previous amino acid.

    Args:
    aatype: Amino acid type, given as array with integers.
    all_atom_pos: atom37 representation of all atom coordinates.
    all_atom_mask: atom37 representation of mask on all atom coordinates.
    placeholder_for_undefined: flag denoting whether to set masked torsion
    angles to zero.
    Returns:
    Dict containing:
    * 'torsion_angles_sin_cos': Array with shape (B, N, 7, 2) where the final
    2 dimensions denote sin and cos respectively
    * 'alt_torsion_angles_sin_cos': same as 'torsion_angles_sin_cos', but
    with the angle shifted by pi for all chi angles affected by the naming
    ambiguities.
    * 'torsion_angles_mask': Mask for which chi angles are present.
    """

    # Map aatype > 20 to 'Unknown' (20).
    aatype = mnp.minimum(aatype, 20)

    # Compute the backbone angles.
    num_batch, num_res = aatype.shape

    pad = mnp.zeros([num_batch, 1, 37, 3], mnp.float32)
    prev_all_atom_pos = mnp.concatenate([pad, all_atom_pos[:, :-1, :, :]], axis=1)

    pad = mnp.zeros([num_batch, 1, 37], mnp.float32)
    prev_all_atom_mask = mnp.concatenate([pad, all_atom_mask[:, :-1, :]], axis=1)

    # For each torsion angle collect the 4 atom positions that define this angle.
    # shape (B, N, atoms=4, xyz=3)
    pre_omega_atom_pos = mnp.concatenate([prev_all_atom_pos[:, :, 1:3, :], all_atom_pos[:, :, 0:2, :]], axis=-2)
    phi_atom_pos = mnp.concatenate([prev_all_atom_pos[:, :, 2:3, :], all_atom_pos[:, :, 0:3, :]], axis=-2)
    psi_atom_pos = mnp.concatenate([all_atom_pos[:, :, 0:3, :], all_atom_pos[:, :, 4:5, :]], axis=-2)
    # # Collect the masks from these atoms.
    # # Shape [batch, num_res]
    # ERROR NO PROD
    pre_omega_mask = (P.ReduceProd()(prev_all_atom_mask[:, :, 1:3], -1)  # prev CA, C
                      * P.ReduceProd()(all_atom_mask[:, :, 0:2], -1))  # this N, CA
    phi_mask = (prev_all_atom_mask[:, :, 2]  # prev C
                * P.ReduceProd()(all_atom_mask[:, :, 0:3], -1))  # this N, CA, C
    psi_mask = (P.ReduceProd()(all_atom_mask[:, :, 0:3], -1) *  # this N, CA, C
                all_atom_mask[:, :, 4])  # this O
    # Collect the atoms for the chi-angles.
    # Compute the table of chi angle indices. Shape: [restypes, chis=4, atoms=4].
    # Select atoms to compute chis. Shape: [batch, num_res, chis=4, atoms=4].
    atom_indices = mnp.take(chi_atom_indices, aatype, axis=0)

    # # Gather atom positions Batch Gather. Shape: [batch, num_res, chis=4, atoms=4, xyz=3].

    # 4 seq_length 4 4  batch, sequence length, chis, atoms
    seq_length = all_atom_pos.shape[1]
    atom_indices = atom_indices.reshape((4, seq_length, 4, 4, 1)).astype("int64")
    new_indices = P.Concat(4)((indices0, indices1, atom_indices))  # 4, seq_length, 4, 4, 3
    chis_atom_pos = P.GatherNd()(all_atom_pos, new_indices)
    chis_mask = mnp.take(chi_angles_mask, aatype, axis=0)
    chi_angle_atoms_mask = P.GatherNd()(all_atom_mask, new_indices)

    # chis_atom_pos = P.GatherBatch(axis=0, batch=2)(all_atom_pos, atom_indices)
    # chis_mask = mnp.take(chi_angles_mask, aatype, axis=0)
    # chi_angle_atoms_mask = P.GatherBatch(axis=0, batch=2)(all_atom_mask, atom_indices)

    # Check if all 4 chi angle atoms were set. Shape: [batch, num_res, chis=4].
    chi_angle_atoms_mask = P.ReduceProd()(chi_angle_atoms_mask, -1)
    chis_mask = chis_mask * (chi_angle_atoms_mask).astype(mnp.float32)

    # Stack all torsion angle atom positions.
    # Shape (B, N, torsions=7, atoms=4, xyz=3)ls
    torsions_atom_pos = mnp.concatenate([pre_omega_atom_pos[:, :, None, :, :],
                                         phi_atom_pos[:, :, None, :, :],
                                         psi_atom_pos[:, :, None, :, :],
                                         chis_atom_pos], axis=2)
    # Stack up masks for all torsion angles.
    # shape (B, N, torsions=7)
    torsion_angles_mask = mnp.concatenate([pre_omega_mask[:, :, None],
                                           phi_mask[:, :, None],
                                           psi_mask[:, :, None],
                                           chis_mask], axis=2)

    torsion_frames_rots, torsion_frames_trans = r3.rigids_from_3_points(
        torsions_atom_pos[:, :, :, 1, :],
        torsions_atom_pos[:, :, :, 2, :],
        torsions_atom_pos[:, :, :, 0, :])
    inv_torsion_rots, inv_torsion_trans = r3.invert_rigids(torsion_frames_rots, torsion_frames_trans)
    forth_atom_rel_pos = r3.rigids_mul_vecs(inv_torsion_rots, inv_torsion_trans, torsions_atom_pos[:, :, :, 3, :])

    # Compute the position of the forth atom in this frame (y and z coordinate
    torsion_angles_sin_cos = mnp.stack([forth_atom_rel_pos[..., 2], forth_atom_rel_pos[..., 1]], axis=-1)
    torsion_angles_sin_cos /= mnp.sqrt(mnp.sum(mnp.square(torsion_angles_sin_cos), axis=-1, keepdims=True) + 1e-8)
    # Mirror psi, because we computed it from the Oxygen-atom.
    torsion_angles_sin_cos *= mirror_psi_mask
    chi_is_ambiguous = mnp.take(chi_pi_periodic, aatype, axis=0)
    mirror_torsion_angles = mnp.concatenate([mnp.ones([num_batch, num_res, 3]), 1.0 - 2.0 * chi_is_ambiguous], axis=-1)
    alt_torsion_angles_sin_cos = (torsion_angles_sin_cos * mirror_torsion_angles[:, :, :, None])
    return torsion_angles_sin_cos, alt_torsion_angles_sin_cos, torsion_angles_mask


def get_chi_atom_indices():
    """Returns atom indices needed to compute chi angles for all residue types.

    Returns:
    A tensor of shape [residue_types=21, chis=4, atoms=4]. The residue types are
    in the order specified in residue_constants.restypes + unknown residue type
    at the end. For chi angles which are not defined on the residue, the
    positions indices are by default set to 0.
    """

    chi_atom_indices = []
    for residue_name in residue_constants.restypes:
        residue_name = residue_constants.restype_1to3[residue_name]
        residue_chi_angles = residue_constants.chi_angles_atoms[residue_name]
        atom_indices = []
        for chi_angle in residue_chi_angles:
            atom_indices.append([residue_constants.atom_order[atom] for atom in chi_angle])
        for _ in range(4 - len(atom_indices)):
            atom_indices.append([0, 0, 0, 0])  # For chi angles not defined on the AA.
        chi_atom_indices.append(atom_indices)
    chi_atom_indices.append([[0, 0, 0, 0]] * 4)  # For UNKNOWN residue.
    return np.asarray(chi_atom_indices)


def to_tensor(quaternion, translation):
    return mnp.concatenate([quaternion, translation], axis=-1)


def from_tensor(tensor, normalize=False):
    quaternion, tx, ty, tz = mnp.split(tensor, [4, 5, 6], axis=-1)
    return quat_affine(quaternion, mnp.stack([tx[..., 0], ty[..., 0], tz[..., 0]], axis=-1), normalize=normalize)
    # return quat_affine(quaternion, [tx[..., 0], ty[..., 0], tz[..., 0]], normalize=normalize)


def generate_new_affine(sequence_mask):
    num_residues, _ = sequence_mask.shape
    quaternion = mnp.tile(mnp.reshape(mnp.asarray([1., 0., 0., 0.]), [1, 4]), [num_residues, 1])
    translation = mnp.zeros([num_residues, 3])
    return quat_affine(quaternion, translation, unstack_inputs=True)


def pre_compose(quaternion, rotation, translation, update):
    """Return a new QuatAffine which applies the transformation update first.

    Args:
    update: Length-6 vector. 3-vector of x, y, and z such that the quaternion
    update is (1, x, y, z) and zero for the 3-vector is the identity
    quaternion. 3-vector for translation concatenated.

    Returns:
    New QuatAffine object.
    """

    vector_quaternion_update, x, y, z = mnp.split(update, [3, 4, 5], axis=-1)
    trans_update = [mnp.squeeze(x, axis=-1), mnp.squeeze(y, axis=-1), mnp.squeeze(z, axis=-1)]
    new_quaternion = (quaternion + quat_multiply_by_vec(quaternion, vector_quaternion_update))
    trans_update = apply_rot_to_vec(rotation, trans_update)
    new_translation = [translation[0] + trans_update[0],
                       translation[1] + trans_update[1],
                       translation[2] + trans_update[2]]
    return quat_affine(new_quaternion, mnp.stack(new_translation, axis=-1))


def scale_translation(quaternion, translation, rotation, position_scale):
    """Return a new quat affine with a different scale for translation."""

    return quat_affine(quaternion,
                       mnp.stack([translation[0] * position_scale, translation[1] * position_scale,
                                  translation[2] * position_scale], axis=-1),
                       rotation=rotation,
                       normalize=False)


def rigids_from_tensor4x4(m):
    """Construct Rigids object from an 4x4 array.

    Here the 4x4 is representing the transformation in homogeneous coordinates.

    Args:
    m: Array representing transformations in homogeneous coordinates.
    Returns:
    Rigids object corresponding to transformations m
    """
    return m[..., 0, 0], m[..., 0, 1], m[..., 0, 2], m[..., 1, 0], m[..., 1, 1], m[..., 1, 2], m[..., 2, 0], \
           m[..., 2, 1], m[..., 2, 2], m[..., 0, 3], m[..., 1, 3], m[..., 2, 3]


def apply_to_point(rotation, translation, point):
    """apply to point func"""

    r00 = mnp.expand_dims(rotation[0][0], axis=-1)
    r01 = mnp.expand_dims(rotation[0][1], axis=-1)
    r02 = mnp.expand_dims(rotation[0][2], axis=-1)
    r10 = mnp.expand_dims(rotation[1][0], axis=-1)
    r11 = mnp.expand_dims(rotation[1][1], axis=-1)
    r12 = mnp.expand_dims(rotation[1][2], axis=-1)
    r20 = mnp.expand_dims(rotation[2][0], axis=-1)
    r21 = mnp.expand_dims(rotation[2][1], axis=-1)
    r22 = mnp.expand_dims(rotation[2][2], axis=-1)

    t0 = mnp.expand_dims(translation[0], axis=-1)
    t1 = mnp.expand_dims(translation[1], axis=-1)
    t2 = mnp.expand_dims(translation[2], axis=-1)

    p0 = point[0]
    p1 = point[1]
    p2 = point[2]
    rot_point = [r00 * p0 + r01 * p1 + r02 * p2,
                 r10 * p0 + r11 * p1 + r12 * p2,
                 r20 * p0 + r21 * p1 + r22 * p2]
    result = [rot_point[0] + t0,
              rot_point[1] + t1,
              rot_point[2] + t2]
    return result


def frames_and_literature_positions_to_atom14_pos(aatype, all_frames_to_global, restype_atom14_to_rigid_group,
                                                  restype_atom14_rigid_group_positions, restype_atom14_mask):  # (N, 14)
    """Put atom literature positions (atom14 encoding) in each rigid group.

    Jumper et al. (2021) Suppl. Alg. 24 "computeAllAtomCoordinates" line 11

    Args:
    aatype: aatype for each residue.
    all_frames_to_global: All per residue coordinate frames.
    Returns:
    Positions of all atom coordinates in global frame.
    """

    # Pick the appropriate transform for every atom.
    residx_to_group_idx = P.Gather()(restype_atom14_to_rigid_group, aatype, 0)
    group_mask = nn.OneHot(depth=8, axis=-1)(residx_to_group_idx)

    # # r3.Rigids with shape (N, 14)
    map_atoms_to_global = map_atoms_to_global_func(all_frames_to_global, group_mask)

    # Gather the literature atom positions for each residue.
    # r3.Vecs with shape (N, 14)
    lit_positions = vecs_from_tensor(P.Gather()(restype_atom14_rigid_group_positions, aatype, 0))

    # Transform each atom from its local frame to the global frame.
    # r3.Vecs with shape (N, 14)
    pred_positions = rigids_mul_vecs(map_atoms_to_global, lit_positions)

    # Mask out non-existing atoms.
    mask = P.Gather()(restype_atom14_mask, aatype, 0)

    pred_positions = pred_map_mul(pred_positions, mask)

    return pred_positions


def pred_map_mul(pred_positions, mask):
    return [pred_positions[0] * mask,
            pred_positions[1] * mask,
            pred_positions[2] * mask]


def rots_mul_vecs(m, v):
    """Apply rotations 'm' to vectors 'v'."""

    return [m[0] * v[0] + m[1] * v[1] + m[2] * v[2],
            m[3] * v[0] + m[4] * v[1] + m[5] * v[2],
            m[6] * v[0] + m[7] * v[1] + m[8] * v[2]]


def rigids_mul_vecs(r, v):
    """Apply rigid transforms 'r' to points 'v'."""

    rots = rots_mul_vecs(r, v)
    vecs_add_r = [rots[0] + r[9],
                  rots[1] + r[10],
                  rots[2] + r[11]]
    return vecs_add_r


def vecs_from_tensor(x):  # shape (...)
    """Converts from tensor of shape (3,) to Vecs."""
    # num_components = x.shape[-1]
    # assert num_components == 3
    return x[..., 0], x[..., 1], x[..., 2]


def get_exp_atom_pos(atom_pos):
    return [mnp.expand_dims(atom_pos[0], axis=0),
            mnp.expand_dims(atom_pos[1], axis=0),
            mnp.expand_dims(atom_pos[2], axis=0)
           ]


def to_tensor_new(quaternion, translation):
    tr_new = [mnp.expand_dims(translation[0], axis=-1),
              mnp.expand_dims(translation[1], axis=-1),
              mnp.expand_dims(translation[2], axis=-1)]
    return mnp.concatenate([quaternion, tr_new[0], tr_new[1], tr_new[2]], axis=-1)


def quat_multiply_by_vec(quat, vec):
    """Multiply a quaternion by a pure-vector quaternion."""

    return mnp.sum(residue_constants.QUAT_MULTIPLY_BY_VEC * quat[..., :, None, None] * vec[..., None, :, None],
                   axis=(-3, -2))


def rigids_mul_rots(xx, xy, xz, yx, yy, yz, zx, zy, zz, ones, zeros, cos_angles, sin_angles):
    """Compose rigid transformations 'r' with rotations 'm'."""

    c00 = xx * ones + xy * zeros + xz * zeros
    c01 = yx * ones + yy * zeros + yz * zeros
    c02 = zx * ones + zy * zeros + zz * zeros
    c10 = xx * zeros + xy * cos_angles + xz * sin_angles
    c11 = yx * zeros + yy * cos_angles + yz * sin_angles
    c12 = zx * zeros + zy * cos_angles + zz * sin_angles
    c20 = xx * zeros + xy * (-sin_angles) + xz * cos_angles
    c21 = yx * zeros + yy * (-sin_angles) + yz * cos_angles
    c22 = zx * zeros + zy * (-sin_angles) + zz * cos_angles
    return c00, c10, c20, c01, c11, c21, c02, c12, c22


def rigids_mul_rigids(a, b):
    """Group composition of Rigids 'a' and 'b'."""

    c00 = a[0] * b[0] + a[1] * b[3] + a[2] * b[6]
    c01 = a[3] * b[0] + a[4] * b[3] + a[5] * b[6]
    c02 = a[6] * b[0] + a[7] * b[3] + a[8] * b[6]

    c10 = a[0] * b[1] + a[1] * b[4] + a[2] * b[7]
    c11 = a[3] * b[1] + a[4] * b[4] + a[5] * b[7]
    c12 = a[6] * b[1] + a[7] * b[4] + a[8] * b[7]

    c20 = a[0] * b[2] + a[1] * b[5] + a[2] * b[8]
    c21 = a[3] * b[2] + a[4] * b[5] + a[5] * b[8]
    c22 = a[6] * b[2] + a[7] * b[5] + a[8] * b[8]

    tr0 = a[0] * b[9] + a[1] * b[10] + a[2] * b[11]
    tr1 = a[3] * b[9] + a[4] * b[10] + a[5] * b[11]
    tr2 = a[6] * b[9] + a[7] * b[10] + a[8] * b[11]

    new_tr0 = a[9] + tr0
    new_tr1 = a[10] + tr1
    new_tr2 = a[11] + tr2

    return [c00, c10, c20, c01, c11, c21, c02, c12, c22, new_tr0, new_tr1, new_tr2]


def rigits_concate_all(xall, x5, x6, x7):
    return [mnp.concatenate([xall[0][:, 0:5], x5[0][:, None], x6[0][:, None], x7[0][:, None]], axis=-1),
            mnp.concatenate([xall[1][:, 0:5], x5[1][:, None], x6[1][:, None], x7[1][:, None]], axis=-1),
            mnp.concatenate([xall[2][:, 0:5], x5[2][:, None], x6[2][:, None], x7[2][:, None]], axis=-1),
            mnp.concatenate([xall[3][:, 0:5], x5[3][:, None], x6[3][:, None], x7[3][:, None]], axis=-1),
            mnp.concatenate([xall[4][:, 0:5], x5[4][:, None], x6[4][:, None], x7[4][:, None]], axis=-1),
            mnp.concatenate([xall[5][:, 0:5], x5[5][:, None], x6[5][:, None], x7[5][:, None]], axis=-1),
            mnp.concatenate([xall[6][:, 0:5], x5[6][:, None], x6[6][:, None], x7[6][:, None]], axis=-1),
            mnp.concatenate([xall[7][:, 0:5], x5[7][:, None], x6[7][:, None], x7[7][:, None]], axis=-1),
            mnp.concatenate([xall[8][:, 0:5], x5[8][:, None], x6[8][:, None], x7[8][:, None]], axis=-1),
            mnp.concatenate([xall[9][:, 0:5], x5[9][:, None], x6[9][:, None], x7[9][:, None]], axis=-1),
            mnp.concatenate([xall[10][:, 0:5], x5[10][:, None], x6[10][:, None], x7[10][:, None]], axis=-1),
            mnp.concatenate([xall[11][:, 0:5], x5[11][:, None], x6[11][:, None], x7[11][:, None]], axis=-1)
           ]


def reshape_back(backb):
    return [backb[0][:, None],
            backb[1][:, None],
            backb[2][:, None],
            backb[3][:, None],
            backb[4][:, None],
            backb[5][:, None],
            backb[6][:, None],
            backb[7][:, None],
            backb[8][:, None],
            backb[9][:, None],
            backb[10][:, None],
            backb[11][:, None]
           ]


def l2_normalize(x, axis=-1):
    return x / mnp.sqrt(mnp.sum(x ** 2, axis=axis, keepdims=True))


def torsion_angles_to_frames(aatype, backb_to_global, torsion_angles_sin_cos, restype_rigid_group_default_frame):
    """Compute rigid group frames from torsion angles."""

    # Gather the default frames for all rigid groups.
    m = P.Gather()(restype_rigid_group_default_frame, aatype, 0)

    xx1, xy1, xz1, yx1, yy1, yz1, zx1, zy1, zz1, x1, y1, z1 = rigids_from_tensor4x4(m)

    # Create the rotation matrices according to the given angles (each frame is
    # defined such that its rotation is around the x-axis).
    sin_angles = torsion_angles_sin_cos[..., 0]
    cos_angles = torsion_angles_sin_cos[..., 1]

    # insert zero rotation for backbone group.
    num_residues, = aatype.shape
    sin_angles = mnp.concatenate([mnp.zeros([num_residues, 1]), sin_angles], axis=-1)
    cos_angles = mnp.concatenate([mnp.ones([num_residues, 1]), cos_angles], axis=-1)
    zeros = mnp.zeros_like(sin_angles)
    ones = mnp.ones_like(sin_angles)
    # Apply rotations to the frames.
    xx2, xy2, xz2, yx2, yy2, yz2, zx2, zy2, zz2 = rigids_mul_rots(xx1, xy1, xz1, yx1, yy1, yz1, zx1, zy1, zz1,
                                                                  ones, zeros, cos_angles, sin_angles)
    all_frames = [xx2, xy2, xz2, yx2, yy2, yz2, zx2, zy2, zz2, x1, y1, z1]
    # chi2, chi3, and chi4 frames do not transform to the backbone frame but to
    # the previous frame. So chain them up accordingly.
    chi2_frame_to_frame = [xx2[:, 5], xy2[:, 5], xz2[:, 5], yx2[:, 5], yy2[:, 5], yz2[:, 5], zx2[:, 5], zy2[:, 5],
                           zz2[:, 5], x1[:, 5], y1[:, 5], z1[:, 5]]
    chi3_frame_to_frame = [xx2[:, 6], xy2[:, 6], xz2[:, 6], yx2[:, 6], yy2[:, 6], yz2[:, 6], zx2[:, 6], zy2[:, 6],
                           zz2[:, 6], x1[:, 6], y1[:, 6], z1[:, 6]]
    chi4_frame_to_frame = [xx2[:, 7], xy2[:, 7], xz2[:, 7], yx2[:, 7], yy2[:, 7], yz2[:, 7], zx2[:, 7], zy2[:, 7],
                           zz2[:, 7], x1[:, 7], y1[:, 7], z1[:, 7]]
    #
    chi1_frame_to_backb = [xx2[:, 4], xy2[:, 4], xz2[:, 4], yx2[:, 4], yy2[:, 4], yz2[:, 4], zx2[:, 4], zy2[:, 4],
                           zz2[:, 4], x1[:, 4], y1[:, 4], z1[:, 4]]

    chi2_frame_to_backb = rigids_mul_rigids(chi1_frame_to_backb, chi2_frame_to_frame)
    chi3_frame_to_backb = rigids_mul_rigids(chi2_frame_to_backb, chi3_frame_to_frame)
    chi4_frame_to_backb = rigids_mul_rigids(chi3_frame_to_backb, chi4_frame_to_frame)

    # Recombine them to a r3.Rigids with shape (N, 8).
    all_frames_to_backb = rigits_concate_all(all_frames, chi2_frame_to_backb,
                                             chi3_frame_to_backb, chi4_frame_to_backb)
    backb_to_global_new = reshape_back(backb_to_global)
    # Create the global frames.
    # shape (N, 8)
    all_frames_to_global = rigids_mul_rigids(backb_to_global_new, all_frames_to_backb)
    # all_frames_to_global = rigids_mul_rigids(all_frames_to_backb, backb_to_global)
    return all_frames_to_global


def map_atoms_to_global_func(all_frames, group_mask):
    return [mnp.sum(all_frames[0][:, None, :] * group_mask, axis=-1),
            mnp.sum(all_frames[1][:, None, :] * group_mask, axis=-1),
            mnp.sum(all_frames[2][:, None, :] * group_mask, axis=-1),
            mnp.sum(all_frames[3][:, None, :] * group_mask, axis=-1),
            mnp.sum(all_frames[4][:, None, :] * group_mask, axis=-1),
            mnp.sum(all_frames[5][:, None, :] * group_mask, axis=-1),
            mnp.sum(all_frames[6][:, None, :] * group_mask, axis=-1),
            mnp.sum(all_frames[7][:, None, :] * group_mask, axis=-1),
            mnp.sum(all_frames[8][:, None, :] * group_mask, axis=-1),
            mnp.sum(all_frames[9][:, None, :] * group_mask, axis=-1),
            mnp.sum(all_frames[10][:, None, :] * group_mask, axis=-1),
            mnp.sum(all_frames[11][:, None, :] * group_mask, axis=-1)
           ]


def get_exp_frames(frames):
    return [mnp.expand_dims(frames[0], axis=0),
            mnp.expand_dims(frames[1], axis=0),
            mnp.expand_dims(frames[2], axis=0),
            mnp.expand_dims(frames[3], axis=0),
            mnp.expand_dims(frames[4], axis=0),
            mnp.expand_dims(frames[5], axis=0),
            mnp.expand_dims(frames[6], axis=0),
            mnp.expand_dims(frames[7], axis=0),
            mnp.expand_dims(frames[8], axis=0),
            mnp.expand_dims(frames[9], axis=0),
            mnp.expand_dims(frames[10], axis=0),
            mnp.expand_dims(frames[11], axis=0)
           ]


def vecs_to_tensor(v):
    """Converts 'v' to tensor with shape 3, inverse of 'vecs_from_tensor'."""

    return mnp.stack([v[0], v[1], v[2]], axis=-1)


def atom14_to_atom37(atom14_data, residx_atom37_to_atom14, atom37_atom_exists, indices0):
    """Convert atom14 to atom37 representation."""

    seq_length = atom14_data.shape[0]
    residx_atom37_to_atom14 = residx_atom37_to_atom14.reshape((seq_length, 37, 1))
    new_indices = P.Concat(2)((indices0, residx_atom37_to_atom14))

    atom37_data = P.GatherNd()(atom14_data, new_indices)
    # atom37_data = P.GatherBatch()(atom14_data, residx_atom37_to_atom14)

    if len(atom14_data.shape) == 2:
        atom37_data *= atom37_atom_exists
    elif len(atom14_data.shape) == 3:
        atom37_data *= atom37_atom_exists[:, :, None].astype(atom37_data.dtype)

    return atom37_data


def batch_apply_rot_to_vec(rot, vec, unstack=False):
    """Multiply rotation matrix by a vector."""
    if unstack:
        x, y, z = vec[:, :, 0], vec[:, :, 1], vec[:, :, 2]
    else:
        x, y, z = vec
    return [(rot[:, 0, 0, :] * x + rot[:, 0, 1, :] * y + rot[:, 0, 2, :] * z)[:, None, :],
            (rot[:, 1, 0, :] * x + rot[:, 1, 1, :] * y + rot[:, 1, 2, :] * z)[:, None, :],
            (rot[:, 2, 0, :] * x + rot[:, 2, 1, :] * y + rot[:, 2, 2, :] * z)[:, None, :]]


def _batch_multiply(a, b):
    """ batch multiply operation"""

    x1 = mnp.concatenate(
        [(a[:, 0, 0, :] * b[:, 0, 0, :] + a[:, 0, 1, :] * b[:, 1, 0, :] + a[:, 0, 2, :] * b[:, 2, 0, :])[:, None, :],
         (a[:, 0, 0, :] * b[:, 0, 1, :] + a[:, 0, 1, :] * b[:, 1, 1, :] + a[:, 0, 2, :] * b[:, 2, 1, :])[:, None, :],
         (a[:, 0, 0, :] * b[:, 0, 2, :] + a[:, 0, 1, :] * b[:, 1, 2, :] + a[:, 0, 2, :] * b[:, 2, 2, :])[:, None, :]],
        axis=1)[:, None, :, :]
    x2 = mnp.concatenate(
        [(a[:, 1, 0, :] * b[:, 0, 0, :] + a[:, 1, 1, :] * b[:, 1, 0, :] + a[:, 1, 2, :] * b[:, 2, 0, :])[:, None, :],
         (a[:, 1, 0, :] * b[:, 0, 1, :] + a[:, 1, 1, :] * b[:, 1, 1, :] + a[:, 1, 2, :] * b[:, 2, 1, :])[:, None, :],
         (a[:, 1, 0, :] * b[:, 0, 2, :] + a[:, 1, 1, :] * b[:, 1, 2, :] + a[:, 1, 2, :] * b[:, 2, 2, :])[:, None, :]],
        axis=1)[:, None, :, :]
    x3 = mnp.concatenate(
        [(a[:, 2, 0, :] * b[:, 0, 0, :] + a[:, 2, 1, :] * b[:, 1, 0, :] + a[:, 2, 2, :] * b[:, 2, 0, :])[:, None, :],
         (a[:, 2, 0, :] * b[:, 0, 1, :] + a[:, 2, 1, :] * b[:, 1, 1, :] + a[:, 2, 2, :] * b[:, 2, 1, :])[:, None, :],
         (a[:, 2, 0, :] * b[:, 0, 2, :] + a[:, 2, 1, :] * b[:, 1, 2, :] + a[:, 2, 2, :] * b[:, 2, 2, :])[:, None, :]],
        axis=1)[:, None, :, :]
    return mnp.concatenate([x1, x2, x3], axis=1)


def batch_make_canonical_transform(n_xyz, ca_xyz, c_xyz):
    """Returns translation and rotation matrices to canonicalize residue atoms.

    Note that this method does not take care of symmetries. If you provide the
    atom positions in the non-standard way, the N atom will end up not at
    [-0.527250, 1.359329, 0.0] but instead at [-0.527250, -1.359329, 0.0]. You
    need to take care of such cases in your code.

    Args:
    n_xyz: An array of shape [batch, 3] of nitrogen xyz coordinates.
    ca_xyz: An array of shape [batch, 3] of carbon alpha xyz coordinates.
    c_xyz: An array of shape [batch, 3] of carbon xyz coordinates.

    Returns:
    A tuple (translation, rotation) where:
      translation is an array of shape [batch, 3] defining the translation.
      rotation is an array of shape [batch, 3, 3] defining the rotation.
    After applying the translation and rotation to all atoms in a residue:
      * All atoms will be shifted so that CA is at the origin,
      * All atoms will be rotated so that C is at the x-axis,
      * All atoms will be shifted so that N is in the xy plane.
    """
    # Place CA at the origin.
    translation = -ca_xyz
    n_xyz = n_xyz + translation
    c_xyz = c_xyz + translation

    # Place C on the x-axis.
    c_x, c_y, c_z = c_xyz[:, :, 0], c_xyz[:, :, 1], c_xyz[:, :, 2]
    # Rotate by angle c1 in the x-y plane (around the z-axis).
    sin_c1 = -c_y / mnp.sqrt(1e-20 + c_x ** 2 + c_y ** 2)
    cos_c1 = c_x / mnp.sqrt(1e-20 + c_x ** 2 + c_y ** 2)
    zeros = mnp.zeros_like(sin_c1).astype("float32")
    ones = mnp.ones_like(sin_c1).astype("float32")
    # # pylint: disable=bad-whitespace
    c1_rot_matrix = mnp.concatenate(
        [mnp.concatenate((cos_c1[:, None, ...], (-sin_c1)[:, None, ...], zeros[:, None, ...]), axis=1)[:, None, :, :],
         mnp.concatenate((sin_c1[:, None, ...], cos_c1[:, None, ...], zeros[:, None, ...]), axis=1)[:, None, :, :],
         mnp.concatenate((zeros[:, None, ...], zeros[:, None, ...], ones[:, None, ...]), axis=1)[:, None, :, :]],
        axis=1)
    # # Rotate by angle c2 in the x-z plane (around the y-axis).
    sin_c2 = c_z / mnp.sqrt(1e-20 + c_x ** 2 + c_y ** 2 + c_z ** 2)
    cos_c2 = mnp.sqrt(c_x ** 2 + c_y ** 2) / mnp.sqrt(1e-20 + c_x ** 2 + c_y ** 2 + c_z ** 2)

    c2_rot_matrix = mnp.concatenate(
        [mnp.concatenate((cos_c2[:, None, ...], zeros[:, None, ...], sin_c2[:, None, ...]), axis=1)[:, None, :, :],
         mnp.concatenate((zeros[:, None, ...], ones[:, None, ...], zeros[:, None, ...]), axis=1)[:, None, :, :],
         mnp.concatenate(((-sin_c2)[:, None, ...], zeros[:, None, ...], cos_c2[:, None, ...]), axis=1)[:, None, :, :]],
        axis=1)
    c_rot_matrix = _batch_multiply(c2_rot_matrix, c1_rot_matrix)
    n_xyz = mnp.transpose(mnp.concatenate(batch_apply_rot_to_vec(c_rot_matrix, n_xyz, unstack=True), axis=1), (0, 2, 1))
    # # Place N in the x-y plane.
    _, n_y, n_z = n_xyz[:, :, 0], n_xyz[:, :, 1], n_xyz[:, :, 2]
    # # Rotate by angle alpha in the y-z plane (around the x-axis).
    sin_n = -n_z / mnp.sqrt(1e-20 + n_y ** 2 + n_z ** 2)
    cos_n = n_y / mnp.sqrt(1e-20 + n_y ** 2 + n_z ** 2)
    n_rot_matrix = mnp.concatenate(
        [mnp.concatenate([ones[:, None, ...], zeros[:, None, ...], zeros[:, None, ...]], axis=1)[:, None, :, :],
         mnp.concatenate([zeros[:, None, ...], cos_n[:, None, ...], (-sin_n)[:, None, ...]], axis=1)[:, None, :, :],
         mnp.concatenate([zeros[:, None, ...], sin_n[:, None, ...], cos_n[:, None, ...]], axis=1)[:, None, :, :]],
        axis=1)
    return translation, mnp.transpose(_batch_multiply(n_rot_matrix, c_rot_matrix), [0, 3, 1, 2])


def batch_make_transform_from_reference(n_xyz, ca_xyz, c_xyz):
    """Returns rotation and translation matrices to convert from reference.

    Note that this method does not take care of symmetries. If you provide the
    atom positions in the non-standard way, the N atom will end up not at
    [-0.527250, 1.359329, 0.0] but instead at [-0.527250, -1.359329, 0.0]. You
    need to take care of such cases in your code.

    Args:
    n_xyz: An array of shape [batch, 3] of nitrogen xyz coordinates.
    ca_xyz: An array of shape [batch, 3] of carbon alpha xyz coordinates.
    c_xyz: An array of shape [batch, 3] of carbon xyz coordinates.

    Returns:
    A tuple (rotation, translation) where:
    rotation is an array of shape [batch, 3, 3] defining the rotation.
    translation is an array of shape [batch, 3] defining the translation.
    After applying the translation and rotation to the reference backbone,
    the coordinates will approximately equal to the input coordinates.

    The order of translation and rotation differs from make_canonical_transform
    because the rotation from this function should be applied before the
    translation, unlike make_canonical_transform.
    """
    translation, rotation = batch_make_canonical_transform(n_xyz, ca_xyz, c_xyz)
    return mnp.transpose(rotation, (0, 1, 3, 2)), -translation


def batch_rot_to_quat(rot, unstack_inputs=False):
    """Convert rotation matrix to quaternion.

    Note that this function calls self_adjoint_eig which is extremely expensive on
    the GPU. If at all possible, this function should run on the CPU.

    Args:
    rot: rotation matrix (see below for format).
    unstack_inputs:  If true, rotation matrix should be shape (..., 3, 3)
    otherwise the rotation matrix should be a list of lists of tensors.

    Returns:
    Quaternion as (..., 4) tensor.
    """
    if unstack_inputs:
        rot = mnp.transpose(rot, [0, 3, 2, 1])

    xx, xy, xz = rot[:, 0, 0, :], rot[:, 0, 1, :], rot[:, 0, 2, :]
    yx, yy, yz = rot[:, 1, 0, :], rot[:, 1, 1, :], rot[:, 1, 2, :]
    zx, zy, zz = rot[:, 2, 0, :], rot[:, 2, 1, :], rot[:, 2, 2, :]

    k = mnp.stack((mnp.stack((xx + yy + zz, zy - yz, xz - zx, yx - xy), axis=-1),
                   mnp.stack((zy - yz, xx - yy - zz, xy + yx, xz + zx), axis=-1),
                   mnp.stack((xz - zx, xy + yx, yy - xx - zz, yz + zy), axis=-1),
                   mnp.stack((yx - xy, xz + zx, yz + zy, zz - xx - yy), axis=-1)), axis=-2)
    k = (1. / 3.) * k

    k = k[:, :, :, 0]
    return k


def batch_quat_affine(quaternion, translation, rotation=None, normalize=True, unstack_inputs=False):
    if unstack_inputs:
        if rotation is not None:
            rotation = mnp.transpose(rotation, [0, 3, 2, 1])
    translation = mnp.moveaxis(translation, -1, 1)  # Unstack.
    if normalize and quaternion is not None:
        quaternion = quaternion / mnp.norm(quaternion, axis=-1, keepdims=True)

    return quaternion, rotation, translation


def batch_apply_inverse_rot_to_vec(rot, vec):
    """Multiply the inverse of a rotation matrix by a vector."""
    # Inverse rotation is just transpose
    return mnp.concatenate(
        ((rot[:, 0, 0, :] * vec[:, 0] + rot[:, 1, 0, :] * vec[:, 1] + rot[:, 2, 0, :] * vec[:, 2])[:, None, ...],
         (rot[:, 0, 1, :] * vec[:, 0] + rot[:, 1, 1, :] * vec[:, 1] + rot[:, 2, 1, :] * vec[:, 2])[:, None, ...],
         (rot[:, 0, 2, :] * vec[:, 0] + rot[:, 1, 2, :] * vec[:, 1] + rot[:, 2, 2, :] * vec[:, 2])[:, None, ...]),
        axis=1)


def batch_invert_point(transformed_point, rotation, translation, extra_dims=0):
    """Apply inverse of transformation to a point.

    Args:
    transformed_point: List of 3 tensors to apply affine
    extra_dims:  Number of dimensions at the end of the transformed_point
    shape that are not present in the rotation and translation.  The most
    common use is rotation N points at once with extra_dims=1 for use in a
    network.

    Returns:
    Transformed point after applying affine.
    """
    for _ in range(extra_dims):
        rotation = mnp.expand_dims(rotation, axis=-1)
        translation = mnp.expand_dims(translation, axis=-1)
    rot_point = transformed_point - translation
    return batch_apply_inverse_rot_to_vec(rotation, rot_point)


def compute_confidence(predicted_lddt_logits):
    """compute confidence"""

    num_bins = predicted_lddt_logits.shape[-1]
    bin_width = 1 / num_bins
    start_n = bin_width / 2
    plddt = compute_plddt(predicted_lddt_logits, start_n, bin_width)
    confidence = np.mean(plddt)
    return confidence


def compute_plddt(logits, start_n, bin_width):
    """Computes per-residue pLDDT from logits.

    Args:
      logits: [num_res, num_bins] output from the PredictedLDDTHead.

    Returns:
      plddt: [num_res] per-residue pLDDT.
    """
    bin_centers = np.arange(start=start_n, stop=1.0, step=bin_width)
    probs = softmax(logits, axis=-1)
    predicted_lddt_ca = np.sum(probs * bin_centers[None, :], axis=-1)
    return predicted_lddt_ca * 100
