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
import mindspore.numpy as ms_np
from mindspore import ms_function
from mindspore import ops
from mindspore import Tensor
import mindspore.common.dtype as mstype

from mindelec.solver import Problem
from mindelec.common import MU, EPS, LIGHT_SPEED, PI
from mindelec.operators import Grad


class Maxwell2DMur(Problem):
    r"""
    The 2D Maxwell's equations with 2nd-order Mur absorbed boundary condition.

    Args:
        model (Cell): The solving network.
        config (dict): Setting information.
        domain_name (str): The corresponding column name of data which governed by maxwell's equation.
        bc_name (str): The corresponding column name of data which governed by boundary condition.
        bc_normal (str): The column name of normal direction vector corresponding to specified boundary.
        ic_name (str): The corresponding column name of data which governed by initial condition.
    """
    def __init__(self, model, config, domain_name=None, bc_name=None, bc_normal=None, ic_name=None):
        super(Maxwell2DMur, self).__init__()
        self.domain_name = domain_name
        self.bc_name = bc_name
        self.bc_normal = bc_normal
        self.ic_name = ic_name
        self.model = model
        self.grad = Grad(self.model)
        self.reshape = ops.Reshape()
        self.cast = ops.Cast()
        self.mul = ops.Mul()
        self.cast = ops.Cast()
        self.split = ops.Split(1, 3)
        self.concat = ops.Concat(1)

        # constants
        self.pi = Tensor(PI, mstype.float32)
        self.eps_x = Tensor(EPS, mstype.float32)
        self.eps_y = Tensor(EPS, mstype.float32)
        self.mu_z = Tensor(MU, mstype.float32)
        self.light_speed = Tensor(LIGHT_SPEED, mstype.float32)

        # gauss-type pulse source
        self.src_frq = config.get("src_frq", 1e+9)
        self.tau = Tensor((2.3 ** 0.5) / (PI * self.src_frq), mstype.float32)
        self.amp = Tensor(1.0, mstype.float32)
        self.t0 = Tensor(3.65 * self.tau, mstype.float32)

        # src space
        self.x0 = Tensor(config["src_pos"][0], mstype.float32)
        self.y0 = Tensor(config["src_pos"][1], mstype.float32)
        self.sigma = Tensor(config["src_radius"] / 4.0, mstype.float32)
        self.coord_min = config["coord_min"]
        self.coord_max = config["coord_max"]

        input_scale = config.get("input_scale", [1.0, 1.0, 2.5e+8])
        output_scale = config.get("output_scale", [37.67303, 37.67303, 0.1])
        self.s_x = Tensor(input_scale[0], mstype.float32)
        self.s_y = Tensor(input_scale[1], mstype.float32)
        self.s_t = Tensor(input_scale[2], mstype.float32)
        self.s_ex = Tensor(output_scale[0], mstype.float32)
        self.s_ey = Tensor(output_scale[1], mstype.float32)
        self.s_hz = Tensor(output_scale[2], mstype.float32)

    def smooth_src(self, x, y, t):
        source = self.amp * ops.exp(- ((t - self.t0) / self.tau)**2)
        gauss = 1 / (2 * self.pi * self.sigma**2) * \
                ops.exp(- ((x - self.x0)**2 + (y - self.y0)**2) / (2 * (self.sigma**2)))
        return self.mul(source, gauss)

    @ms_function
    def governing_equation(self, *output, **kwargs):
        """maxwell equation of TE mode wave"""
        u = output[0]
        data = kwargs[self.domain_name]
        x = self.reshape(data[:, 0], (-1, 1))
        y = self.reshape(data[:, 1], (-1, 1))
        t = self.reshape(data[:, 2], (-1, 1))

        dex_dxyt = self.grad(data, None, 0, u)
        _, dex_dy, dex_dt = self.split(dex_dxyt)
        dey_dxyt = self.grad(data, None, 1, u)
        dey_dx, _, dey_dt = self.split(dey_dxyt)
        dhz_dxyt = self.grad(data, None, 2, u)
        dhz_dx, dhz_dy, dhz_dt = self.split(dhz_dxyt)

        dex_dy = self.cast(dex_dy, mstype.float32)
        dex_dt = self.cast(dex_dt, mstype.float32)
        dey_dx = self.cast(dey_dx, mstype.float32)
        dey_dt = self.cast(dey_dt, mstype.float32)
        dhz_dx = self.cast(dhz_dx, mstype.float32)
        dhz_dy = self.cast(dhz_dy, mstype.float32)
        dhz_dt = self.cast(dhz_dt, mstype.float32)

        loss_a1 = (self.s_hz * dhz_dy) / (self.s_ex * self.s_t * self.eps_x)
        loss_a2 = dex_dt / self.s_t

        loss_b1 = -(self.s_hz * dhz_dx) / (self.s_ey * self.s_t * self.eps_y)
        loss_b2 = dey_dt / self.s_t

        loss_c1 = (self.s_ey * dey_dx - self.s_ex * dex_dy) / (self.s_hz * self.s_t * self.mu_z)
        loss_c2 = - dhz_dt / self.s_t

        src = self.smooth_src(x, y, t) / (self.s_hz * self.s_t * self.mu_z)

        pde_r1 = loss_a1 - loss_a2
        pde_r2 = loss_b1 - loss_b2
        pde_r3 = loss_c1 - loss_c2 - src
        pde_r = ops.Concat(1)((pde_r1, pde_r2, pde_r3))
        return pde_r

    @ms_function
    def boundary_condition(self, *output, **kwargs):
        """2nd-order mur boundary condition"""
        u = output[0]
        data = kwargs[self.bc_name]

        coord_min = self.coord_min
        coord_max = self.coord_max
        batch_size, _ = data.shape
        attr = ms_np.zeros(shape=(batch_size, 4))
        attr[:, 0] = ms_np.where(ms_np.isclose(data[:, 0], coord_min[0]), 1.0, 0.0)
        attr[:, 1] = ms_np.where(ms_np.isclose(data[:, 0], coord_max[0]), 1.0, 0.0)
        attr[:, 2] = ms_np.where(ms_np.isclose(data[:, 1], coord_min[1]), 1.0, 0.0)
        attr[:, 3] = ms_np.where(ms_np.isclose(data[:, 1], coord_max[1]), 1.0, 0.0)

        dex_dxyt = self.grad(data, None, 0, u)
        _, dex_dy, _ = self.split(dex_dxyt)
        dey_dxyt = self.grad(data, None, 1, u)
        dey_dx, _, _ = self.split(dey_dxyt)
        dhz_dxyt = self.grad(data, None, 2, u)
        dhz_dx, dhz_dy, dhz_dt = self.split(dhz_dxyt)

        dex_dy = self.cast(dex_dy, mstype.float32)
        dey_dx = self.cast(dey_dx, mstype.float32)
        dhz_dx = self.cast(dhz_dx, mstype.float32)
        dhz_dy = self.cast(dhz_dy, mstype.float32)
        dhz_dt = self.cast(dhz_dt, mstype.float32)

        bc_r1 = dhz_dx / self.s_x - dhz_dt / (self.light_speed * self.s_x) + \
                self.s_ex * self.light_speed * self.eps_x / (2 * self.s_hz * self.s_x) * dex_dy # x=0
        bc_r2 = dhz_dx / self.s_x + dhz_dt / (self.light_speed * self.s_x) - \
                self.s_ex * self.light_speed * self.eps_x / (2 * self.s_hz * self.s_x) * dex_dy  # x=L
        bc_r3 = dhz_dy / self.s_y - dhz_dt / (self.light_speed * self.s_y) - \
                self.s_ey * self.light_speed * self.eps_y / (2 * self.s_hz * self.s_y) * dey_dx  # y=0
        bc_r4 = dhz_dy / self.s_y + dhz_dt / (self.light_speed * self.s_y) + \
                self.s_ey * self.light_speed * self.eps_y / (2 * self.s_hz * self.s_y) * dey_dx  # y=L

        bc_r_all = self.concat((bc_r1, bc_r2, bc_r3, bc_r4))
        bc_r = self.mul(bc_r_all, attr)
        return bc_r

    @ms_function
    def initial_condition(self, *output, **kwargs):
        """initial condition: u = 0"""
        u = output[0]
        return u
