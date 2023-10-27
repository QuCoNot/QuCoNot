import numpy as np


def load_matrix(mode, controls_no):
    container = np.load("./tests/mct_matrices/mct_" + mode + ".npz")
    return container["arr_" + str(controls_no - 1)]
