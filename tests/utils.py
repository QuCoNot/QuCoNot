from functools import lru_cache

import numpy as np


@lru_cache()
def load_matrix(mode: str, controls_no: int):
    container = np.load("./tests/ref_matrices/mct_" + mode + ".npz")
    return container["arr_" + str(controls_no - 1)]
