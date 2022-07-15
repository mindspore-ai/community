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
'''data process'''
import os
import hashlib
import re
import numpy as np
from commons import residue_constants
from data.tools.parsers import parse_fasta, parse_hhr, parse_a3m
from data.tools.templates import TemplateHitFeaturizer
from data.tools.data_tools import HHSearch

def get_hash(x):
    return hashlib.sha1(x.encode()).hexdigest()

def run_mmseqs2(x, path, use_env=False):
    '''run mmseqs2'''
    a3m_files = [f"{path}/uniref.a3m"]
    if use_env: a3m_files.append(f"{path}/bfd.mgnify30.metaeuk30.smag30.a3m")

    # gather a3m lines
    a3m_lines = {}
    for a3m_file in a3m_files:
        update_m, m = True, None
        for line in open(a3m_file, "r"):
            if line:
                if "\x00" in line:
                    line = line.replace("\x00", "")
                    update_m = True
                if line.startswith(">") and update_m:

                    m = int(line[2:6].rstrip())
                    update_m = False
                    if m not in a3m_lines: a3m_lines[m] = []
                a3m_lines[m].append(line)

    # return results
    a3m_lines = ["".join(a3m_lines[key]) for key in a3m_lines]

    if isinstance(x, str):
        return a3m_lines[0]
    return a3m_lines


def make_sequence_features(
        sequence: str, description: str, num_res: int):
    """Constructs a feature dict of sequence features."""
    features = {'aatype': residue_constants.sequence_to_onehot(sequence=sequence,
                                                               mapping=residue_constants.restype_order_with_x,
                                                               map_unknown_to_x=True),
                'between_segment_residues': np.zeros((num_res,), dtype=np.int32),
                'domain_name': np.array([description.encode('utf-8')], dtype=np.object_),
                'residue_index': np.array(range(num_res), dtype=np.int32),
                'seq_length': np.array([num_res] * num_res, dtype=np.int32),
                'sequence': np.array([sequence.encode('utf-8')], dtype=np.object_)}
    return features


def make_msa_features(
        msas,
        deletion_matrices):
    """Constructs a feature dict of MSA features."""
    if not msas:
        raise ValueError('At least one MSA must be provided.')

    int_msa = []
    deletion_matrix = []
    seen_sequences = set()
    for msa_index, msa in enumerate(msas):
        if not msa:
            raise ValueError(f'MSA {msa_index} must contain at least one sequence.')
        for sequence_index, sequence in enumerate(msa):
            if sequence in seen_sequences:
                continue
            seen_sequences.add(sequence)
            int_msa.append(
                [residue_constants.HHBLITS_AA_TO_ID[res] for res in sequence])
            deletion_matrix.append(deletion_matrices[msa_index][sequence_index])

    num_res = len(msas[0][0])
    num_alignments = len(int_msa)
    features = {'deletion_matrix_int': np.array(deletion_matrix, dtype=np.int32),
                'msa': np.array(int_msa, dtype=np.int32),
                'num_alignments': np.array([num_alignments] * num_res, dtype=np.int32)}
    return features


class DataPipeline:
    """Runs the alignment tools and assembles the input features."""

    def __init__(self,
                 hhsearch_binary_path: str,
                 pdb70_database_path: str,
                 template_featurizer: TemplateHitFeaturizer,
                 result_path,
                 use_env=False):
        """Constructs a feature dict for a given FASTA file."""

        self.hhsearch_pdb70_runner = HHSearch(
            binary_path=hhsearch_binary_path,
            databases=[pdb70_database_path])
        self.template_featurizer = template_featurizer
        self.result_path = result_path
        self.use_env = use_env

    def process(self, input_fasta_path):
        """Runs alignment tools on the input sequence and creates features."""
        with open(input_fasta_path) as f:
            input_fasta_str = f.read()
        input_seqs, input_descs = parse_fasta(input_fasta_str)
        if len(input_seqs) != 1:
            raise ValueError(f'More than one input sequence found in {input_fasta_path}.')
        input_sequence = input_seqs[0]
        input_description = input_descs[0]

        num_res = len(input_sequence)

        # mmseq2
        sequence = input_sequence
        sequence = re.sub("[^A-Z:/]", "", sequence.upper())
        sequence = re.sub(":+", ":", sequence)
        sequence = re.sub("/+", "/", sequence)
        sequence = re.sub("^[:/]+", "", sequence)
        sequence = re.sub("[:/]+$", "", sequence)
        ori_sequence = sequence
        seqs = ori_sequence.replace("/", "").split(":")

        a3m_lines = run_mmseqs2(seqs, path=self.result_path, use_env=self.use_env)

        hhsearch_result = self.hhsearch_pdb70_runner.query(a3m_lines[0])
        hhsearch_hits = parse_hhr(hhsearch_result)

        msas, deletion_matrices = parse_a3m(a3m_lines[0])
        templates_result = self.template_featurizer.get_templates(
            query_sequence=input_sequence,
            query_pdb_code=None,
            query_release_date=None,
            hhr_hits=hhsearch_hits)
        sequence_features = make_sequence_features(
            sequence=input_sequence,
            description=input_description,
            num_res=num_res)
        msa_features = make_msa_features(
            msas=(msas,),
            deletion_matrices=(deletion_matrices,
                               ))
        return {**sequence_features, **msa_features, **templates_result.features}


def data_process(seq_name, args):
    """data_process"""

    fasta_path = os.path.join(args.input_fasta_path, seq_name + '.fasta')
    result_path = os.path.join(args.msa_result_path, "/result_" + str(seq_name))
    if args.database_envdb_dir:
        use_env = True
        command = "sh ./data/tools/msa_search.sh mmseqs " + fasta_path + " " + result_path + " " + \
                  args.database_dir + " " + "\"\"" + " " + args.database_envdb_dir + " \"1\" \"0\" \"1\""
    else:
        use_env = False
        command = "sh ./data/tools/msa_search.sh mmseqs " + fasta_path + " " + result_path + " " + \
                  args.database_dir + " " + "\"\"" + " \"\"" + " \"0\" \"0\" \"1\""
    print('start mmseqs2 MSA')
    print('command: ', command)
    os.system(command)
    print('mmseqs2 MSA successful')
    print('use_env: ', use_env)
    hhsearch_binary_path = args.hhsearch_binary_path

    pdb70_database_path = args.pdb70_database_path
    template_mmcif_dir = args.template_mmcif_dir
    max_template_date = args.max_template_date
    kalign_binary_path = args.kalign_binary_path
    obsolete_pdbs_path = args.obsolete_pdbs_path

    template_featurizer = TemplateHitFeaturizer(
        mmcif_dir=template_mmcif_dir,
        max_template_date=max_template_date,
        max_hits=20,
        kalign_binary_path=kalign_binary_path,
        release_dates_path=None,
        obsolete_pdbs_path=obsolete_pdbs_path)

    data_pipeline = DataPipeline(

        hhsearch_binary_path=hhsearch_binary_path,
        pdb70_database_path=pdb70_database_path,
        template_featurizer=template_featurizer,
        result_path=result_path,
        use_env=use_env)

    feature_dict = data_pipeline.process(fasta_path)
    return feature_dict
