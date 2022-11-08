import numpy as np
import pytest
from functions import (
    absolute_error_tol,
    check_all_zero,
    identity_matrix,
    ket_0_matrix,
    load_matrix,
    relative_error_tol,
    usim,
    zero_matrix,
)


# 1.1 No Ancilla
def generate_circuit_no_ancilla(unitary_matrix, controls_no: int, ancillas_no: int):
    # get mct inverse matrix
    inverse_matrix = load_matrix("noancilla", controls_no)

    no_of_qubits = controls_no + 1

    # X_1 * X_2^dagger * np.conj((X_1 * X_2^dagger)[0,0]) - I = 0
    M = np.matmul(unitary_matrix, inverse_matrix)
    generated_unitary = M * np.conjugate(M[0, 0]) - identity_matrix(no_of_qubits)

    # Expected unitary after calculation is 0.
    expected_unitary = zero_matrix(no_of_qubits)

    assert generated_unitary.shape == expected_unitary.shape

    assert np.allclose(
        generated_unitary, expected_unitary, atol=absolute_error_tol, rtol=relative_error_tol
    )


# 1.2 No Ancilla Relative
def generate_circuit_no_ancilla_relative(unitary_matrix, controls_no: int, ancillas_no: int):
    # get mct inverse matrix
    inverse_matrix = load_matrix("noancilla", controls_no)

    no_of_qubits = controls_no + 1

    # X_1 * X_2^dagger - I = 0
    M = np.matmul(unitary_matrix, inverse_matrix)
    generated_unitary = M - identity_matrix(no_of_qubits)

    # Expected unitary after calculation is 0.
    expected_unitary = zero_matrix(no_of_qubits)

    assert generated_unitary.shape == expected_unitary.shape

    assert np.allclose(
        generated_unitary, expected_unitary, atol=absolute_error_tol, rtol=relative_error_tol
    )


# 2.1 Clean Non-wasted
def generate_circuit_clean_ancilla(unitary_matrix, controls_no: int, ancillas_no: int):

    # slice the matrix M = U[0:2**n,0:2**n]  (n = controls qubit + target qubit)
    unitary_matrix = unitary_matrix[: 2 ** (controls_no + 1), : 2 ** (controls_no + 1)]

    # get mct inverse matrix
    inverse_matrix = load_matrix("noancilla", controls_no)

    no_of_qubits = controls_no + 1

    # X_1 * X_2^dagger * np.conj((X_1 * X_2^dagger)[0,0]) - I = 0
    M = np.matmul(unitary_matrix, inverse_matrix)
    generated_unitary = M * np.conjugate(M[0, 0]) - identity_matrix(no_of_qubits)

    # Expected unitary after calculation is 0.
    expected_unitary = zero_matrix(no_of_qubits)

    assert generated_unitary.shape == expected_unitary.shape

    print(np.round(generated_unitary))

    assert np.allclose(
        generated_unitary, expected_unitary, atol=absolute_error_tol, rtol=relative_error_tol
    ), "Generated matrix should be all 0"


# 2.2 Clean Non-wasted Relative
def generate_circuit_clean_relative_ancilla(unitary_matrix, controls_no: int, ancillas_no: int):

    # slice the matrix M = U[0:2**n,0:2**n]  (n = controls qubit + target qubit)
    unitary_matrix = unitary_matrix[: 2 ** (controls_no + 1), : 2 ** (controls_no + 1)]

    # get mct inverse matrix
    inverse_matrix = load_matrix("noancilla", controls_no)

    no_of_qubits = controls_no + 1

    # X_1 * X_2^dagger - I = 0
    M = np.matmul(unitary_matrix, inverse_matrix)
    generated_unitary = M - identity_matrix(no_of_qubits)

    # Expected unitary after calculation is 0.
    expected_unitary = zero_matrix(no_of_qubits)

    assert generated_unitary.shape == expected_unitary.shape

    assert np.allclose(
        generated_unitary, expected_unitary, atol=absolute_error_tol, rtol=relative_error_tol
    )


# 3.1 Dirty Non-Wasted
def generate_circuit_dirty_ancilla(unitary_matrix, controls_no: int, ancillas_no: int):
    # get mct inverse matrix
    inverse_matrix = load_matrix("noancilla", controls_no)
    inverse_matrix = np.kron(identity_matrix(ancillas_no), inverse_matrix)

    no_of_qubits = controls_no + ancillas_no + 1

    # X_1 * X_2^dagger * np.conj((X_1 * X_2^dagger)[0,0]) - I = 0
    M = np.matmul(unitary_matrix, inverse_matrix)
    generated_unitary = M * np.conjugate(M[0, 0]) - identity_matrix(no_of_qubits)

    # Expected unitary after calculation is 0.
    expected_unitary = zero_matrix(no_of_qubits)

    assert generated_unitary.shape == expected_unitary.shape

    assert np.allclose(
        generated_unitary, expected_unitary, atol=absolute_error_tol, rtol=relative_error_tol
    )


# 3.2 Dirty Non-Wasted Relative
def generate_circuit_dirty_relative_ancilla(unitary_matrix, controls_no: int, ancillas_no: int):
    # get mct inverse matrix
    inverse_matrix = load_matrix("noancilla", controls_no)
    I_ct = identity_matrix(controls_no + 1)  # I_C,T
    I_a = identity_matrix(ancillas_no)  # I_A
    ket_0_A = ket_0_matrix(ancillas_no)  # |0>_A

    # tensor with the I for the Ancilla qubit
    inverse_matrix_I = np.kron(I_a, inverse_matrix)  # --> (U_MCT^\dagger @ I_A)

    A = np.kron(ket_0_A, I_ct)  # A = ( I_C,T @ <0|_A )
    B = np.matmul(inverse_matrix_I, np.kron(ket_0_A, I_ct).T)  # B = (U_MCT @ I_A) ( I_C,T @ |0>_A )
    dr = np.matmul(A, np.matmul(unitary_matrix, B))  # D^R = A * U * B

    no_of_qubits = controls_no + ancillas_no + 1

    # ( ( ( D^R )^\dagger @ I_A) * U * inverse_matrix ) - I = 0
    generated_unitary = np.matmul(
        np.kron(I_a, np.linalg.inv(dr)), np.matmul(unitary_matrix, inverse_matrix_I)
    ) - identity_matrix(no_of_qubits)

    # Expected unitary after calculation is 0.
    expected_unitary = zero_matrix(no_of_qubits)

    assert generated_unitary.shape == expected_unitary.shape

    assert np.allclose(
        generated_unitary, expected_unitary, atol=absolute_error_tol, rtol=relative_error_tol
    )


# 4.1 Clean Wasted Entangled Leftout
def generate_circuit_clean_wasted_entangled_ancilla(
    unitary_matrix, controls_no: int, ancillas_no: int
):
    # get mct inverse matrix
    inverse_matrix = load_matrix("noancilla", controls_no)

    # || ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>) ||_2

    # |0>_A
    ket_0_A = ket_0_matrix(ancillas_no)

    I_A = identity_matrix(ancillas_no)

    for i in range(2 ** (controls_no + 1)):
        ket_b_ct = np.zeros(2 ** (controls_no + 1))

        ket_b_ct[i] = 1  # |b_C,T>

        bct_0a = np.kron(ket_0_A, ket_b_ct)  # (|b_C,T> @ |0_A>)

        res_1 = np.matmul(unitary_matrix, bct_0a)  # U_tilde(|b_C,T> @ |0_A>)

        u_mct_i = np.kron(I_A, inverse_matrix)  # (U_MCT @ I)
        res_2 = np.matmul(u_mct_i, res_1)  # (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>)

        ket_b_ct_i = np.kron(I_A, np.conj(ket_b_ct).T)  # ( <b_C,T| @ I_A )
        res_3 = np.matmul(
            ket_b_ct_i, res_2
        )  # ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>)

        # res_4 = np.matmul(
        #    np.conj(res_3).T, res_3
        # )  # || ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>) ||_2
        res_4 = np.linalg.norm(res_3)

        assert np.round(res_4) == 1, "The length should be 1"


# 4.2 Clean Wasted Relative Entangled Leftout
# currently it is the same with 4.1
def generate_circuit_clean_wasted_relative_entangled_ancilla(
    unitary_matrix, controls_no: int, ancillas_no: int
):
    # get mct inverse matrix
    inverse_matrix = load_matrix("noancilla", controls_no)

    # || ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>) ||_2

    # |0>_A
    ket_0_A = ket_0_matrix(ancillas_no)

    I_A = identity_matrix(ancillas_no)

    for i in range(2 ** (controls_no + 1)):
        ket_b_ct = np.zeros(2 ** (controls_no + 1))

        ket_b_ct[i] = 1  # |b_C,T>

        bct_0a = np.kron(ket_0_A, ket_b_ct)  # (|b_C,T> @ |0_A>)

        res_1 = np.matmul(unitary_matrix, bct_0a)  # U_tilde(|b_C,T> @ |0_A>)

        u_mct_i = np.kron(I_A, inverse_matrix)  # (U_MCT @ I)
        res_2 = np.matmul(u_mct_i, res_1)  # (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>)

        ket_b_ct_i = np.kron(I_A, np.conj(ket_b_ct).T)  # ( <b_C,T| @ I_A )
        res_3 = np.matmul(
            ket_b_ct_i, res_2
        )  # ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>)

        # res_4 = np.matmul(
        #    np.conj(res_3).T, res_3
        # )  # || ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>) ||_2
        res_4 = np.linalg.norm(res_3)

        assert np.round(res_4) == 1, "The length should be 1"


# 4.3 Clean Wasted Separable
def generate_circuit_clean_wasted_separable_ancilla(
    unitary_matrix, controls_no: int, ancillas_no: int
):
    # get mct inverse matrix
    inverse_matrix = load_matrix("noancilla", controls_no)

    # || ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>) ||_2

    # |0>_A
    ket_0_A = ket_0_matrix(ancillas_no)

    I_A = identity_matrix(ancillas_no)

    phi_0 = np.zeros(2)

    for i in range(2 ** (controls_no + 1)):
        ket_b_ct = np.zeros(2 ** (controls_no + 1))

        ket_b_ct[i] = 1  # |b_C,T>

        bct_0a = np.kron(ket_0_A, ket_b_ct)  # (|b_C,T> @ |0_A>)

        res_1 = np.matmul(unitary_matrix, bct_0a)  # U_tilde(|b_C,T> @ |0_A>)

        u_mct_i = np.kron(I_A, inverse_matrix)  # (U_MCT @ I)
        res_2 = np.matmul(u_mct_i, res_1)  # (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>)

        ket_b_ct_i = np.kron(I_A, np.conj(ket_b_ct).T)  # ( <b_C,T| @ I_A )
        res_3 = np.matmul(
            ket_b_ct_i, res_2
        )  # ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>)

        # this is to get the |\phi_0>
        if i == 0:
            phi_0 = res_3

        # check if res_3 a quantum state here
        assert np.round(np.matmul(phi_0.T, res_3)) == 1, "The state should be a quantum state"


# 4.4 Clean Wasted Relative Separable
def generate_circuit_clean_wasted_relative_separable_ancilla(
    unitary_matrix, controls_no: int, ancillas_no: int
):
    # get mct inverse matrix
    inverse_matrix = load_matrix("noancilla", controls_no)

    # || ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>) ||_2

    # |0>_A
    ket_0_A = ket_0_matrix(ancillas_no)

    I_A = identity_matrix(ancillas_no)

    I_ct = identity_matrix(controls_no + 1)  # I_ct
    u_mct_i = np.kron(I_A, inverse_matrix)  # (U_MCT @ I_A)
    ket_0_A = ket_0_matrix(ancillas_no)  # |0>_A

    I_ct_0 = np.kron(ket_0_A, I_ct)  # ( I_ct @ |0>_A )

    # U_tilde (U_MCT @ I_A)
    res_1 = np.matmul(unitary_matrix, u_mct_i)

    I_ct_0_T = np.kron(ket_0_A.T, I_ct.T)  # ( I_ct @ <0|_A )

    # ( I_ct @ <0|_A ) U_tilde (U_MCT @ I_A)
    res_2 = np.matmul(I_ct_0_T, res_1)

    # D_R = ( I_ct @ <0|_A ) U_tilde (U_MCT @ I_A) ( I_ct @ |0>_A )
    D_R = np.matmul(res_2, I_ct_0.T)

    phi_0 = np.zeros(2)

    for i in range(2 ** (controls_no + 1)):
        ket_b_ct = np.zeros(2 ** (controls_no + 1))

        ket_b_ct[i] = 1  # |b_C,T>

        bct_0a = np.kron(ket_0_A, ket_b_ct)  # (|b_C,T> @ |0_A>)

        res_1 = np.matmul(unitary_matrix, bct_0a)  # U_tilde(|b_C,T> @ |0_A>)

        u_mct_i = np.kron(I_A, inverse_matrix)  # (U_MCT @ I)
        res_2 = np.matmul(u_mct_i, res_1)  # (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>)

        ket_b_ct_i = np.kron(I_A, np.conj(ket_b_ct).T)  # ( <b_C,T| @ I_A )

        # ( D_R^\dagger @ I_A )
        D_R_I = np.kron(I_A, np.linalg.inv(D_R))

        res_3 = np.matmul(
            D_R_I, res_2
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
        assert np.round(np.matmul(phi_0.T, res_4)) == 1, "The state should be a quantum state"
