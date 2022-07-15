"""Transformations for 3D coordinates."""

import mindspore.numpy as mnp


def vecs_sub(v1, v2):
    """Computes v1 - v2."""
    return v1 - v2


def vecs_robust_norm(v, epsilon=1e-8):
    """Computes norm of vectors 'v'."""

    return mnp.sqrt(mnp.sum(mnp.square(v), axis=-1) + epsilon)


def vecs_robust_normalize(v, epsilon=1e-8):
    """Normalizes vectors 'v'."""

    norms = vecs_robust_norm(v, epsilon)
    return v / norms[..., None]


def vecs_dot_vecs(v1, v2):
    """Dot product of vectors 'v1' and 'v2'."""
    return mnp.sum(v1 * v2, axis=-1)


def vecs_cross_vecs(v1, v2):
    """Cross product of vectors 'v1' and 'v2'."""

    return mnp.concatenate(((v1[..., 1] * v2[..., 2] - v1[..., 2] * v2[..., 1])[..., None],
                            (v1[..., 2] * v2[..., 0] - v1[..., 0] * v2[..., 2])[..., None],
                            (v1[..., 0] * v2[..., 1] - v1[..., 1] * v2[..., 0])[..., None]), axis=-1)


def rots_from_two_vecs(e0_unnormalized, e1_unnormalized):
    """Create rotation matrices from unnormalized vectors for the x and y-axes."""

    # Normalize the unit vector for the x-axis, e0.
    e0 = vecs_robust_normalize(e0_unnormalized)

    # make e1 perpendicular to e0.
    c = vecs_dot_vecs(e1_unnormalized, e0)
    e1 = e1_unnormalized - c[..., None] * e0
    e1 = vecs_robust_normalize(e1)

    # Compute e2 as cross product of e0 and e1.
    e2 = vecs_cross_vecs(e0, e1)

    rots = mnp.concatenate(
        (mnp.concatenate([e0[..., 0][None, ...], e1[..., 0][None, ...], e2[..., 0][None, ...]], axis=0)[None, ...],
         mnp.concatenate([e0[..., 1][None, ...], e1[..., 1][None, ...], e2[..., 1][None, ...]], axis=0)[None, ...],
         mnp.concatenate([e0[..., 2][None, ...], e1[..., 2][None, ...], e2[..., 2][None, ...]], axis=0)[None, ...]),
        axis=0)
    return rots


def rigids_from_3_points(
        point_on_neg_x_axis,  # shape (...)
        origin,  # shape (...)
        point_on_xy_plane,  # shape (...)
):  # shape (...)
    """Create Rigids from 3 points. """

    m = rots_from_two_vecs(
        e0_unnormalized=vecs_sub(origin, point_on_neg_x_axis),
        e1_unnormalized=vecs_sub(point_on_xy_plane, origin))
    return m, origin


def invert_rots(m):
    """Computes inverse of rotations 'm'."""

    return mnp.transpose(m, (1, 0, 2, 3, 4))


def rots_mul_vecs(m, v):
    """Apply rotations 'm' to vectors 'v'."""

    return mnp.concatenate(((m[0][0] * v[..., 0] + m[0][1] * v[..., 1] + m[0][2] * v[..., 2])[..., None],
                            (m[1][0] * v[..., 0] + m[1][1] * v[..., 1] + m[1][2] * v[..., 2])[..., None],
                            (m[2][0] * v[..., 0] + m[2][1] * v[..., 1] + m[2][2] * v[..., 2])[..., None]), axis=-1)


def invert_rigids(rot, trans):
    """Computes group inverse of rigid transformations 'r'."""

    inv_rots = invert_rots(rot)
    t = rots_mul_vecs(inv_rots, trans)
    inv_trans = -t
    return inv_rots, inv_trans


def vecs_add(v1, v2):
    """Add two vectors 'v1' and 'v2'."""

    return v1 + v2


def rigids_mul_vecs(rot, trans, v):
    """Apply rigid transforms 'r' to points 'v'."""

    return vecs_add(rots_mul_vecs(rot, v), trans)
