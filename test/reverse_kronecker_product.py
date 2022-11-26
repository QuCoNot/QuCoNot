import numpy as np


def reverse_kronecker_product(A, B_shape):
    """Reverse Kronecker Product (RKP) to a matrix.
    Given a matrix A and a shape, solves the problem
    min || A - kron(B, C) ||_{Fro}^2
    where the minimization is over B with (the specified shape) and C.
    Args:
    A: m x n matrix
    B_shape: pair of ints (a, b) where a divides m and b divides n
    Returns:
    Approximating factors (B, C)
    """
    blocks = map(lambda blockcol: np.split(blockcol, B_shape[0], 0), np.split(A, B_shape[1], 1))

    # rearrange matrix A to A^(m1n1 x m2n2) matrix
    R_A = np.vstack([block.ravel() for blockcol in blocks for block in blockcol])

    # get the SVD from R_A
    W, s, V = np.linalg.svd(R_A)

    # approximate the C matrix shape
    C_shape = A.shape[0] // B_shape[0], A.shape[1] // B_shape[1]

    # get the largest singular value
    idx = np.argmax(s)

    # throw an error if we don't find any largest singular value
    if s[idx] <= 0:
        raise Exception("No largest singular value exist, RKP cannot be proceed")

    # get matrix B back from the computation
    Vec_B = np.sqrt(s[idx]) * W[:, idx]
    B = Vec_B.reshape(B_shape).T

    # get matrix C back from the computation
    Vec_C = np.sqrt(s[idx]) * V[idx, :]
    C = Vec_C.reshape(C_shape)

    B /= np.linalg.norm(B[:, 0], ord=2)
    C /= np.linalg.norm(C[:, 0], ord=2)

    return B, C
