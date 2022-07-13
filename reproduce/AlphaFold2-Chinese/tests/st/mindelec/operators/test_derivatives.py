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
# ==============================================================================
#pylint: disable=W0235
"""
test derivatives
"""
import pytest
import numpy as np

from mindelec.operators import Grad, SecondOrderGrad, Jacobian, Hessian
from mindspore import Tensor, ops
from mindspore import dtype as mstype
from mindspore import context
from mindspore import nn
context.set_context(mode=context.GRAPH_MODE, device_target="Ascend")


def func(x):
    return x * x * x


class Net(nn.Cell):
    def __init__(self):
        super(Net, self).__init__()
        self.w = Tensor(np.array([[1, 5, 2], [8, 4, 6], [7, 6, 9], [5, 1, 5]], np.float32))
        self.matmul = ops.MatMul()

    def construct(self, a, b):
        x = ops.Concat(1)((a, b))
        return self.matmul(self.w, x)


class Net1(nn.Cell):
    def __init__(self):
        super(Net1, self).__init__()

    def construct(self, x, y):
        out = x * x * x * y * 5 + 3 * y * x * x + 15 * x * y
        return out.sum()


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_grad_error():
    """test grad error"""
    # check argnum error
    with pytest.raises(TypeError):
        Grad(func, "a")
    # check model error
    with pytest.raises(TypeError):
        Grad("a", 0)

    x = Tensor(np.array([[1.0, -2.0], [-3.0, 4.0]]).astype(np.float32))
    x1 = Tensor(np.array([[[1.0, -2.0], [-3.0, 4.0]]]).astype(np.float32))
    out = func(x)
    grad = Grad(func)
    # check net input type error
    with pytest.raises(TypeError):
        grad(0.0, 0, 0, out)
    # check input index type error
    with pytest.raises(TypeError):
        grad(x, [0], 0, out)
    # check output index type error
    with pytest.raises(TypeError):
        grad(x, 0, 1.2, out)
    # check net output type error
    with pytest.raises(TypeError):
        grad(x, 0, 0, (1,))
    # check net input value error
    with pytest.raises(ValueError):
        grad(x1, 0, 0, out)
    # check input index value error
    with pytest.raises(ValueError):
        grad(x, 7, 0, out)
    # check output index value error
    with pytest.raises(ValueError):
        grad(x, 0, 7, out)
    # check net output value error
    with pytest.raises(ValueError):
        grad(x, 0, 0, func(x1))


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_grad():
    """test grad"""
    x = Tensor(np.array([[1.0, -2.0], [-3.0, 4.0]]).astype(np.float32))
    out = func(x)
    grad = Grad(func)
    output = grad(x, 0, 0, out).asnumpy()
    res = np.array([[3.0], [27.0]], np.float32)
    assert (output == res).any()


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_grad_two_input():
    """test_grad_two_input"""
    a = Tensor(np.array([[1, 3], [5, 9], [8, 2]], np.float32))
    b = Tensor(np.array([[4, 6], [7, 2], [2, 1]], np.float32))
    net = Net()
    out = net(a, b)
    grad = Grad(net)
    output = grad(a, b, 0, 0, out).asnumpy()
    res = np.array([[21.0], [16.0], [22.0]], np.float32)
    assert (output == res).any()


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_second_order_grad_error():
    """test_second_order_grad_error"""
    # check input_idx1 type error
    with pytest.raises(TypeError):
        SecondOrderGrad(func, "a", 1, 0)
    # check input_idx2 type error
    with pytest.raises(TypeError):
        SecondOrderGrad(func, 1, 1.0, 0)
    # check output_idx type error
    with pytest.raises(TypeError):
        SecondOrderGrad(func, 1, 1, True)
    # check model error
    with pytest.raises(TypeError):
        Grad("a", 0, 0, 0)

    x = Tensor(np.array([[1.0, -2.0], [-3.0, 4.0]]).astype(np.float32))
    x1 = Tensor(np.array([[[1.0, -2.0], [-3.0, 4.0]]]).astype(np.float32))
    # check net input type error
    with pytest.raises(TypeError):
        second_order_grad = SecondOrderGrad(func, 0, 0, 0)
        second_order_grad(0.0)
    # check net input value error
    with pytest.raises(ValueError):
        second_order_grad = SecondOrderGrad(func, 0, 0, 0)
        second_order_grad(x1)
    # check input index 1 value error
    with pytest.raises(ValueError):
        second_order_grad = SecondOrderGrad(func, 7, 0, 0)
        second_order_grad(x)
    # check input index 2 value error
    with pytest.raises(ValueError):
        second_order_grad = SecondOrderGrad(func, 0, 7, 0)
        second_order_grad(x)
    # check output index value error
    with pytest.raises(ValueError):
        second_order_grad = SecondOrderGrad(func, 0, 0, 7)
        second_order_grad(x)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_second_order_grad():
    """test_second_order_grad"""
    x = Tensor(np.array([[1.0, -2.0], [-3.0, 4.0]]).astype(np.float32))
    second_order_grad = SecondOrderGrad(func, 0, 0, 0)
    output = second_order_grad(x).asnumpy()
    res = np.array([[6.0], [-18.0]], np.float32)
    assert output.any() == res.any()


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_class_jacobian_type_error():
    with pytest.raises(TypeError):
        Jacobian(Net1(), "a", 1)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_class_jacobian():
    """test Jacobian"""
    a = Tensor(np.array([[1, 3], [5, 9], [8, 2]], np.float32))
    b = Tensor(np.array([[4, 6], [7, 2], [2, 1]], np.float32))
    jac = Jacobian(Net(), 0, 0)
    output = jac(a, b).asnumpy()
    res = Tensor([[[[1, 0], [5, 0], [2, 0]], [[0, 1], [0, 5], [0, 2]],
                   [[0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0]]],
                  [[[8, 0], [4, 0], [6, 0]], [[0, 8], [0, 4], [0, 6]],
                   [[0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0]]],
                  [[[7, 0], [6, 0], [9, 0]], [[0, 7], [0, 6], [0, 9]],
                   [[0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0]]],
                  [[[5, 0], [1, 0], [5, 0]], [[0, 5], [0, 1], [0, 5]],
                   [[0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0]]]], mstype.float32).asnumpy()
    assert output.any() == res.any()


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_class_hessian_type_error():
    with pytest.raises(TypeError):
        Hessian(Net1(), "a", 1)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_onecard
def test_class_hessian():
    """test Hessian"""
    a = Tensor(np.array([[1, 3], [5, 9], [8, 2]], np.float32))
    b = Tensor(np.array([[4, 6], [7, 2], [2, 1]], np.float32))
    hes = Hessian(Net1(), 0, 1)
    output = hes(a, b).asnumpy()
    res = Tensor([[[[36, 0], [0, 0], [0, 0]], [[0, 168], [0, 0], [0, 0]]],
                  [[[0, 0], [420, 0], [0, 0]], [[0, 0], [0, 1284], [0, 0]]],
                  [[[0, 0], [0, 0], [1023, 0]], [[0, 0], [0, 0], [0, 87]]]], mstype.float32).asnumpy()
    assert output.any() == res.any()
