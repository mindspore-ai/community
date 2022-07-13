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
"""Simulation"""
import numpy as np

import mindspore.common.dtype as mstype
from mindspore import Tensor
from mindspore import nn
from mindspore.common.parameter import Parameter
from mindspore.ops import operations as P
from mindsponge import Bond
from mindsponge import MdInformation


class Controller:
    """Controller"""

    def __init__(self, args_opt):
        self.input_file = args_opt['i']
        self.initial_coordinates_file = args_opt['c']
        self.amber_parm = args_opt['amber_parm']
        self.restrt = args_opt['r']
        self.mdcrd = args_opt['x']
        self.mdout = args_opt['o']
        self.mdbox = args_opt['box']

        self.command_set = {}
        self.md_task = None
        self.commands_from_in_file()
        self.punctuation = ","

    def commands_from_in_file(self):
        """command from in file"""
        file = open(self.input_file, 'r')
        context = file.readlines()
        file.close()
        self.md_task = context[0].strip()
        for val in context:
            val = val.strip()
            if val and val[0] != '#' and ("=" in val):
                val = val[:val.index(",")] if ',' in val else val
                assert len(val.strip().split("=")) == 2
                flag, value = val.strip().split("=")
                value = value.replace(" ", "")
                flag = flag.replace(" ", "")
                if flag not in self.command_set:
                    self.command_set[flag] = value
                else:
                    print("ERROR COMMAND FILE")


class Simulation(nn.Cell):
    """simulation"""

    def __init__(self, args_opt):
        super(Simulation, self).__init__()
        self.control = Controller(args_opt)
        self.md_info = MdInformation(self.control)
        self.mode = self.md_info.mode
        self.bond = Bond(self.control)
        self.atom_numbers = self.md_info.atom_numbers
        self.residue_numbers = self.md_info.residue_numbers
        self.bond_numbers = self.bond.bond_numbers
        self.init_tensor()
        self.op_define()

    def init_tensor(self):
        """init tensor"""
        self.crd = Parameter(
            Tensor(np.array(self.md_info.coordinate).reshape([self.atom_numbers, 3]), mstype.float32),
            requires_grad=False)
        self.crd_to_uint_crd_cof = Tensor(np.asarray(self.md_info.pbc.crd_to_uint_crd_cof, np.float32), mstype.float32)
        self.uint_dr_to_dr_cof = Parameter(Tensor(self.md_info.pbc.uint_dr_to_dr_cof, mstype.float32),
                                           requires_grad=False)
        self.bond_atom_a = Tensor(np.asarray(self.bond.h_atom_a, np.int32), mstype.int32)
        self.bond_atom_b = Tensor(np.asarray(self.bond.h_atom_b, np.int32), mstype.int32)
        self.bond_k = Tensor(np.asarray(self.bond.h_k, np.float32), mstype.float32)
        self.bond_r0 = Tensor(np.asarray(self.bond.h_r0, np.float32), mstype.float32)

    def op_define(self):
        """op define"""
        self.crd_to_uint_crd = P.CrdToUintCrd(self.atom_numbers)
        self.bond_energy = P.BondEnergy(self.bond_numbers, self.atom_numbers)

    def simulation_beforce_caculate_force(self):
        """simulation before calculate force"""
        crd_to_uint_crd_cof = 0.5 * self.crd_to_uint_crd_cof
        uint_crd = self.crd_to_uint_crd(crd_to_uint_crd_cof, self.crd)
        return uint_crd

    def simulation_caculate_energy(self, uint_crd, uint_dr_to_dr_cof):
        """simulation calculate energy"""
        bond_energy = self.bond_energy(uint_crd, uint_dr_to_dr_cof, self.bond_atom_a, self.bond_atom_b, self.bond_k,
                                       self.bond_r0)
        bond_energy_sum = P.ReduceSum(True)(bond_energy)

        return bond_energy_sum

    def construct(self):
        """construct"""
        uint_crd = self.simulation_beforce_caculate_force()
        bond_energy_sum = self.simulation_caculate_energy(uint_crd, self.uint_dr_to_dr_cof)
        return bond_energy_sum
