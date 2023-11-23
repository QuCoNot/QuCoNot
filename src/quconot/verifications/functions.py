# This is where we put fixtures
from typing import Tuple

import numpy as np

# constants
ABS_TOLERANCE = 1e-8
REL_TOLERANCE = 1e-8


def ket0(dim: int):
    ket_0 = np.zeros(dim)
    ket_0[0] = 1.0
    return ket_0


def _get_dims(
    tested_matrix: np.ndarray, ref_unitary: np.ndarray
) -> Tuple[int, int, int]:
    """Returns the dimensions of the global, main and auxilliary system.

    Auxiliary system dimension is the dimensionality

    Args:
        tested_matrix (np.ndarray): the global system unitary
        ref_unitary (np.ndarray): the main system unitary

    Returns:
        Tuple[int, int, int]: global, main, and aux dimensions.
    """
    main_dim = ref_unitary.shape[0]
    global_dim = tested_matrix.shape[0]
    if global_dim % main_dim != 0:
        raise ValueError(
            f"One cannot find auxilliary system for dimensions {main_dim} and {global_dim} cannot"
        )
    aux_dim = global_dim // main_dim
    return global_dim, main_dim, aux_dim
