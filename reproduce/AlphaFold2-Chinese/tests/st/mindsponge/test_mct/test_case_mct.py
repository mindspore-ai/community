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
"""Test case mct"""

import time
import numpy as np
import pytest
from mindspore import context, load_checkpoint, ops, nn, Tensor

import mindspore.numpy as msnp
import mindspore.common.dtype as mstype
from mindspore.common.parameter import Parameter
from mindspore.ops import functional as F
from mindspore.ops import operations as P
from mindspore.ops import constexpr
from mindspore.ops import composite as C

from mindsponge import Angle
from mindsponge import Bond
from mindsponge import Dihedral
from mindsponge import LennardJonesInformation
from mindsponge import NonBond14
from mindsponge import ParticleMeshEwald
from mindsponge import LangevinLiujian
from mindsponge import MdInformation
from mindsponge import NeighborList
from mindsponge.md.cybertron.meta_dynamics import Bias
from mindsponge.md.cybertron.units import units
from mindsponge.md.cybertron.models import MolCT
from mindsponge.md.cybertron.readouts import AtomwiseReadout
from mindsponge.md.cybertron.cybertron import Cybertron

standard_normal = ops.StandardNormal()
zeros = ops.Zeros()

WALL_P = 9e08
WALL_POTENTIAL = np.zeros(200, dtype=np.float32)
WALL_POTENTIAL[0] = WALL_P
WALL_POTENTIAL[1] = WALL_P
WALL_POTENTIAL[2] = WALL_P
WALL_POTENTIAL[-1] = WALL_P
WALL_POTENTIAL[-2] = WALL_P
WALL_POTENTIAL[-3] = WALL_P
SMIN = 0
SMAX = 8
DS = 0.04
OMEGA = 50
SIGMA = 0.005
DDT = 0.001
T = 300
ALPHA = 0.5
GAMMA = 6
KAPPA = 4
UPPER_BOUND_INDEX = 190
LOWER_BOUND_INDEX = 10
WALL_FACTOR = 0.1

@constexpr
def get_full_tensor(shape, fill_value, dtype=np.float32):
    '''get_full_tensor'''
    return msnp.full(shape, fill_value, dtype)


class Controller:
    '''controller'''

    def __init__(self, args_opt):
        self.input_file = args_opt.i
        self.initial_coordinates_file = args_opt.c
        self.amber_parm = args_opt.amber_parm
        self.restrt = args_opt.r
        self.mdcrd = args_opt.x
        self.mdout = args_opt.o
        self.mdbox = args_opt.box
        self.meta = args_opt.meta
        self.with_box = args_opt.with_box
        self.np_iter = args_opt.np_iter
        self.command_set = {}
        self.md_task = None
        self.commands_from_in_file()

    def commands_from_in_file(self):
        '''command from in file'''
        file = open(self.input_file, 'r')
        ct = file.readlines()
        file.close()
        self.md_task = ct[0].strip()
        for val in ct:
            if "=" in val:
                assert len(val.strip().split("=")) == 2
                flag, value = val.strip().split("=")
                value = value.replace(",", '')
                flag = flag.replace(" ", "")
                if flag not in self.command_set:
                    self.command_set[flag] = value
                else:
                    print("ERROR COMMAND FILE")

class SimulationCybertron(nn.Cell):
    '''simulation'''

    def __init__(self, args_opt, network=None):
        super().__init__()
        self.control = Controller(args_opt)
        if self.control.meta:
            self.meta = Tensor([1], mstype.int32)
        else:
            self.meta = Tensor([0], mstype.int32)
        self.md_info = MdInformation(self.control)
        self.bond = Bond(self.control)
        self.angle = Angle(self.control)
        self.dihedral = Dihedral(self.control)
        self.nb14 = NonBond14(self.control, self.dihedral, self.md_info.atom_numbers)
        self.nb_info = NeighborList(self.control, self.md_info.atom_numbers, self.md_info.box_length)
        self.lj_info = LennardJonesInformation(self.control, self.md_info.nb.cutoff, self.md_info.sys.box_length)
        self.liujian_info = LangevinLiujian(self.control, self.md_info.atom_numbers)
        self.pme_method = ParticleMeshEwald(self.control, self.md_info)
        self.bond_energy_sum = Tensor(0, mstype.int32)
        self.angle_energy_sum = Tensor(0, mstype.int32)
        self.dihedral_energy_sum = Tensor(0, mstype.int32)
        self.nb14_lj_energy_sum = Tensor(0, mstype.int32)
        self.nb14_cf_energy_sum = Tensor(0, mstype.int32)
        self.lj_energy_sum = Tensor(0, mstype.int32)
        self.ee_ene = Tensor(0, mstype.int32)
        self.total_energy = Tensor(0, mstype.int32)
        # Init scalar
        self.ntwx = self.md_info.ntwx
        self.atom_numbers = self.md_info.atom_numbers
        self.residue_numbers = self.md_info.residue_numbers
        self.bond_numbers = self.bond.bond_numbers
        self.angle_numbers = self.angle.angle_numbers
        self.dihedral_numbers = self.dihedral.dihedral_numbers
        self.nb14_numbers = self.nb14.nb14_numbers
        self.nxy = self.nb_info.nxy
        self.grid_numbers = self.nb_info.grid_numbers
        self.max_atom_in_grid_numbers = self.nb_info.max_atom_in_grid_numbers
        self.max_neighbor_numbers = self.nb_info.max_neighbor_numbers
        self.excluded_atom_numbers = self.nb_info.excluded_atom_numbers
        self.refresh_count = Parameter(Tensor(self.nb_info.refresh_count, mstype.int32), requires_grad=False)
        self.refresh_interval = self.nb_info.refresh_interval
        self.skin = self.nb_info.skin
        self.cutoff = self.nb_info.cutoff
        self.cutoff_square = self.nb_info.cutoff_square
        self.cutoff_with_skin = self.nb_info.cutoff_with_skin
        self.half_cutoff_with_skin = self.nb_info.half_cutoff_with_skin
        self.cutoff_with_skin_square = self.nb_info.cutoff_with_skin_square
        self.half_skin_square = self.nb_info.half_skin_square
        self.beta = self.pme_method.beta
        self.fftx = self.pme_method.fftx
        self.ffty = self.pme_method.ffty
        self.fftz = self.pme_method.fftz
        self.random_seed = self.liujian_info.random_seed
        self.dt = self.liujian_info.dt
        self.half_dt = self.liujian_info.half_dt
        self.exp_gamma = self.liujian_info.exp_gamma

        self.tmp_forces = Tensor(np.zeros((self.atom_numbers, 3)), dtype=mstype.float32)

        self.bias_potential = Parameter(Tensor(WALL_POTENTIAL, mstype.float32), requires_grad=True)
        self.grid_num = 200
        self.wall_potential = WALL_P

        self.meta_interval = 5

        self.wall_factor = WALL_FACTOR
        self.upper_bound_index = UPPER_BOUND_INDEX
        self.lower_bound_index = LOWER_BOUND_INDEX
        self.kappa = KAPPA
        self.smin = (Tensor(SMIN, mstype.float32),)
        self.smax = SMAX
        self.t = T
        self.alpha = ALPHA
        self.gamma = GAMMA
        self.ds = DS
        self.ddt = DDT
        self.sum = ops.ReduceSum()
        self.omega = OMEGA
        self.sigma = Tensor(SIGMA, mstype.float32)
        self.exp = ops.Exp()
        self.square = ops.Square()
        self.sqrt = ops.Sqrt()
        self.zeros = ops.Zeros()
        self.ones = ops.Ones()
        self.norm = nn.Norm()
        self.add = ops.Add()
        self.cast = ops.Cast()
        self.cv_list = Tensor(np.arange(SMIN, SMAX, DS, dtype=np.float32)[0:self.grid_num], dtype=mstype.float32)
        self.init_tensor()
        self.op_define()
        self.update = False
        self.constant_random_force = Tensor(np.zeros([self.atom_numbers, 3], np.float32), mstype.float32)
        self.max_vel = 20
        self.hsigmoid = nn.HSigmoid()
        self.one_hill = Tensor([1], mstype.int32)
        self.sqrt2 = Tensor(np.sqrt(2), mstype.float32)
        self.kb = units.boltzmann()
        self.kbt = self.kb * self.t
        self.beta = 1.0 / self.kbt
        self.wt_factor = -1.0 / (self.gamma - 1.0) * self.beta

        self.network = network
        self.index_add = ops.IndexAdd(axis=-1)
        self.bias = Bias
        self.keep_sum = P.ReduceSum(keep_dims=True)
        self.grad = C.GradOperation()
        self.squeeze = P.Squeeze(0)
        self.file = None

    def init_tensor(self):
        '''init tensor'''
        self.hills = Parameter(Tensor(np.zeros(self.grid_num), mstype.float32), requires_grad=False)
        self.crd = Parameter(
            Tensor(np.float32(np.asarray(self.md_info.coordinate).reshape([self.atom_numbers, 3])), mstype.float32),
            requires_grad=False)
        self.crd_to_uint_crd_cof = Tensor(np.asarray(self.md_info.pbc.crd_to_uint_crd_cof, np.float32), mstype.float32)
        self.uint_dr_to_dr_cof = Parameter(
            Tensor(np.asarray(self.md_info.pbc.uint_dr_to_dr_cof, np.float32), mstype.float32), requires_grad=False)
        self.box_length = Tensor(self.md_info.box_length, mstype.float32)
        self.virtual_box_length = Tensor([0., 0., 0.], mstype.float32)
        self.charge = Parameter(Tensor(np.asarray(self.md_info.h_charge, dtype=np.float32), mstype.float32),
                                requires_grad=False)
        self.old_crd = Parameter(Tensor(np.zeros([self.atom_numbers, 3], dtype=np.float32), mstype.float32),
                                 requires_grad=False)
        self.last_crd = Parameter(Tensor(np.zeros([self.atom_numbers, 3], dtype=np.float32), mstype.float32),
                                  requires_grad=False)
        self.uint_crd = Parameter(Tensor(np.zeros([self.atom_numbers, 3], dtype=np.uint32), mstype.uint32),
                                  requires_grad=False)
        self.mass_inverse = Tensor(self.md_info.h_mass_inverse, mstype.float32)
        self.res_start = Tensor(self.md_info.h_res_start, mstype.int32)
        self.res_end = Tensor(self.md_info.h_res_end, mstype.int32)
        self.mass = Tensor(self.md_info.h_mass, mstype.float32)
        self.velocity = Parameter(Tensor(self.md_info.velocity, mstype.float32), requires_grad=False)
        self.acc = Parameter(Tensor(np.zeros([self.atom_numbers, 3], np.float32), mstype.float32), requires_grad=False)
        self.grid_n = Tensor(self.nb_info.grid_n, mstype.int32)
        self.grid_length_inverse = Tensor(self.nb_info.grid_length_inverse, mstype.float32)
        self.bucket = Parameter(Tensor(
            np.asarray(self.nb_info.bucket, np.int32).reshape([self.grid_numbers, self.max_atom_in_grid_numbers]),
            mstype.int32), requires_grad=False)
        self.atom_numbers_in_grid_bucket = Parameter(Tensor(self.nb_info.atom_numbers_in_grid_bucket, mstype.int32),
                                                     requires_grad=False)
        self.atom_in_grid_serial = Parameter(Tensor(np.zeros([self.nb_info.atom_numbers,], np.int32), mstype.int32),
                                             requires_grad=False)
        self.pointer = Parameter(
            Tensor(np.asarray(self.nb_info.pointer, np.int32).reshape([self.grid_numbers, 125]), mstype.int32),
            requires_grad=False)
        self.nl_atom_numbers = Parameter(Tensor(np.zeros([self.atom_numbers,], np.int32), mstype.int32),
                                         requires_grad=False)
        self.nl_atom_serial = Parameter(
            Tensor(np.zeros([self.atom_numbers, self.max_neighbor_numbers], np.int32), mstype.int32),
            requires_grad=False)

        self.excluded_list_start = Tensor(np.asarray(self.nb_info.excluded_list_start, np.int32), mstype.int32)
        self.excluded_list = Tensor(np.asarray(self.nb_info.excluded_list, np.int32), mstype.int32)
        self.excluded_numbers = Tensor(np.asarray(self.nb_info.excluded_numbers, np.int32), mstype.int32)
        self.need_refresh_flag = Tensor(np.asarray([0], np.int32), mstype.int32)
        self.sqrt_mass = Tensor(self.liujian_info.h_sqrt_mass, mstype.float32)
        self.rand_state = Parameter(Tensor(self.liujian_info.rand_state, mstype.float32))
        self.zero_fp_tensor = Tensor(np.asarray([0,], np.float32))

    def op_define(self):
        '''op define'''
        self.mdtemp = P.MDTemperature(self.residue_numbers, self.atom_numbers)
        self.setup_random_state = P.MDIterationSetupRandState(self.atom_numbers, self.random_seed)

        self.md_iteration_leap_frog_liujian = P.MDIterationLeapFrogLiujian(self.atom_numbers, self.half_dt, self.dt,
                                                                           self.exp_gamma)

        self.neighbor_list_update_init = P.NeighborListUpdate(grid_numbers=self.grid_numbers,
                                                              atom_numbers=self.atom_numbers, not_first_time=0,
                                                              nxy=self.nxy,
                                                              excluded_atom_numbers=self.excluded_atom_numbers,
                                                              cutoff_square=self.cutoff_square,
                                                              half_skin_square=self.half_skin_square,
                                                              cutoff_with_skin=self.cutoff_with_skin,
                                                              half_cutoff_with_skin=self.half_cutoff_with_skin,
                                                              cutoff_with_skin_square=self.cutoff_with_skin_square,
                                                              refresh_interval=self.refresh_interval,
                                                              cutoff=self.cutoff, skin=self.skin,
                                                              max_atom_in_grid_numbers=self.max_atom_in_grid_numbers,
                                                              max_neighbor_numbers=self.max_neighbor_numbers)

        self.random_force = Tensor(np.zeros([self.atom_numbers, 3], np.float32), mstype.float32)

    def update_hills(self, index, value):
        hills = ops.TensorScatterAdd()(self.hills,
                                       F.expand_dims(index, -1),
                                       F.expand_dims(self.cast(value, mstype.float32), -1))
        return hills

    def simulation_caculate_cybertron_force(self, positions, step, atom_types=None):
        """simulation_caculate_cybertron_force"""
        forces = -1 * self.grad(self.network)(positions,
                                              atom_types,
                                              None,
                                              None)
        cv = self.norm(self.add(self.last_crd[11], -self.last_crd[14]))
        cv_index = self.cast((cv - self.smin) / self.ds, mstype.int32)
        cv_index = cv_index * (cv_index >= 0)
        cv_index = cv_index * (cv_index < self.grid_num) + (self.grid_num - 1) * (cv_index >= self.grid_num)
        self.hills = self.update_hills(cv_index, step % self.meta_interval == 0)
        bias_cell = self.bias(self.hills,
                              smin=self.smin,
                              smax=self.smax,
                              ds=self.ds,
                              omega=self.omega,
                              sigma=self.sigma,
                              dt=self.ddt,
                              t=self.t,
                              alpha=self.alpha,
                              gamma=self.gamma,
                              wall_potential=self.wall_potential,
                              kappa=self.kappa,
                              upper_bound=self.upper_bound_index,
                              lower_bound=self.lower_bound_index,
                              factor=self.wall_factor)
        entropy_force = self.grad(bias_cell)(self.last_crd)
        tforces = P.AddN()([self.squeeze(forces), -self.meta * entropy_force])
        return tforces

    def simulation_caculate_cybertron_energy(self, positions, atom_types=None):
        energy = self.network(positions, atom_types, None, None)
        energy = self.squeeze(energy)
        return energy

    def simulation_temperature(self):
        '''caculate temperature'''
        res_ek_energy = self.mdtemp(self.res_start, self.res_end, self.velocity, self.mass)
        temperature = P.ReduceSum()(res_ek_energy)
        return temperature

    def simulation_mditeration_leapfrog_liujian(self, inverse_mass, sqrt_mass_inverse, crd, frc, rand_state,
                                                random_frc):
        '''simulation leap frog iteration liujian'''
        crd = self.md_iteration_leap_frog_liujian(inverse_mass, sqrt_mass_inverse, self.velocity, crd, frc, self.acc,
                                                  rand_state, random_frc)

        vel = F.depend(self.velocity, crd)
        vel = (self.hsigmoid(vel * 3 / self.max_vel) - 0.5) * 2 * self.max_vel
        acc = F.depend(self.acc, crd)
        return vel, crd, acc

    def main_print(self, *args):
        """compute the temperature"""
        _, temperature, total_potential_energy, _, _, _, _, _, _, _ = list(args)

        temperature = temperature.asnumpy()
        total_potential_energy = total_potential_energy.asnumpy()
        cv = self.norm(self.add(self.last_crd[11], -self.last_crd[14]))
        biasp = self.sum(
            self.dt * self.hills * self.omega * self.exp(-self.square(cv - self.cv_list) / 2 / self.square(self.sigma)))
        return cv, biasp

    def main_initial(self):
        """main initial"""
        if self.control.mdout:
            self.file = open(self.control.mdout, 'w')
            self.file.write("_steps_ _TEMP_ _TOT_POT_ENE_ _CVariable_ _Bias_Potential_\n")
        if self.control.mdcrd:
            self.datfile = open(self.control.mdcrd, 'wb')

    def main_destroy(self):
        """main destroy"""
        if self.file is not None:
            self.file.close()
            print("Save .out file successfully!")
        if self.datfile is not None:
            self.datfile.close()
            print("Save .dat file successfully!")

    def construct(self, step, print_step):
        '''construct'''
        self.last_crd = self.crd
        if step == 0:
            res = self.neighbor_list_update_init(self.atom_numbers_in_grid_bucket, self.bucket, self.crd,
                                                 self.virtual_box_length, self.grid_n, self.grid_length_inverse,
                                                 self.atom_in_grid_serial, self.old_crd, self.crd_to_uint_crd_cof,
                                                 self.uint_crd, self.pointer, self.nl_atom_numbers, self.nl_atom_serial,
                                                 self.uint_dr_to_dr_cof, self.excluded_list_start, self.excluded_list,
                                                 self.excluded_numbers, self.need_refresh_flag, self.refresh_count)
            self.nl_atom_numbers = F.depend(self.nl_atom_numbers, res)
            self.nl_atom_serial = F.depend(self.nl_atom_serial, res)
            self.uint_dr_to_dr_cof = F.depend(self.uint_dr_to_dr_cof, res)
            self.old_crd = F.depend(self.old_crd, res)
            self.atom_numbers_in_grid_bucket = F.depend(self.atom_numbers_in_grid_bucket, res)
            self.bucket = F.depend(self.bucket, res)
            self.atom_in_grid_serial = F.depend(self.atom_in_grid_serial, res)
            self.pointer = F.depend(self.pointer, res)

            positions = F.expand_dims(self.crd, 0)
            force = self.simulation_caculate_cybertron_force(positions, step)
            bond_energy_sum = self.zero_fp_tensor
            angle_energy_sum = self.zero_fp_tensor
            dihedral_energy_sum = self.zero_fp_tensor
            nb14_lj_energy_sum = self.zero_fp_tensor
            nb14_cf_energy_sum = self.zero_fp_tensor
            lj_energy_sum = self.zero_fp_tensor
            ee_ene = self.zero_fp_tensor
            total_energy = self.simulation_caculate_cybertron_energy(positions)

            temperature = self.simulation_temperature()
            self.rand_state = self.setup_random_state()
            self.velocity, self.crd, _ = self.simulation_mditeration_leapfrog_liujian(self.mass_inverse,
                                                                                      self.sqrt_mass, self.crd, force,
                                                                                      self.rand_state,
                                                                                      self.random_force)

            res = self.ds
            self.nl_atom_numbers = F.depend(self.nl_atom_numbers, res)
            self.nl_atom_serial = F.depend(self.nl_atom_serial, res)
        else:

            positions = F.expand_dims(self.crd, 0)
            force = self.simulation_caculate_cybertron_force(positions, step)
            if print_step == 0:
                bond_energy_sum = self.zero_fp_tensor
                angle_energy_sum = self.zero_fp_tensor
                dihedral_energy_sum = self.zero_fp_tensor
                nb14_lj_energy_sum = self.zero_fp_tensor
                nb14_cf_energy_sum = self.zero_fp_tensor
                lj_energy_sum = self.zero_fp_tensor
                ee_ene = self.zero_fp_tensor
                total_energy = self.simulation_caculate_cybertron_energy(positions)
            else:
                bond_energy_sum = self.zero_fp_tensor
                angle_energy_sum = self.zero_fp_tensor
                dihedral_energy_sum = self.zero_fp_tensor
                nb14_lj_energy_sum = self.zero_fp_tensor
                nb14_cf_energy_sum = self.zero_fp_tensor
                lj_energy_sum = self.zero_fp_tensor
                ee_ene = self.zero_fp_tensor
                total_energy = self.zero_fp_tensor
            temperature = self.simulation_temperature()
            self.velocity, self.crd, _ = self.simulation_mditeration_leapfrog_liujian(self.mass_inverse,
                                                                                      self.sqrt_mass, self.crd, force,
                                                                                      self.rand_state,
                                                                                      self.random_force)

            res = self.ds
            self.nl_atom_numbers = F.depend(self.nl_atom_numbers, res)
            self.nl_atom_serial = F.depend(self.nl_atom_serial, res)
        return temperature, total_energy, bond_energy_sum, angle_energy_sum, dihedral_energy_sum, nb14_lj_energy_sum, \
               nb14_cf_energy_sum, lj_energy_sum, ee_ene, res

class ArgsOpt():
    """ArgsOpt"""
    def __init__(self):
        self.amber_parm = '/home/workspace/mindspore_dataset/mindsponge_data/ai/cba.prmtop'
        self.box = ''
        self.c = '/home/workspace/mindspore_dataset/mindsponge_data/ai/cba_its_mw0_trans.rst7'
        self.checkpoint = ''
        self.device_id = 0
        self.i = '/home/workspace/mindspore_dataset/mindsponge_data/ai/md.in'
        self.o = ''
        self.r = ''
        self.u = False
        self.x = ''
        self.meta = 0
        self.with_box = 1
        self.np_iter = 0


@pytest.mark.level1
@pytest.mark.platform_x86_gpu_training
@pytest.mark.env_onecard
def test_case_mct():
    """test_case_mct for test"""
    args_opt = ArgsOpt()
    args_opt.initial_coordinates_file = args_opt.c
    context.set_context(mode=context.GRAPH_MODE, device_target="GPU", save_graphs=False)
    atom_types = Tensor([6, 1, 6, 1, 6, 1, 1, 6, 1, 6, 1, 6, 1, 1, 8])
    mod = MolCT(
        min_rbf_dis=0.1,
        max_rbf_dis=10,
        num_rbf=128,
        rbf_sigma=0.2,
        n_interactions=3,
        dim_feature=128,
        n_heads=8,
        max_cycles=1,
        use_time_embedding=True,
        fixed_cycles=True,
        self_dis=0.1,
        unit_length='A',
        use_feed_forward=False,
    )
    scales = 3.0
    readout = AtomwiseReadout(n_in=mod.dim_feature, n_interactions=mod.n_interactions, activation=mod.activation,
                              n_out=1, mol_scale=scales, unit_energy='kcal/mol')
    net = Cybertron(mod, atom_types=atom_types, full_connect=True, readout=readout, unit_dis='A',
                    unit_energy='kcal/mol')

    param_file = '/home/workspace/mindspore_dataset/mindsponge_data/ai/cba_kcal_mol_A_MolCT-best.ckpt'
    load_checkpoint(param_file, net=net)

    simulation = SimulationCybertron(args_opt, network=net)
    compiler_time = 0
    simulation.main_initial()
    for steps in range(simulation.md_info.step_limit):
        print_step = steps % simulation.ntwx
        if steps == simulation.md_info.step_limit - 1:
            print_step = 0
        temperature, total_potential_energy, sigma_of_bond_ene, sigma_of_angle_ene, _, \
        _, nb14_cf_energy_sum, lj_energy_sum, ee_ene, _ = simulation(Tensor(steps), Tensor(print_step))

        if steps == 0:
            compiler_time = time.time()
            cv, biasp = simulation.main_print(steps, temperature, total_potential_energy, sigma_of_bond_ene,
                                              sigma_of_angle_ene, Tensor(0), Tensor(0), nb14_cf_energy_sum,
                                              lj_energy_sum, ee_ene)
            assert np.allclose(round(float(temperature.asnumpy()), 3), 0.000, rtol=0.1)
            assert np.allclose(round(float(total_potential_energy.asnumpy()), 3), 464.834, rtol=0.1)
            assert np.allclose(round(float(cv.asnumpy()), 3), 1.449, rtol=0.1)
            assert np.allclose(round(float(biasp.asnumpy()), 3), 0.222, rtol=0.1)
    end = time.time()
    assert ((end - compiler_time) / 9) < 0.5
