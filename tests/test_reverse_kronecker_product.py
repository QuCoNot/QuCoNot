import numpy as np
import pytest

from quconot.verifications.functions import ABS_TOLERANCE, REL_TOLERANCE
from quconot.verifications.reverse_kronecker_product import reverse_kronecker_product


@pytest.mark.parametrize(
    "par_B",
    [
        np.array([[1, 0], [0, -1]]),
        np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
        np.array([[0, 1], [1, 0]]),
    ],
)
@pytest.mark.parametrize(
    "par_C", [np.array([[1, 0], [0, -1]]), np.array([[0, 1], [1, 0]])]
)
def test_reverse_kronecker_product(par_B, par_C):
    A = np.kron(par_B, par_C)

    res_B, res_C = reverse_kronecker_product(A, par_B.shape)

    res_A = np.kron(res_B, res_C)

    zero_matrix = A - res_A

    assert np.allclose(
        np.eye(len(res_B)), res_B.dot(res_B.T.conj())
    ), "B Matrix should be a Unitary"

    assert np.allclose(
        np.eye(len(res_C)), res_C.dot(res_C.T.conj())
    ), "C Matrix should be a Unitary"

    assert np.allclose(
        zero_matrix, 0.0, ABS_TOLERANCE, REL_TOLERANCE
    ), "Result should close to 0"
