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

    # slice the matrix M = U[0:2**n,0:2**n]  (n = controls qubit + target qubit)
    unitary_matrix = unitary_matrix[: 2 ** (controls_no + 1), : 2 ** (controls_no + 1)]

    # get mct inverse matrix
    inverse_matrix = load_matrix("noauxiliary", controls_no)

    no_of_qubits = controls_no + 1

    # X_1 * X_2^dagger * np.conj((X_1 * X_2^dagger)[0,0]) - I = 0
    m = np.matmul(unitary_matrix, inverse_matrix)
    generated_unitary = m * np.conjugate(m[0, 0]) - identity_matrix(no_of_qubits)

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
        return False, "Generated matrix should be all 0"

    return True, ""


# Relative Clean Non-Wasting
def verify_circuit_relative_clean_non_wasting(
    unitary_matrix, controls_no: int, auxiliaries_no: int
):
    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # slice the matrix M = U[0:2**n,0:2**n]  (n = controls qubit + target qubit)
    unitary_matrix = unitary_matrix[: 2 ** (controls_no + 1), : 2 ** (controls_no + 1)]

    # get mct inverse matrix
    inverse_matrix = load_matrix("noauxiliary", controls_no)

    no_of_qubits = controls_no + 1

    # X_1 * X_2^dagger - I = 0
    m = np.matmul(unitary_matrix, inverse_matrix)
    generated_unitary = np.absolute(m) - identity_matrix(no_of_qubits)

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

    # X_1 * X_2^dagger * np.conj((X_1 * X_2^dagger)[0,0]) - I = 0
    m = np.matmul(unitary_matrix, inverse_matrix)
    generated_unitary = (m * np.conjugate(m[0, 0])) - identity_matrix(no_of_qubits)

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


# Relative Dirty Non-Wasting
def verify_circuit_relative_dirty_non_wasting(
    unitary_matrix, controls_no: int, auxiliaries_no: int
):
    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    inverse_matrix = load_matrix("noauxiliary", controls_no)
    I_ct = identity_matrix(controls_no + 1)  # I_C,T

    i_a = identity_matrix(auxiliaries_no)  # I_A
    ket_0_a = ket_0_matrix(auxiliaries_no)  # |0>_A

    # tensor with the I for the Auxiliary qubit
    inverse_matrix_I = np.kron(i_a, inverse_matrix)  # --> (U_MCT^\dagger @ I_A)

    # print(inverse_matrix_I.shape, " - ", np.kron(ket_0_a, I_ct).T.shape)

    A = np.kron(ket_0_a, I_ct)  # A = ( I_C,T @ <0|_A )
    B = np.matmul(inverse_matrix_I, np.kron(ket_0_a, I_ct).T)  # B = (U_MCT @ I_A) ( I_C,T @ |0>_A )
    dr = np.matmul(A, np.matmul(unitary_matrix, B))  # D^R = A * U * B

    no_of_qubits = controls_no + auxiliaries_no + 1

    # ( ( ( D^R )^\dagger @ I_A) * U * inverse_matrix ) - I = 0
    generated_unitary = np.matmul(
        np.kron(i_a, np.linalg.inv(dr)), np.matmul(unitary_matrix, inverse_matrix_I)
    ) - identity_matrix(no_of_qubits)

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
        return False, "Generated matrix should be all 0"

    return True, ""


# Strict Clean Wasting-Entangled
def verify_circuit_strict_clean_wasting_entangled(
    unitary_matrix, controls_no: int, auxiliaries_no: int
):
    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    inverse_matrix = load_matrix("noauxiliary", controls_no)

    # || ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>) ||_2

    i_a = identity_matrix(auxiliaries_no)  # I_A
    ket_0_a = ket_0_matrix(auxiliaries_no)  # |0>_A

    u_mct_i = np.kron(i_a, inverse_matrix)  # (U_MCT @ I)

    for i in range(2 ** (controls_no + 1)):
        ket_b_ct = np.zeros(2 ** (controls_no + 1))

        ket_b_ct[i] = 1  # |b_C,T>

        bct_0a = np.kron(ket_0_a, ket_b_ct)  # (|b_C,T> @ |0_A>)

        res_1 = np.matmul(unitary_matrix, bct_0a)  # U_tilde(|b_C,T> @ |0_A>)

        res_2 = np.matmul(u_mct_i, res_1)  # (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>)

        ket_b_ct_i = np.kron(i_a, np.conj(ket_b_ct).T)  # ( <b_C,T| @ I_A )
        res_3 = np.matmul(
            ket_b_ct_i, res_2
        )  # ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>)

        # res_4 = np.matmul(
        #    np.conj(res_3).T, res_3
        # )  # || ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>) ||_2
        res_4 = np.linalg.norm(res_3)

        if np.round(res_4) != 1:
            return False, "The length should be 1"

    return True, ""


# Relative Clean Wasting-Entangled
def verify_circuit_relative_clean_wasting_entangled(
    unitary_matrix, controls_no: int, auxiliaries_no: int
):
    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    inverse_matrix = load_matrix("noauxiliary", controls_no)

    # || ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>) ||_2

    i_a = identity_matrix(auxiliaries_no)  # I_A
    ket_0_a = ket_0_matrix(auxiliaries_no)  # |0>_A

    u_mct_i = np.kron(i_a, inverse_matrix)  # (U_MCT @ I)

    for i in range(2 ** (controls_no + 1)):
        ket_b_ct = np.zeros(2 ** (controls_no + 1))

        ket_b_ct[i] = 1  # |b_C,T>

        bct_0a = np.kron(ket_0_a, ket_b_ct)  # (|b_C,T> @ |0_A>)

        res_1 = np.matmul(unitary_matrix, bct_0a)  # U_tilde(|b_C,T> @ |0_A>)

        res_2 = np.matmul(u_mct_i, res_1)  # (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>)

        ket_b_ct_i = np.kron(i_a, np.conj(ket_b_ct).T)  # ( <b_C,T| @ I_A )
        res_3 = np.matmul(
            ket_b_ct_i, res_2
        )  # ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>)

        # res_4 = np.matmul(
        #    np.conj(res_3).T, res_3
        # )  # || ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>) ||_2
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

    # || ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>) ||_2

    i_a = identity_matrix(auxiliaries_no)  # I_A
    ket_0_a = ket_0_matrix(auxiliaries_no)  # |0>_A

    u_mct_i = np.kron(i_a, inverse_matrix)  # (U_MCT @ I)

    phi_0 = np.zeros(2)

    for i in range(2 ** (controls_no + 1)):
        ket_b_ct = np.zeros(2 ** (controls_no + 1))

        ket_b_ct[i] = 1  # |b_C,T>

        bct_0a = np.kron(ket_0_a, ket_b_ct)  # (|b_C,T> @ |0_A>)

        res_1 = np.matmul(unitary_matrix, bct_0a)  # U_tilde(|b_C,T> @ |0_A>)

        res_2 = np.matmul(u_mct_i, res_1)  # (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>)

        ket_b_ct_i = np.kron(i_a, np.conj(ket_b_ct).T)  # ( <b_C,T| @ I_A )
        res_3 = np.matmul(
            ket_b_ct_i, res_2
        )  # ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>)

        # this is to get the |\phi_0>
        if i == 0:
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

    # || ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>) ||_2

    i_a = identity_matrix(auxiliaries_no)  # I_A
    ket_0_a = ket_0_matrix(auxiliaries_no)  # |0>_A

    i_ct = identity_matrix(controls_no + 1)  # I_ct
    u_mct_i = np.kron(i_a, inverse_matrix)  # (U_MCT @ I_A)

    i_ct_0 = np.kron(ket_0_a, i_ct)  # ( I_ct @ |0>_A )

    # U_tilde (U_MCT @ I_A)
    res_1 = np.matmul(unitary_matrix, u_mct_i)

    i_ct_0_t = np.kron(ket_0_a.T, i_ct.T)  # ( I_ct @ <0|_A )

    # ( I_ct @ <0|_A ) U_tilde (U_MCT @ I_A)
    res_2 = np.matmul(i_ct_0_t, res_1)

    # D_R = ( I_ct @ <0|_A ) U_tilde (U_MCT @ I_A) ( I_ct @ |0>_A )
    d_r = np.matmul(res_2, i_ct_0.T)

    phi_0 = np.zeros(2)

    for i in range(2 ** (controls_no + 1)):
        ket_b_ct = np.zeros(2 ** (controls_no + 1))

        ket_b_ct[i] = 1  # |b_C,T>

        bct_0a = np.kron(ket_0_a, ket_b_ct)  # (|b_C,T> @ |0_A>)

        res_1 = np.matmul(unitary_matrix, bct_0a)  # U_tilde(|b_C,T> @ |0_A>)

        res_2 = np.matmul(u_mct_i, res_1)  # (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>)

        ket_b_ct_i = np.kron(i_a, np.conj(ket_b_ct).T)  # ( <b_C,T| @ I_A )

        # ( D_R^\dagger @ I_A )
        d_r_i = np.kron(i_a, np.linalg.inv(d_r))

        res_3 = np.matmul(
            d_r_i, res_2
        )  # ( (D_R^\dagger @ I_A) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>) )

        res_4 = np.matmul(
            ket_b_ct_i, res_3
        )  # ( <b_C,T| @ I_A ) ((D_R^\dagger @ I_A) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>)) )

        # res_4 should be a quantum_state
        # check if res_4 a quantum state here

        # this is to get the |\phi_0>
        if i == 0:
            phi_0 = res_4

        # check if res_3 a quantum state here
        if np.round(np.matmul(phi_0.T, res_4)) != 1:
            return False, "The state should be a quantum state"

    return True, ""


# Strict Dirty Wasting-Entangled
def verify_circuit_strict_dirty_wasting_entangled(
    unitary_matrix, controls_no: int, auxiliaries_no: int
):
    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    # inverse_matrix = load_matrix("noauxiliary", controls_no)

    i_a = identity_matrix(auxiliaries_no)

    # Expected unitary after calculation is 0.
    expected_unitary = zero_matrix(auxiliaries_no)

    for i in range(2 ** (controls_no + 1)):
        # print("-----------")
        ket_b_ct = np.zeros(2 ** (controls_no + 1))

        ket_b_ct[i] = 1  # |b_C,T>

        ket_b_ct_i = np.kron(i_a, np.conj(ket_b_ct))  # ( |b_C,T> @ I_A )

        # print(np.round(np.linalg.det(unitary_matrix)))

        res_1 = np.matmul(ket_b_ct_i, unitary_matrix)  # U_tilde ( |b_C,T> @ I_A )

        v_b = np.matmul(res_1, ket_b_ct_i.T)  # ( <b_C,T| @ I_A ) U_tilde ( |b_C,T> @ I_A )

        # print(np.round(v_b))
        # print(np.linalg.det(v_b))

        if np.linalg.det(v_b) == 0:
            return False, "Cannot get inverse of singular matrix"

        res = np.matmul(v_b, np.linalg.inv(v_b))

        # check that (V_b * V_B') - I = 0
        if (
            np.allclose(
                res - i_a, expected_unitary, atol=absolute_error_tol, rtol=relative_error_tol
            )
            is False
        ):
            return False, "Something wrong with the implementation"

    return True, ""


# Strict Dirty Wasting-Separable
def verify_circuit_strict_dirty_wasting_separable(
    unitary_matrix, controls_no: int, auxiliaries_no: int
):
    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    inverse_matrix = load_matrix("reverse_noauxiliary", controls_no)

    b_shape = 2 ** (controls_no + 1)
    c_shape = 2 ** (auxiliaries_no)

    b, c = reverse_kronecker_product(unitary_matrix, (b_shape, b_shape))

    no_of_qubits = controls_no + 1

    # check shape of c
    if c.shape != (c_shape, c_shape):
        return False, "Unitary C has different shape."

    # check if c is unitary
    check_c = np.matmul(c, np.linalg.inv(c))  # will be faster to multiply with the dagger

    if (
        np.allclose(
            check_c,
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
    m = np.matmul(b, inverse_matrix)
    generated_unitary = m * np.conjugate(m[0, 0])

    if generated_unitary.shape != expected_unitary.shape:
        return False, "Unitary B has different shape."

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


# Relative Dirty Wasting-Separable
def verify_circuit_relative_dirty_wasting_separable(
    unitary_matrix, controls_no: int, auxiliaries_no: int
):
    if auxiliaries_no == 0:
        return False, "No of Auxiliary qubit should bigger than 0"

    # get mct inverse matrix
    inverse_matrix = load_matrix("reverse_noauxiliary", controls_no)

    b_shape = 2 ** (controls_no + 1)
    c_shape = 2 ** (auxiliaries_no)

    b, c = reverse_kronecker_product(unitary_matrix, (b_shape, b_shape))

    no_of_qubits = controls_no + 1

    # check shape of c
    if c.shape != (c_shape, c_shape):
        return False, "Unitary C has different shape."

    # check if c is unitary
    check_c = np.matmul(c, np.linalg.inv(c))

    if (
        np.allclose(
            check_c,
            identity_matrix(auxiliaries_no),
            atol=absolute_error_tol,
            rtol=relative_error_tol,
        )
        is False
    ):
        return False, "Something wrong with the implementation"

    # Expected unitary after calculation is identity.
    expected_unitary = identity_matrix(no_of_qubits)

    # X_1 * X_2^dagger = I
    m = np.matmul(b, inverse_matrix)
    generated_unitary = np.absolute(m)

    if generated_unitary.shape != expected_unitary.shape:
        return False, "Unitary B has different shape."

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
#         assert rd["RCWE"]

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
#         assert rd["RCWE"]
