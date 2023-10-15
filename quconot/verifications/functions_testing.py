import numpy as np

from .functions import (
    absolute_error_tol,
    identity_matrix,
    ket_0_matrix,
    load_matrix,
    relative_error_tol,
    zero_matrix,
)
from .reverse_kronecker_product import reverse_kronecker_product


# No Auxiliary
def verify_circuit_no_auxiliary(unitary_matrix, controls_no: int, auxiliaries_no: int):
    # get mct inverse matrix
    inverse_matrix = load_matrix("noauxiliary", controls_no)

    no_of_qubits = controls_no + 1

    # X_1 * X_2^dagger * np.conj((X_1 * X_2^dagger)[0,0]) - I = 0
    M = np.matmul(unitary_matrix, inverse_matrix)
    generated_unitary = M * np.conjugate(M[0, 0]) - identity_matrix(no_of_qubits)

    # Expected unitary after calculation is 0.
    expected_unitary = zero_matrix(no_of_qubits)

    if generated_unitary.shape != expected_unitary.shape:
        return False, "Unitary has different shape."

    if (
        np.allclose(
            generated_unitary,
            expected_unitary,
            atol=absolute_error_tol,
            rtol=relative_error_tol,
        )
        is False
    ):
        return False, "Something wrong with the implementation"

    return True, ""


# No Auxiliary Relative-phase
def verify_circuit_no_auxiliary_relative(unitary_matrix, controls_no: int, auxiliaries_no: int):
    # get mct inverse matrix
    inverse_matrix = load_matrix("noauxiliary", controls_no)

    no_of_qubits = controls_no + 1

    unitary_matrix = np.abs(unitary_matrix)

    # X_1 * X_2^dagger - I = 0
    M = np.matmul(unitary_matrix, inverse_matrix)
    generated_unitary = M - identity_matrix(no_of_qubits)

    # Expected unitary after calculation is 0.
    expected_unitary = zero_matrix(no_of_qubits)

    if generated_unitary.shape != expected_unitary.shape:
        return False, "Unitary has different shape."

    if (
        np.allclose(
            generated_unitary,
            expected_unitary,
            atol=absolute_error_tol,
            rtol=relative_error_tol,
        )
        is False
    ):
        return False, "Something wrong with the implementation"

    return True, ""


# Strict Clean Non-Wasting
def verify_circuit_strict_clean_non_wasting(unitary_matrix, controls_no: int, auxiliaries_no: int):
    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    inverse_matrix = load_matrix("noauxiliary", controls_no)

    i = identity_matrix(controls_no + 1)
    ket_0 = ket_0_matrix(auxiliaries_no)
    ket_0_i = np.kron(ket_0, i)

    unitary_matrix = np.matmul(np.matmul(ket_0_i, unitary_matrix), ket_0_i.T)

    no_of_qubits = controls_no + 1

    m = np.matmul(unitary_matrix, inverse_matrix)
    generated_unitary = m * np.conjugate(m[0, 0]) - identity_matrix(no_of_qubits)

    expected_unitary = zero_matrix(no_of_qubits)

    if generated_unitary.shape != expected_unitary.shape:
        return False, "Unitary has different shape."

    if (
        np.allclose(
            generated_unitary,
            expected_unitary,
            atol=absolute_error_tol,
            rtol=relative_error_tol,
        )
        is False
    ):
        return False, "Generated matrix should be all 0"

    return True, ""


# Relative Clean Non-Wasting
def verify_circuit_relative_clean_non_wasting(
    unitary_matrix, controls_no: int, auxiliaries_no: int
):
    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    inverse_matrix = load_matrix("noauxiliary", controls_no)
    # inverse_matrix = np.kron(identity_matrix(auxiliaries_no), inverse_matrix)

    i = identity_matrix(controls_no + 1)
    ket_0 = ket_0_matrix(auxiliaries_no)
    ket_0_i = np.kron(ket_0, i)

    unitary_matrix = np.matmul(np.matmul(ket_0_i, unitary_matrix), ket_0_i.T)

    no_of_qubits = controls_no + 1

    m = np.matmul(unitary_matrix, inverse_matrix)
    generated_unitary = np.absolute(m) - identity_matrix(no_of_qubits)

    expected_unitary = zero_matrix(no_of_qubits)

    if generated_unitary.shape != expected_unitary.shape:
        return False, "Unitary has different shape."

    if (
        np.allclose(
            generated_unitary,
            expected_unitary,
            atol=absolute_error_tol,
            rtol=relative_error_tol,
        )
        is False
    ):
        return False, "Generated matrix should be all 0"

    return True, ""


# Strict Dirty Non-Wasting
def verify_circuit_strict_dirty_non_wasting(unitary_matrix, controls_no: int, auxiliaries_no: int):
    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    inverse_matrix = load_matrix("noauxiliary", controls_no)
    inverse_matrix = np.kron(identity_matrix(auxiliaries_no), inverse_matrix)

    no_of_qubits = controls_no + auxiliaries_no + 1

    m = np.matmul(unitary_matrix, inverse_matrix)
    generated_unitary = (m * np.conjugate(m[0, 0])) - identity_matrix(no_of_qubits)

    expected_unitary = zero_matrix(no_of_qubits)

    if generated_unitary.shape != expected_unitary.shape:
        return False, "Unitary has different shape."

    if (
        np.allclose(
            generated_unitary,
            expected_unitary,
            atol=absolute_error_tol,
            rtol=relative_error_tol,
        )
        is False
    ):
        return False, "Generated matrix should be all 0"

    return True, ""


# Relative Dirty Non-Wasting
def verify_circuit_relative_dirty_non_wasting(
    unitary_matrix, controls_no: int, auxiliaries_no: int
):
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

    if (
        np.allclose(
            check_w,
            identity_matrix(auxiliaries_no),
            atol=absolute_error_tol,
            rtol=relative_error_tol,
        )
        is False
    ):
        return False, "Matrix W should be unitary"

    check_v = np.matmul(np.absolute(v), inverse_matrix)
    generated_unitary = check_v - identity_matrix(controls_no + 1)
    expected_unitary = zero_matrix(controls_no + 1)

    if generated_unitary.shape != expected_unitary.shape:
        return False, "Unitary V has different shape."

    if (
        np.allclose(
            generated_unitary,
            expected_unitary,
            atol=absolute_error_tol,
            rtol=relative_error_tol,
        )
        is False
    ):
        return False, "Generated matrix V should be all 0"

    return True, ""


# Strict Clean Wasting-Entangled
# Relative Clean Wasting-Entangled
def verify_circuit_strict_clean_wasting_entangled(
    unitary_matrix, controls_no: int, auxiliaries_no: int
):
    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    inverse_matrix = load_matrix("noauxiliary", controls_no)

    i = identity_matrix(auxiliaries_no)
    ket_0 = ket_0_matrix(auxiliaries_no)

    for idx in range(2 ** (controls_no + 1)):
        ket_b = np.zeros(2 ** (controls_no + 1))

        ket_b[idx] = 1

        b_0 = np.kron(ket_0, ket_b)

        res_1 = np.matmul(unitary_matrix, b_0)

        res_2 = np.kron(i, np.matmul(inverse_matrix, ket_b))

        res_3 = np.matmul(res_2, res_1)

        res_4 = np.linalg.norm(res_3)

        if np.round(res_4) != 1:
            return False, "The length should be 1"

    return True, ""


# Strict Dirty Wasting-Entangled
def verify_circuit_strict_dirty_wasting_entangled(
    unitary_matrix, controls_no: int, auxiliaries_no: int
):
    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    inverse_matrix = load_matrix("noauxiliary", controls_no)

    i = identity_matrix(auxiliaries_no)

    u_i = np.kron(i, inverse_matrix)

    for idx in range(2 ** (controls_no + auxiliaries_no + 1)):
        ket_bc = np.zeros(2 ** (controls_no + auxiliaries_no + 1))

        ket_bc[idx] = 1

        res_1 = np.matmul(unitary_matrix, ket_bc)

        res_2 = np.matmul(u_i, ket_bc)

        res_3 = np.matmul(res_2, res_1)

        res_4 = np.linalg.norm(res_3)

        if np.round(res_4) != 1:
            return False, "The length should be 1"

    return True, ""


# Strict Clean Wasting-Separable
def verify_circuit_strict_clean_wasting_separable(
    unitary_matrix, controls_no: int, auxiliaries_no: int
):
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
        if np.round(np.matmul(phi_0.T, res_3)) != 1:
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

    if (
        np.allclose(
            generated_unitary,
            expected_unitary,
            atol=absolute_error_tol,
            rtol=relative_error_tol,
        )
        is False
    ):
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

    if (
        np.allclose(
            check_w,
            identity_matrix(auxiliaries_no),
            atol=absolute_error_tol,
            rtol=relative_error_tol,
        )
        is False
    ):
        return False, "Something wrong with the implementation"

    # Expected unitary after calculation is identity.
    expected_unitary = identity_matrix(no_of_qubits)

    # X_1 * X_2^dagger * np.conj((X_1 * X_2^dagger)[0,0]) = I
    m = np.matmul(v, inverse_matrix)
    generated_unitary = m * np.conjugate(m[0, 0])

    if generated_unitary.shape != expected_unitary.shape:
        return False, "Unitary V has different shape."

    if (
        np.allclose(
            generated_unitary,
            expected_unitary,
            atol=absolute_error_tol,
            rtol=relative_error_tol,
        )
        is False
    ):
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

    if (
        np.allclose(
            check_w,
            identity_matrix(auxiliaries_no),
            atol=absolute_error_tol,
            rtol=relative_error_tol,
        )
        is False
    ):
        return False, "Resulting matrix should be identity"

    expected_unitary = identity_matrix(no_of_qubits)

    m = np.matmul(v, inverse_matrix)
    generated_unitary = np.absolute(m)

    if generated_unitary.shape != expected_unitary.shape:
        return False, "Unitary V has different shape."

    if (
        np.allclose(
            generated_unitary,
            expected_unitary,
            atol=absolute_error_tol,
            rtol=relative_error_tol,
        )
        is False
    ):
        return False, "Resulting matrix should be identity"

    return True, ""


# def verify_dependencies(rd):
#     if rd["SDNW"]:
#         assert rd["SCNW"]
#         assert rd["RDNW"]
#         assert rd["SDWS"]

#     if rd["RDNW"]:
#         assert rd["RCNW"]
#         assert rd["RDWS"]

#     if rd["SDWS"]:
#         assert rd["SCWS"]
#         assert rd["RDWS"]

#     if rd["SDWE"]:
#         assert rd["SCWE"]

#     if rd["SCNW"]:
#         assert rd["RCNW"]
#         assert rd["SCWS"]

#     if rd["SCWS"]:
#         assert rd["RCWS"]

#     if rd["RCNW"]:
#         assert rd["RCWS"]

#     if rd["RDWS"]:
#         assert rd["SDWE"]

#     if rd["RCWS"]:
#         assert rd["SCWE"]
