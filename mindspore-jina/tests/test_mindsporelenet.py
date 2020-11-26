import numpy as np

from .. import MindsporeLeNet


def test_mindsporelenet():
    """here is my test code

    https://docs.pytest.org/en/stable/getting-started.html#create-your-first-test
    """
    mln = MindsporeLeNet('lenet/ckpt/checkpoint_lenet-1_1875.ckpt')
    tmp = np.random.random([4, 28 * 28])

    # The sixth layer is a fully connected layer (F6) with 84 units.
    # it is the last layer before the output
    assert mln.encode(tmp).shape == (4, 84)
