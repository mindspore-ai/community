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
#pylint: disable=W0613
"""
2D maxwell problem with Mur bc
"""
import numpy as np

import mindspore.numpy as ms_np
from mindspore import ms_function
from mindspore import ops
from mindspore import Tensor
import mindspore.common.dtype as ms_type

from mindelec.solver import Problem
from mindelec.common import MU, EPS, PI
from mindelec.operators import Grad


class Maxwell2DMur(Problem):
    r"""
    The 2D Maxwell's equations with 2nd-order Mur absorbed boundary condition.

    Args:
        network (Cell): The solving network.
        config (dict): Setting information.
        domain_column (str): The corresponding column name of data which governed by maxwell's equation.
        bc_column (str): The corresponding column name of data which governed by boundary condition.
        bc_normal (str): The column name of normal direction vector corresponding to specified boundary.
        ic_column (str): The corresponding column name of data which governed by initial condition.
    """
    def __init__(self, network, config, domain_column=None, bc_column=None, ic_column=None):
        super(Maxwell2DMur, self).__init__()
        self.domain_column = domain_column
        self.bc_column = bc_column
        self.ic_column = ic_column
        self.network = network

        # operations
        self.gradient = Grad(self.network)
        self.reshape = ops.Reshape()
        self.cast = ops.Cast()
        self.mul = ops.Mul()
        self.cast = ops.Cast()
        self.split = ops.Split(1, 3)
        self.concat = ops.Concat(1)
        self.sqrt = ops.Sqrt()

        # gauss-type pulse source
        self.pi = Tensor(PI, ms_type.float32)
        self.src_frq = config.get("src_frq", 1e+9)
        self.tau = Tensor((2.3 ** 0.5) / (PI * self.src_frq), ms_type.float32)
        self.amp = Tensor(1.0, ms_type.float32)
        self.t0 = Tensor(3.65 * self.tau, ms_type.float32)

        # src space
        self.src_x0 = Tensor(config["src_pos"][0], ms_type.float32)
        self.src_y0 = Tensor(config["src_pos"][1], ms_type.float32)
        self.src_sigma = Tensor(config["src_radius"] / 4.0, ms_type.float32)
        self.src_coord_min = config["coord_min"]
        self.src_coord_max = config["coord_max"]

        input_scales = config.get("input_scales", [1.0, 1.0, 2.5e+8])
        output_scales = config.get("output_scales", [37.67303, 37.67303, 0.1])
        self.s_x = Tensor(input_scales[0], ms_type.float32)
        self.s_y = Tensor(input_scales[1], ms_type.float32)
        self.s_t = Tensor(input_scales[2], ms_type.float32)
        self.s_ex = Tensor(output_scales[0], ms_type.float32)
        self.s_ey = Tensor(output_scales[1], ms_type.float32)
        self.s_hz = Tensor(output_scales[2], ms_type.float32)

        # set up eps, mu candidates
        eps_candidates = np.array(config["eps_list"], dtype=np.float32) * EPS
        mu_candidates = np.array(config["mu_list"], dtype=np.float32) * MU
        self.epsilon_x = Tensor(eps_candidates, ms_type.float32).view((-1, 1))
        self.epsilon_y = Tensor(eps_candidates, ms_type.float32).view((-1, 1))
        self.mu_z = Tensor(mu_candidates, ms_type.float32).view((-1, 1))
        self.light_speed = 1.0 / ops.Sqrt()(ops.Mul()(self.epsilon_x, self.mu_z))

    def smooth_src(self, x, y, t):
        source = self.amp * ops.exp(- ((t - self.t0) / self.tau)**2)
        gauss = 1 / (2 * self.pi * self.src_sigma**2) * \
                ops.exp(- ((x - self.src_x0)**2 + (y - self.src_y0)**2) / (2 * (self.src_sigma**2)))
        return self.mul(source, gauss)

    @ms_function
    def governing_equation(self, *output, **kwargs):
        """maxwell equation of TE mode wave"""
        out = output[0]
        data = kwargs[self.domain_column]
        x = self.reshape(data[:, 0], (-1, 1))
        y = self.reshape(data[:, 1], (-1, 1))
        t = self.reshape(data[:, 2], (-1, 1))

        dex_dxyt = self.gradient(data, None, 0, out)
        _, dex_dy, dex_dt = self.split(dex_dxyt)
        dey_dxyt = self.gradient(data, None, 1, out)
        dey_dx, _, dey_dt = self.split(dey_dxyt)
        dhz_dxyt = self.gradient(data, None, 2, out)
        dhz_dx, dhz_dy, dhz_dt = self.split(dhz_dxyt)

        dex_dy = self.cast(dex_dy, ms_type.float32)
        dex_dt = self.cast(dex_dt, ms_type.float32)
        dey_dx = self.cast(dey_dx, ms_type.float32)
        dey_dt = self.cast(dey_dt, ms_type.float32)
        dhz_dx = self.cast(dhz_dx, ms_type.float32)
        dhz_dy = self.cast(dhz_dy, ms_type.float32)
        dhz_dt = self.cast(dhz_dt, ms_type.float32)

        loss_a1 = (self.s_hz * dhz_dy) / (self.s_ex * self.s_t * self.epsilon_x)
        loss_a2 = dex_dt / self.s_t

        loss_b1 = -(self.s_hz * dhz_dx) / (self.s_ey * self.s_t * self.epsilon_y)
        loss_b2 = dey_dt / self.s_t

        loss_c1 = (self.s_ey * dey_dx - self.s_ex * dex_dy) / (self.s_hz * self.s_t * self.mu_z)
        loss_c2 = - dhz_dt / self.s_t

        source = self.smooth_src(x, y, t) / (self.s_hz * self.s_t * self.mu_z)

        pde_res1 = loss_a1 - loss_a2
        pde_res2 = loss_b1 - loss_b2
        pde_res3 = loss_c1 - loss_c2 - source
        pde_r = ops.Concat(1)((pde_res1, pde_res2, pde_res3))
        return pde_r

    @ms_function
    def boundary_condition(self, *output, **kwargs):
        """2nd-order mur boundary condition"""
        u = output[0]
        data = kwargs[self.bc_column]

        coord_min = self.src_coord_min
        coord_max = self.src_coord_max
        batch_size, _ = data.shape
        bc_attr = ms_np.zeros(shape=(batch_size, 4))
        bc_attr[:, 0] = ms_np.where(ms_np.isclose(data[:, 0], coord_min[0]), 1.0, 0.0)
        bc_attr[:, 1] = ms_np.where(ms_np.isclose(data[:, 0], coord_max[0]), 1.0, 0.0)
        bc_attr[:, 2] = ms_np.where(ms_np.isclose(data[:, 1], coord_min[1]), 1.0, 0.0)
        bc_attr[:, 3] = ms_np.where(ms_np.isclose(data[:, 1], coord_max[1]), 1.0, 0.0)

        dex_dxyt = self.gradient(data, None, 0, u)
        _, dex_dy, _ = self.split(dex_dxyt)
        dey_dxyt = self.gradient(data, None, 1, u)
        dey_dx, _, _ = self.split(dey_dxyt)
        dhz_dxyt = self.gradient(data, None, 2, u)
        dhz_dx, dhz_dy, dhz_dt = self.split(dhz_dxyt)

        dex_dy = self.cast(dex_dy, ms_type.float32)
        dey_dx = self.cast(dey_dx, ms_type.float32)
        dhz_dx = self.cast(dhz_dx, ms_type.float32)
        dhz_dy = self.cast(dhz_dy, ms_type.float32)
        dhz_dt = self.cast(dhz_dt, ms_type.float32)

        bc_r1 = dhz_dx / self.s_x - dhz_dt / (self.light_speed * self.s_x) + \
                self.s_ex * self.light_speed * self.epsilon_x / (2 * self.s_hz * self.s_x) * dex_dy # x=0
        bc_r2 = dhz_dx / self.s_x + dhz_dt / (self.light_speed * self.s_x) - \
                self.s_ex * self.light_speed * self.epsilon_x / (2 * self.s_hz * self.s_x) * dex_dy  # x=L
        bc_r3 = dhz_dy / self.s_y - dhz_dt / (self.light_speed * self.s_y) - \
                self.s_ey * self.light_speed * self.epsilon_y / (2 * self.s_hz * self.s_y) * dey_dx  # y=0
        bc_r4 = dhz_dy / self.s_y + dhz_dt / (self.light_speed * self.s_y) + \
                self.s_ey * self.light_speed * self.epsilon_y / (2 * self.s_hz * self.s_y) * dey_dx  # y=L

        bc_r_all = self.concat((bc_r1, bc_r2, bc_r3, bc_r4))
        bc_r = self.mul(bc_r_all, bc_attr)
        return bc_r

    @ms_function
    def initial_condition(self, *output, **kwargs):
        """initial condition: u = 0"""
        net_out = output[0]
        return net_out
