from typing import Tuple

import numpy as np

from .functions import ABS_TOLERANCE, REL_TOLERANCE, ket0, load_matrix
from .reverse_kronecker_product import reverse_kronecker_product


def _get_dims(tested_matrix: np.ndarray, ref_unitary: np.ndarray) -> Tuple[int, int, int]:
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


# Strict Clean Non-Wasting
def verify_circuit_strict_clean_non_wasting(
    tested_matrix: np.ndarray, ref_unitary: np.ndarray
) -> Tuple[bool, str]:
    """Verifies if tested_matrix is strict clean non-wasting based on reference matrix.

    Args:
        tested_matrix (np.ndarray): the global matrix to be tested
        ref_unitary (np.ndarray): true 0-1 unitary matrix

    Returns:
        Tuple[bool, str]: flag denoting if the tested matrix is of given class, and reason if
            it is not.
    """
    _, main_dim, aux_dim = _get_dims(tested_matrix, ref_unitary)

    i = np.eye(main_dim)
    ket_0 = ket0(aux_dim)
    ket_0_i = np.kron(ket_0, i)

    tested_matrix = ket_0_i @ tested_matrix @ ket_0_i.T

    m = tested_matrix @ ref_unitary.conj().T
    generated_unitary = m * np.conjugate(m[0, 0]) - np.eye(main_dim)

    if not np.allclose(generated_unitary, 0.0, atol=ABS_TOLERANCE, rtol=REL_TOLERANCE):
        return False, "Generated matrix should be all 0"

    return True, ""


# Relative Clean Non-Wasting
def verify_circuit_relative_clean_non_wasting(
    tested_matrix: np.ndarray, ref_unitary: np.ndarray
) -> Tuple[bool, str]:
    """Verifies if tested_matrix is relative clean non-wasting based on reference matrix.

    Args:
        tested_matrix (np.ndarray): the global matrix to be tested
        ref_unitary (np.ndarray): true 0-1 unitary matrix

    Returns:
        Tuple[bool, str]: flag denoting if the tested matrix is of given class, and reason if
            it is not.
    """
    _, main_dim, aux_dim = _get_dims(tested_matrix, ref_unitary)
    ket_0_i = np.kron(ket0(aux_dim), np.eye(main_dim))

    tested_matrix = ket_0_i @ tested_matrix @ ket_0_i.T

    m = tested_matrix @ ref_unitary.conj().T
    generated_unitary = np.abs(m) - np.eye(main_dim)

    if not np.allclose(generated_unitary, 0.0, atol=ABS_TOLERANCE, rtol=REL_TOLERANCE):
        return False, "Generated matrix should be all 0"
    return True, ""


# Strict Dirty Non-Wasting
def verify_circuit_strict_dirty_non_wasting(
    tested_matrix: np.ndarray, ref_unitary: np.ndarray
) -> tuple:
    """Verifies if tested_matrix is strict dirty non-wasting based on reference matrix.

    Args:
        tested_matrix (np.ndarray): the global matrix to be tested
        ref_unitary (np.ndarray): true 0-1 unitary matrix

    Returns:
        Tuple[bool, str]: flag denoting if the tested matrix is of given class, and reason if
            it is not.
    """
    global_dim, _, aux_dim = _get_dims(tested_matrix, ref_unitary)

    inverse_matrix = np.kron(np.eye(aux_dim), ref_unitary.conj().T)

    m = tested_matrix @ inverse_matrix
    generated_unitary = np.conjugate(m[0, 0]) * m - np.eye(global_dim)

    if not np.allclose(generated_unitary, 0.0, atol=ABS_TOLERANCE, rtol=REL_TOLERANCE):
        return False, "Generated matrix should be all 0"

    return True, ""


# Relative Dirty Non-Wasting
def verify_circuit_relative_dirty_non_wasting(
    tested_matrix, controls_no: int, auxiliaries_no: int
) -> Tuple[bool, str]:
    """Verifies if tested_matrix is relative dirty non-wasting based on reference matrix.

    Args:
        tested_matrix (np.ndarray): the global matrix to be tested
        ref_unitary (np.ndarray): true 0-1 unitary matrix

    Returns:
        Tuple[bool, str]: flag denoting if the tested matrix is of given class, and reason if
            it is not.
    """
    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    inverse_matrix = load_matrix("reverse_noauxiliary", controls_no)

    v_shape = 2 ** (controls_no + 1)
    w_shape = 2 ** (auxiliaries_no)

    v, w = reverse_kronecker_product(tested_matrix, (v_shape, v_shape))

    # check shape of w
    if w.shape != (w_shape, w_shape):
        return False, "Unitary W has different shape."

    # check if w is unitary
    check_w = w @ w.conj().T

    if not np.allclose(
        check_w,
        np.eye(2**auxiliaries_no),
        atol=ABS_TOLERANCE,
        rtol=REL_TOLERANCE,
    ):
        return False, "Matrix W should be unitary"

    check_v = np.matmul(np.abs(v), inverse_matrix)
    generated_unitary = check_v - np.eye(2 ** (controls_no + 1))

    if not np.allclose(
        generated_unitary,
        0.0,
        atol=ABS_TOLERANCE,
        rtol=REL_TOLERANCE,
    ):
        return False, "Generated matrix V should be all 0"

    return True, ""


# Strict Clean Wasting-Entangled
# Relative Clean Wasting-Entangled
def verify_circuit_strict_clean_wasting_entangled(
    tested_matrix: np.ndarray, ref_unitary: np.ndarray
) -> Tuple[bool, str]:
    """Verifies if tested_matrix is strict clean wasting entangled based on reference matrix.

    Args:
        tested_matrix (np.ndarray): the global matrix to be tested
        ref_unitary (np.ndarray): true 0-1 unitary matrix

    Returns:
        Tuple[bool, str]: flag denoting if the tested matrix is of given class, and reason if
            it is not.
    """
    _, main_dim, aux_dim = _get_dims(tested_matrix, ref_unitary)

    i = np.eye(aux_dim)
    ket_0 = ket0(aux_dim)

    for idx in range(main_dim):
        ket_b = np.zeros(main_dim)
        ket_b[idx] = 1
        b_0 = np.kron(ket_0, ket_b)
        res_1 = tested_matrix @ b_0
        res_2 = np.kron(i, ref_unitary.conj().T @ ket_b)
        res_3 = res_2 @ res_1

        if not np.isclose(np.linalg.norm(res_3), 1.0):
            return False, "The length should be 1"

    return True, ""


# Strict Dirty Wasting-Entangled
def verify_circuit_strict_dirty_wasting_entangled(
    tested_matrix: np.ndarray, ref_unitary: np.ndarray
) -> Tuple[bool, str]:
    """Verifies if tested_matrix is strict dirty wasting entangled based on reference matrix.

    Args:
        tested_matrix (np.ndarray): the global matrix to be tested
        ref_unitary (np.ndarray): true 0-1 unitary matrix

    Returns:
        Tuple[bool, str]: flag denoting if the tested matrix is of given class, and reason if
            it is not.
    """

    _, main_dim, aux_dim = _get_dims(tested_matrix, ref_unitary)

    i = np.eye(aux_dim)

    ket_b = np.zeros(main_dim)
    for idx_b in range(main_dim):
        ket_b[idx_b] = 1.0
        ket_pib = np.kron(i, (ref_unitary @ ket_b).conj().T)
        ket_c = np.zeros(aux_dim)
        for idx_c in range(aux_dim):
            ket_c[idx_c] = 1.0
            ket_bc = np.kron(ket_c, ket_b)
            res = tested_matrix @ ket_bc
            res = ket_pib @ res
            if not np.isclose(np.linalg.norm(res), 1.0):
                return False, "The length should be 1"
            ket_c[idx_c] = 0.0
        ket_b[idx_b] = 0.0
    return True, ""


# Strict Clean Wasting-Separable
def verify_circuit_strict_clean_wasting_separable(
    tested_matrix: np.ndarray, ref_unitary: np.ndarray
) -> Tuple[bool, str]:
    """Verifies if tested_matrix is strict clean wasting separable based on reference matrix.

    Args:
        tested_matrix (np.ndarray): the global matrix to be tested
        ref_unitary (np.ndarray): true 0-1 unitary matrix

    Returns:
        Tuple[bool, str]: flag denoting if the tested matrix is of given class, and reason if
            it is not.
    """

    _, main_dim, aux_dim = _get_dims(tested_matrix, ref_unitary)

    i = np.eye(aux_dim)
    ket_0 = ket0(aux_dim)

    phi_0 = np.zeros(aux_dim)
    ket_b = np.zeros(main_dim)
    for idx in range(main_dim):
        ket_b[idx] = 1
        b_0 = np.kron(ket_0, ket_b)
        res = np.kron(i, ref_unitary @ ket_b) @ tested_matrix @ b_0
        # this is to get the |\phi_0>
        if idx == 0:
            phi_0 = res

        # check if res_3 a quantum state here
        if not np.isclose(np.vdot(phi_0, res), 1):
            return False, "The state should be a quantum state"
        ket_b[idx] = 0

    return True, ""


# Relative Clean Wasting-Separable
def verify_circuit_relative_clean_wasting_separable(
    tested_matrix: np.ndarray, ref_unitary: np.ndarray
) -> Tuple[bool, str]:
    """Verifies if tested_matrix is relative clean wasting separable based on reference matrix.

    Args:
        tested_matrix (np.ndarray): the global matrix to be tested
        ref_unitary (np.ndarray): true 0-1 unitary matrix

    Returns:
        Tuple[bool, str]: flag denoting if the tested matrix is of given class, and reason if
            it is not.
    """

    global_dim, main_dim, aux_dim = _get_dims(tested_matrix, ref_unitary)

    i_c = np.eye(aux_dim)
    i_b = np.eye(main_dim)
    ket_0b = ket0(main_dim)
    ket_0c = ket0(aux_dim)
    ket_0bc = ket0(global_dim)

    psi = np.kron(i_c, ref_unitary @ ket_0b) @ tested_matrix @ ket_0bc

    res_3 = tested_matrix @ np.kron(ket_0c, i_b).conj().T
    res_4 = np.kron(psi, i_b)

    generated_unitary = np.abs(res_4 @ res_3)

    if not np.allclose(generated_unitary, ref_unitary, atol=ABS_TOLERANCE, rtol=REL_TOLERANCE):
        return False, "Resulting matrix should be identity"

    return True, ""


# Strict Dirty Wasting-Separable
def verify_circuit_strict_dirty_wasting_separable(
    tested_matrix, controls_no: int, auxiliaries_no: int
):
    """Verifies if tested_matrix is strict dirty wasting separable based on reference matrix.

    Args:
        tested_matrix (np.ndarray): the global matrix to be tested
        ref_unitary (np.ndarray): true 0-1 unitary matrix

    Returns:
        Tuple[bool, str]: flag denoting if the tested matrix is of given class, and reason if
            it is not.
    """

    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    inverse_matrix = load_matrix("reverse_noauxiliary", controls_no)

    v_shape = 2 ** (controls_no + 1)
    w_shape = 2 ** (auxiliaries_no)

    v, w = reverse_kronecker_product(tested_matrix, (v_shape, v_shape))

    no_of_qubits = controls_no + 1

    # check shape of w
    if w.shape != (w_shape, w_shape):
        return False, "Unitary W has different shape."

    # check if w is unitary
    check_w = np.matmul(w, w.conj().T)

    if not np.allclose(
        check_w, np.eye(2**auxiliaries_no), atol=ABS_TOLERANCE, rtol=REL_TOLERANCE
    ):
        return False, "Something wrong with the implementation"

    # Expected unitary after calculation is identity.
    expected_unitary = np.eye(2**no_of_qubits)

    # X_1 * X_2^dagger * np.conj((X_1 * X_2^dagger)[0,0]) = I
    m = v @ inverse_matrix
    generated_unitary = m * np.conjugate(m[0, 0])

    if generated_unitary.shape != expected_unitary.shape:
        return False, "Unitary V has different shape."

    if not np.allclose(generated_unitary, expected_unitary, atol=ABS_TOLERANCE, rtol=REL_TOLERANCE):
        return False, "Resulting matrix should be an Identity"

    return True, ""


# Relative Dirty Wasting-Separable
def verify_circuit_relative_dirty_wasting_separable(
    tested_matrix, controls_no: int, auxiliaries_no: int
):
    """Verifies if tested_matrix is relative dirty wasting separable based on reference matrix.

    Args:
        tested_matrix (np.ndarray): the global matrix to be tested
        ref_unitary (np.ndarray): true 0-1 unitary matrix

    Returns:
        Tuple[bool, str]: flag denoting if the tested matrix is of given class, and reason if
            it is not.
    """

    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    inverse_matrix = load_matrix("reverse_noauxiliary", controls_no)

    v_shape = 2 ** (controls_no + 1)
    w_shape = 2 ** (auxiliaries_no)

    v, w = reverse_kronecker_product(tested_matrix, (v_shape, v_shape))

    no_of_qubits = controls_no + 1

    # check shape of w
    if w.shape != (w_shape, w_shape):
        return False, "Unitary W has different shape."

    # check if w is unitary
    check_w = w @ w.conj().T

    if not np.allclose(
        check_w, np.eye(2**auxiliaries_no), atol=ABS_TOLERANCE, rtol=REL_TOLERANCE
    ):
        return False, "Resulting matrix should be identity"

    expected_unitary = np.eye(2**no_of_qubits)

    m = v @ inverse_matrix
    generated_unitary = np.abs(m)

    if generated_unitary.shape != expected_unitary.shape:
        return False, "Unitary V has different shape."

    if not np.allclose(generated_unitary, expected_unitary, atol=ABS_TOLERANCE, rtol=REL_TOLERANCE):
        return False, "Resulting matrix should be identity"

    return True, ""
