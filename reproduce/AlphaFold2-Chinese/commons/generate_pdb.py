"""generate pdb file"""

import dataclasses
import numpy as np

from commons import residue_constants


@dataclasses.dataclass(frozen=True)
class Protein:
    """Protein structure representation."""

    # Cartesian coordinates of atoms in angstroms. The atom types correspond to
    # residue_constants.atom_types, i.e. the first three are N, CA, CB.
    atom_positions: np.ndarray  # [num_res, num_atom_type, 3]

    # Amino-acid type for each residue represented as an integer between 0 and
    # 20, where 20 is 'X'.
    aatype: np.ndarray  # [num_res]

    # Binary float mask to indicate presence of a particular atom. 1.0 if an atom
    # is present and 0.0 if not. This should be used for loss masking.
    atom_mask: np.ndarray  # [num_res, num_atom_type]

    # Residue index as used in PDB. It is not necessarily continuous or 0-indexed.
    residue_index: np.ndarray  # [num_res]

    # B-factors, or temperature factors, of each residue (in sq. angstroms units),
    # representing the displacement of the residue from its ground truth mean
    # value.
    b_factors: np.ndarray  # [num_res, num_atom_type]


def from_prediction(final_atom_mask, aatype, final_atom_positions, residue_index):
    """Assembles a protein from a prediction.

    Args:
      final_atom_mask: atom mask info from structure module.
      aatype: amino acid type info.
      final_atom_positions: final atom positions from structure module
      residue_index: from processed_features

    Returns:
      A protein instance.
    """
    dist_per_residue = np.zeros_like(final_atom_mask)

    return Protein(
        aatype=aatype,
        atom_positions=final_atom_positions,
        atom_mask=final_atom_mask,
        residue_index=residue_index + 1,
        b_factors=dist_per_residue)


def to_pdb(prot: Protein):
    """Converts a `Protein` instance to a PDB string.

    Args:
      prot: The protein to convert to PDB.

    Returns:
      PDB string.
    """
    restypes = residue_constants.restypes + ['X']
    res_1to3 = lambda r: residue_constants.restype_1to3.get(restypes[r], 'UNK')
    atom_types = residue_constants.atom_types

    pdb_lines = []

    atom_mask = prot.atom_mask
    aatype = prot.aatype
    atom_positions = prot.atom_positions
    residue_index = prot.residue_index.astype(np.int32)
    b_factors = prot.b_factors

    if (aatype > residue_constants.restype_num).any():
        raise ValueError('Invalid aatypes.')

    pdb_lines.append('MODEL     1')
    atom_index = 1
    chain_id = 'A'
    # Add all atom sites.
    for i in range(aatype.shape[0]):
        res_name_3 = res_1to3(aatype[i])
        for atom_name, pos, mask, b_factor in zip(
                atom_types, atom_positions[i], atom_mask[i], b_factors[i]):
            if mask < 0.5:
                continue

            record_type = 'ATOM'
            name = atom_name if len(atom_name) == 4 else f' {atom_name}'
            alt_loc = ''
            insertion_code = ''
            occupancy = 1.00
            element = atom_name[0]  # Protein supports only C, N, O, S, this works.
            charge = ''
            # PDB is a columnar format, every space matters here!
            atom_line = (f'{record_type:<6}{atom_index:>5} {name:<4}{alt_loc:>1}'
                         f'{res_name_3:>3} {chain_id:>1}'
                         f'{residue_index[i]:>4}{insertion_code:>1}   '
                         f'{pos[0]:>8.3f}{pos[1]:>8.3f}{pos[2]:>8.3f}'
                         f'{occupancy:>6.2f}{b_factor:>6.2f}          '
                         f'{element:>2}{charge:>2}')
            pdb_lines.append(atom_line)
            atom_index += 1

    # Close the chain.
    chain_end = 'TER'
    chain_termination_line = (
        f'{chain_end:<6}{atom_index:>5}      {res_1to3(aatype[-1]):>3} '
        f'{chain_id:>1}{residue_index[-1]:>4}')
    pdb_lines.append(chain_termination_line)
    pdb_lines.append('ENDMDL')

    pdb_lines.append('END')
    pdb_lines.append('')
    return '\n'.join(pdb_lines)
