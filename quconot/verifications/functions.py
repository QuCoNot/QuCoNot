# This is where we put fixtures
import numpy as np

# constants
ABS_TOLERANCE = 1e-8
REL_TOLERANCE = 1e-8


def ket0(dim: int):
    ket_0 = np.zeros(dim)
    ket_0[0] = 1.0
    return ket_0


def load_matrix(mode, controls_no):
    container = np.load("./tests/mct_matrices/mct_" + mode + ".npz")
    return container["arr_" + str(controls_no - 1)]
