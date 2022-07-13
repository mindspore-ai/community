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
"""serving config for mindspore serving"""

import time
import os
import json
import numpy as np

from mindspore_serving.server import register
import mindspore.context as context
from mindspore.common.tensor import Tensor
from mindspore import load_checkpoint

from data.feature.feature_extraction import process_features
from data.tools.data_process import data_process
from commons.utils import compute_confidence
from commons.generate_pdb import to_pdb, from_prediction
from model import AlphaFold
from config import config, global_config
from fold_service.config import config as serving_config

context.set_context(mode=context.GRAPH_MODE,
                    device_target="Ascend",
                    variable_memory_max_size="31GB",
                    device_id=serving_config.device_id,
                    save_graphs=False)
model_name = "model_1"
model_config = config.model_config(model_name)
num_recycle = model_config.model.num_recycle
global_config = global_config.global_config(serving_config.seq_length)
extra_msa_length = global_config.extra_msa_length

fold_net = AlphaFold(model_config, global_config)
load_checkpoint(serving_config.ckpt_path, fold_net)

def fold_model(input_fasta_path):
    """defining fold model"""

    seq_files = os.listdir(input_fasta_path)
    for seq_file in seq_files:
        print(seq_file)
        t1 = time.time()
        seq_name = seq_file.split('.')[0]

        input_features = data_process(seq_name, serving_config)
        tensors, aatype, residue_index, ori_res_length = process_features(
            raw_features=input_features, config=model_config, global_config=global_config)
        prev_pos = Tensor(np.zeros([global_config.seq_length, 37, 3]).astype(np.float16))
        prev_msa_first_row = Tensor(np.zeros([global_config.seq_length, 256]).astype(np.float16))
        prev_pair = Tensor(np.zeros([global_config.seq_length, global_config.seq_length, 128]).astype(np.float16))

        t2 = time.time()
        for i in range(num_recycle+1):
            tensors_i = [tensor[i] for tensor in tensors]
            input_feats = [Tensor(tensor) for tensor in tensors_i]
            final_atom_positions, final_atom_mask, predicted_lddt_logits,\
                prev_pos, prev_msa_first_row, prev_pair = fold_net(*input_feats,
                                                                   prev_pos,
                                                                   prev_msa_first_row,
                                                                   prev_pair)

        t3 = time.time()

        final_atom_positions = final_atom_positions.asnumpy()[:ori_res_length]
        final_atom_mask = final_atom_mask.asnumpy()[:ori_res_length]
        predicted_lddt_logits = predicted_lddt_logits.asnumpy()[:ori_res_length]

        confidence = compute_confidence(predicted_lddt_logits)
        unrelaxed_protein = from_prediction(final_atom_mask, aatype[0], final_atom_positions, residue_index[0])
        pdb_file = to_pdb(unrelaxed_protein)

        seq_length = aatype.shape[-1]
        os.makedirs(f'./result/seq_{seq_name}_{seq_length}', exist_ok=True)

        with open(os.path.join(f'./result/seq_{seq_name}_{seq_length}/', f'unrelaxed_model_{seq_name}.pdb'), 'w') as f:
            f.write(pdb_file)
        t4 = time.time()
        timings = {"pre_process_time": round(t2 - t1, 2),
                   "model_time": round(t3 - t2, 2),
                   "pos_process_time": round(t4 - t3, 2),
                   "all_time": round(t4 - t1, 2),
                   "confidence": confidence}
        print(timings)
        with open(f'./result/seq_{seq_name}_{seq_length}/timings', 'w') as f:
            f.write(json.dumps(timings))
    return True

@register.register_method(output_names=["res"])
def folding(input_fasta_path):
    res = register.add_stage(fold_model, input_fasta_path, outputs_count=1)
    return res
