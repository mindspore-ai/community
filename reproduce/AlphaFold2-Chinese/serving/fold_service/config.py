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
"""config for serving mode"""

import ml_collections

config = ml_collections.ConfigDict({
    "seq_length": 256,
    "device_id": 0,
    "port": 5500,
    "ckpt_path": "/CHECKPOINT_PATH",
    "input_fasta_path": "INPUT_FASTA_PATH",
    "msa_result_path": "MSA_RESULT_PATH",
    "database_dir": "DATABASE_DIR",
    "database_envdb_dir": "DATABASE_ENVDB_DIR",
    "hhsearch_binary_path": "HHSEARCH_BINARY_PATH",
    "pdb70_database_path": 'PDB&)_DATABASE_PATH',
    "template_mmcif_dir": 'TEMPLATE_MMCIF_DIR',
    "max_template_date": "MAX_TEMPLATE_DATE",
    "kalign_binary_path": 'KALIGN_BINARY_PATH',
    "obsolete_pdbs_path": 'OBSOLETE_PDBS_PATH',
})
