"""Model config."""

import copy
import ml_collections

def global_config(length: int) -> ml_collections.ConfigDict:
    """Get the global config."""
    if str(length) not in GLOBAL_CONFIG:
        raise ValueError(f'Invalid padding sequence length {length}.')
    cfg = copy.deepcopy(GLOBAL_CONFIG[str(length)])
    return cfg

GLOBAL_CONFIG = ml_collections.ConfigDict({
    "256": {
        'zero_init': True,
        'seq_length': 256,
        'extra_msa_length': 5120,
        'template_embedding': {
            'slice_num': 0,
        },
        'template_pair_stack': {
            'triangle_attention_starting_node': {
                'slice_num': 0,
            },
            'triangle_attention_ending_node': {
                'slice_num': 0,
            },
            'pair_transition': {
                'slice_num': 0,
            },
        },
        'extra_msa_stack': {
            'msa_transition': {
                'slice_num': 0,
            },
            'msa_row_attention_with_pair_bias': {
                'slice_num': 0,
            },
            'msa_column_global_attention': {
                'slice_num': 0,
            },
            'outer_product_mean': {
                'slice_num': 0,
            },
            'triangle_attention_starting_node': {
                'slice_num': 0,
            },
            'triangle_attention_ending_node': {
                'slice_num': 0,
            },
            'pair_transition': {
                'slice_num': 0,
            },
        },
        'evoformer_iteration': {
            'msa_transition': {
                'slice_num': 0,
            },
            'msa_row_attention_with_pair_bias': {
                'slice_num': 0,
            },
            'msa_column_attention': {
                'slice_num': 0,
            },
            'outer_product_mean': {
                'slice_num': 0,
            },
            'triangle_attention_starting_node': {
                'slice_num': 0,
            },
            'triangle_attention_ending_node': {
                'slice_num': 0,
            },
            'pair_transition': {
                'slice_num': 0,
            },
        },
    },
    "512": {
        'zero_init': True,
        'seq_length': 512,
        'extra_msa_length': 5120,
        'template_embedding': {
            'slice_num': 0,
        },
        'template_pair_stack': {
            'triangle_attention_starting_node': {
                'slice_num': 0,
            },
            'triangle_attention_ending_node': {
                'slice_num': 0,
            },
            'pair_transition': {
                'slice_num': 0,
            },
        },
        'extra_msa_stack': {
            'msa_transition': {
                'slice_num': 0,
            },
            'msa_row_attention_with_pair_bias': {
                'slice_num': 4,
            },
            'msa_column_global_attention': {
                'slice_num': 0,
            },
            'outer_product_mean': {
                'slice_num': 0,
            },
            'triangle_attention_starting_node': {
                'slice_num': 0,
            },
            'triangle_attention_ending_node': {
                'slice_num': 0,
            },
            'pair_transition': {
                'slice_num': 0,
            },
        },
        'evoformer_iteration': {
            'msa_transition': {
                'slice_num': 0,
            },
            'msa_row_attention_with_pair_bias': {
                'slice_num': 0,
            },
            'msa_column_attention': {
                'slice_num': 0,
            },
            'outer_product_mean': {
                'slice_num': 0,
            },
            'triangle_attention_starting_node': {
                'slice_num': 0,
            },
            'triangle_attention_ending_node': {
                'slice_num': 0,
            },
            'pair_transition': {
                'slice_num': 0,
            },
        },
    },
    "1024": {
        'zero_init': True,
        'seq_length': 1024,
        'extra_msa_length': 5120,
        'template_embedding': {
            'slice_num': 4,
        },
        'template_pair_stack': {
            'triangle_attention_starting_node': {
                'slice_num': 4,
            },
            'triangle_attention_ending_node': {
                'slice_num': 4,
            },
            'pair_transition': {
                'slice_num': 0,
            },
        },
        'extra_msa_stack': {
            'msa_transition': {
                'slice_num': 0,
            },
            'msa_row_attention_with_pair_bias': {
                'slice_num': 16,
            },
            'msa_column_global_attention': {
                'slice_num': 4,
            },
            'outer_product_mean': {
                'slice_num': 0,
            },
            'triangle_attention_starting_node': {
                'slice_num': 4,
            },
            'triangle_attention_ending_node': {
                'slice_num': 4,
            },
            'pair_transition': {
                'slice_num': 0,
            },
        },
        'evoformer_iteration': {
            'msa_transition': {
                'slice_num': 0,
            },
            'msa_row_attention_with_pair_bias': {
                'slice_num': 4,
            },
            'msa_column_attention': {
                'slice_num': 4,
            },
            'outer_product_mean': {
                'slice_num': 0,
            },
            'triangle_attention_starting_node': {
                'slice_num': 4,
            },
            'triangle_attention_ending_node': {
                'slice_num': 4,
            },
            'pair_transition': {
                'slice_num': 0,
            },
        },
    },
    "2048": {
        'zero_init': True,
        'seq_length': 2048,
        'extra_msa_length': 5120,
        'template_embedding': {
            'slice_num': 32,
        },
        'template_pair_stack': {
            'triangle_attention_starting_node': {
                'slice_num': 32,
            },
            'triangle_attention_ending_node': {
                'slice_num': 32,
            },
            'pair_transition': {
                'slice_num': 16,
            },
        },

        'extra_msa_stack': {
            'msa_transition': {
                'slice_num': 16,
            },
            'msa_row_attention_with_pair_bias': {
                'slice_num': 128,
            },
            'msa_column_global_attention': {
                'slice_num': 32,
            },
            'outer_product_mean': {
                'slice_num': 16,
            },
            'triangle_attention_starting_node': {
                'slice_num': 32,
            },
            'triangle_attention_ending_node': {
                'slice_num': 32,
            },
            'pair_transition': {
                'slice_num': 16,
            },
        },
        'evoformer_iteration': {
            'msa_transition': {
                'slice_num': 16,
            },
            'msa_row_attention_with_pair_bias': {
                'slice_num': 32,
            },
            'msa_column_attention': {
                'slice_num': 32,
            },
            'outer_product_mean': {
                'slice_num': 16,
            },
            'triangle_attention_starting_node': {
                'slice_num': 32,
            },
            'triangle_attention_ending_node': {
                'slice_num': 32,
            },
            'pair_transition': {
                'slice_num': 16,
            },
        },
    },
    "2304": {
        'zero_init': True,
        'seq_length': 2304,
        'extra_msa_length': 5120,
        'template_embedding': {
            'slice_num': 64,
        },
        'template_pair_stack': {
            'triangle_attention_starting_node': {
                'slice_num': 64,
            },
            'triangle_attention_ending_node': {
                'slice_num': 64,
            },
            'pair_transition': {
                'slice_num': 2,
            },
        },

        'extra_msa_stack': {
            'msa_transition': {
                'slice_num': 2,
            },
            'msa_row_attention_with_pair_bias': {
                'slice_num': 64,
            },
            'msa_column_global_attention': {
                'slice_num': 64,
            },
            'outer_product_mean': {
                'slice_num': 8,
            },
            'triangle_attention_starting_node': {
                'slice_num': 64,
            },
            'triangle_attention_ending_node': {
                'slice_num': 64,
            },
            'pair_transition': {
                'slice_num': 4,
            },
        },
        'evoformer_iteration': {
            'msa_transition': {
                'slice_num': 2,
            },
            'msa_row_attention_with_pair_bias': {
                'slice_num': 64,
            },
            'msa_column_attention': {
                'slice_num': 64,
            },
            'outer_product_mean': {
                'slice_num': 8,
            },
            'triangle_attention_starting_node': {
                'slice_num': 64,
            },
            'triangle_attention_ending_node': {
                'slice_num': 64,
            },
            'pair_transition': {
                'slice_num': 4,
            },
        },
    },
})
