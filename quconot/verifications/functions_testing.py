import numpy as np

from .functions import (
    ABS_TOLERANCE,
    identity_matrix,
    ket0,
    ket_0_matrix,
    load_matrix,
    REL_TOLERANCE,
    zero_matrix,
)
from .reverse_kronecker_product import reverse_kronecker_product
from typing import Tuple


def _get_dims(unitary_matrix: np.ndarray, ref_unitary: np.ndarray) -> Tuple[int, int, int]:
    main_dim = ref_unitary.shape[0]
    global_dim = unitary_matrix.shape[0]
    aux_dim = global_dim // main_dim
    return global_dim, main_dim, aux_dim


# Strict Clean Non-Wasting
def verify_circuit_strict_clean_non_wasting(
    unitary_matrix: np.ndarray, ref_unitary: np.ndarray
) -> Tuple[bool, str]:
    _, main_dim, aux_dim = _get_dims(unitary_matrix, ref_unitary)

    i = np.eye(main_dim)
    ket_0 = ket0(aux_dim)
    ket_0_i = np.kron(ket_0, i)

    unitary_matrix = ket_0_i @ unitary_matrix @ ket_0_i.T

    m = unitary_matrix @ ref_unitary.conj().T
    generated_unitary = m * np.conjugate(m[0, 0]) - np.eye(main_dim)

    if not np.allclose(generated_unitary, 0.0, atol=ABS_TOLERANCE, rtol=REL_TOLERANCE):
        return False, "Generated matrix should be all 0"

    return True, ""


# Relative Clean Non-Wasting
def verify_circuit_relative_clean_non_wasting(
    unitary_matrix: np.ndarray, ref_unitary: np.ndarray
) -> Tuple[bool, str]:
    _, main_dim, aux_dim = _get_dims(unitary_matrix, ref_unitary)
    ket_0_i = np.kron(ket0(aux_dim), np.eye(main_dim))

    unitary_matrix = ket_0_i @ unitary_matrix @ ket_0_i.T

    m = unitary_matrix @ ref_unitary.conj().T
    generated_unitary = np.absolute(m) - np.eye(main_dim)

    if not np.allclose(generated_unitary, 0.0, atol=ABS_TOLERANCE, rtol=REL_TOLERANCE):
        return False, "Generated matrix should be all 0"
    return True, ""


# Strict Dirty Non-Wasting
def verify_circuit_strict_dirty_non_wasting(
    unitary_matrix: np.ndarray, ref_unitary: np.ndarray
) -> tuple:
    global_dim, main_dim, aux_dim = _get_dims(unitary_matrix, ref_unitary)

    inverse_matrix = np.kron(np.eye(aux_dim), ref_unitary.conj().T)

    m = unitary_matrix @ inverse_matrix
    generated_unitary = np.conjugate(m[0, 0]) * m - np.eye(global_dim)

    if not np.allclose(generated_unitary, 0.0, atol=ABS_TOLERANCE, rtol=REL_TOLERANCE):
        return False, "Generated matrix should be all 0"

    return True, ""


# Relative Dirty Non-Wasting
def verify_circuit_relative_dirty_non_wasting(
    unitary_matrix, controls_no: int, auxiliaries_no: int
) -> Tuple[bool, str]:
    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    inverse_matrix = load_matrix("reverse_noauxiliary", controls_no)

    v_shape = 2 ** (controls_no + 1)
    w_shape = 2 ** (auxiliaries_no)

    v, w = reverse_kronecker_product(unitary_matrix, (v_shape, v_shape))

    # check shape of w
    if w.shape != (w_shape, w_shape):
        return False, "Unitary W has different shape."

    # check if w is unitary
    check_w = np.matmul(w, np.linalg.inv(w))

    if not np.allclose(
        check_w,
        identity_matrix(auxiliaries_no),
        atol=ABS_TOLERANCE,
        rtol=REL_TOLERANCE,
    ):
        return False, "Matrix W should be unitary"

    check_v = np.matmul(np.absolute(v), inverse_matrix)
    generated_unitary = check_v - identity_matrix(controls_no + 1)
    expected_unitary = zero_matrix(controls_no + 1)

    if generated_unitary.shape != expected_unitary.shape:
        return False, "Unitary V has different shape."

    if not np.allclose(
        generated_unitary,
        expected_unitary,
        atol=ABS_TOLERANCE,
        rtol=REL_TOLERANCE,
    ):
        return False, "Generated matrix V should be all 0"

    return True, ""


# Strict Clean Wasting-Entangled
# Relative Clean Wasting-Entangled
def verify_circuit_strict_clean_wasting_entangled(
    unitary_matrix: np.ndarray, ref_unitary: np.ndarray
) -> Tuple[bool, str]:
    _, main_dim, aux_dim = _get_dims(unitary_matrix, ref_unitary)

    i = np.eye(aux_dim)
    ket_0 = ket0(aux_dim)

    for idx in range(main_dim):
        ket_b = np.zeros(main_dim)
        ket_b[idx] = 1
        b_0 = np.kron(ket_0, ket_b)
        res_1 = unitary_matrix @ b_0
        res_2 = np.kron(i, ref_unitary.conj().T @ ket_b)
        res_3 = res_2 @ res_1

        if not np.isclose(np.linalg.norm(res_3), 1.0):
            return False, "The length should be 1"

    return True, ""


# Strict Dirty Wasting-Entangled
def verify_circuit_strict_dirty_wasting_entangled(
    unitary_matrix: np.ndarray, ref_unitary: np.ndarray
) -> Tuple[bool, str]:
    _, main_dim, aux_dim = _get_dims(unitary_matrix, ref_unitary)

    i = np.eye(aux_dim)

    ket_b = np.zeros(main_dim)
    for idx_b in range(main_dim):
        ket_b[idx_b] = 1.0
        ket_pib = np.kron(i, (ref_unitary @ ket_b).conj().T)
        ket_c = np.zeros(aux_dim)
        for idx_c in range(aux_dim):
            ket_c[idx_c] = 1.0
            ket_bc = np.kron(ket_c, ket_b)
            res = unitary_matrix @ ket_bc
            res = ket_pib @ res
            if not np.isclose(np.linalg.norm(res), 1.0):
                return False, "The length should be 1"
            ket_c[idx_c] = 0.0
        ket_b[idx_b] = 0.0
    return True, ""


# Strict Clean Wasting-Separable
def verify_circuit_strict_clean_wasting_separable(
    unitary_matrix, controls_no: int, auxiliaries_no: int
) -> Tuple[bool, str]:
    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    inverse_matrix = load_matrix("noauxiliary", controls_no)

    i = identity_matrix(auxiliaries_no)
    ket_0 = ket_0_matrix(auxiliaries_no)

    phi_0 = np.zeros(2)

    for idx in range(2 ** (controls_no + 1)):
        ket_b = np.zeros(2 ** (controls_no + 1))
        ket_b[idx] = 1
        b_0 = np.kron(ket_0, ket_b)
        res_1 = np.matmul(unitary_matrix, b_0)
        res_2 = np.kron(i, np.matmul(inverse_matrix, ket_b))
        res_3 = np.matmul(res_2, res_1)
        # this is to get the |\phi_0>
        if idx == 0:
            phi_0 = res_3

        # check if res_3 a quantum state here
        if not np.isclose(np.matmul(phi_0.T, res_3), 1):
            return False, "The state should be a quantum state"

    return True, ""


# Relative Clean Wasting-Separable
def verify_circuit_relative_clean_wasting_separable(
    unitary_matrix, controls_no: int, auxiliaries_no: int
):
    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    inverse_matrix = load_matrix("noauxiliary", controls_no)

    i_c = identity_matrix(auxiliaries_no)
    i_b = identity_matrix(controls_no + 1)
    ket_0b = ket_0_matrix(controls_no + 1)
    ket_0c = ket_0_matrix(auxiliaries_no)
    ket_0bc = ket_0_matrix(controls_no + auxiliaries_no + 1)

    res_1 = np.matmul(unitary_matrix, ket_0bc)
    res_2 = np.kron(i_c, np.matmul(inverse_matrix, ket_0b))

    psi = np.matmul(res_2, res_1)

    res_3 = np.matmul(unitary_matrix, np.kron(ket_0c, i_b).T)
    res_4 = np.kron(psi, i_b)

    m = np.matmul(res_4, res_3)
    generated_unitary = np.absolute(m)

    expected_unitary = inverse_matrix

    if generated_unitary.shape != expected_unitary.shape:
        return False, "generated_unitary has different shape."

    if not np.allclose(generated_unitary, expected_unitary, atol=ABS_TOLERANCE, rtol=REL_TOLERANCE):
        return False, "Resulting matrix should be identity"

    return True, ""


# Strict Dirty Wasting-Separable
def verify_circuit_strict_dirty_wasting_separable(
    unitary_matrix, controls_no: int, auxiliaries_no: int
):
    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    inverse_matrix = load_matrix("reverse_noauxiliary", controls_no)

    v_shape = 2 ** (controls_no + 1)
    w_shape = 2 ** (auxiliaries_no)

    v, w = reverse_kronecker_product(unitary_matrix, (v_shape, v_shape))

    no_of_qubits = controls_no + 1

    # check shape of w
    if w.shape != (w_shape, w_shape):
        return False, "Unitary W has different shape."

    # check if w is unitary
    check_w = np.matmul(w, np.linalg.inv(w))

    if not np.allclose(
        check_w, identity_matrix(auxiliaries_no), atol=ABS_TOLERANCE, rtol=REL_TOLERANCE
    ):
        return False, "Something wrong with the implementation"

    # Expected unitary after calculation is identity.
    expected_unitary = identity_matrix(no_of_qubits)

    # X_1 * X_2^dagger * np.conj((X_1 * X_2^dagger)[0,0]) = I
    m = np.matmul(v, inverse_matrix)
    generated_unitary = m * np.conjugate(m[0, 0])

    if generated_unitary.shape != expected_unitary.shape:
        return False, "Unitary V has different shape."

    if not np.allclose(generated_unitary, expected_unitary, atol=ABS_TOLERANCE, rtol=REL_TOLERANCE):
        return False, "Resulting matrix should be an Identity"

    return True, ""


# Relative Dirty Wasting-Separable
def verify_circuit_relative_dirty_wasting_separable(
    unitary_matrix, controls_no: int, auxiliaries_no: int
):
    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    inverse_matrix = load_matrix("reverse_noauxiliary", controls_no)

    v_shape = 2 ** (controls_no + 1)
    w_shape = 2 ** (auxiliaries_no)

    v, w = reverse_kronecker_product(unitary_matrix, (v_shape, v_shape))

    no_of_qubits = controls_no + 1

    # check shape of w
    if w.shape != (w_shape, w_shape):
        return False, "Unitary W has different shape."

    # check if w is unitary
    check_w = np.matmul(w, np.linalg.inv(w))

    if not np.allclose(
        check_w, identity_matrix(auxiliaries_no), atol=ABS_TOLERANCE, rtol=REL_TOLERANCE
    ):
        return False, "Resulting matrix should be identity"

    expected_unitary = identity_matrix(no_of_qubits)

    m = np.matmul(v, inverse_matrix)
    generated_unitary = np.absolute(m)

    if generated_unitary.shape != expected_unitary.shape:
        return False, "Unitary V has different shape."

    if not np.allclose(generated_unitary, expected_unitary, atol=ABS_TOLERANCE, rtol=REL_TOLERANCE):
        return False, "Resulting matrix should be identity"

    return True, ""
