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

from qumcat.implementations.mct_n_qubit_decomposition import MCTNQubitDecomposition

implementation = MCTNQubitDecomposition


@pytest.mark.parametrize("controls_no", [5])
def test_generate_circuit_dirty_ancilla(controls_no):
    mct = implementation(controls_no)

    circ = mct.generate_circuit()

    no_of_qubits = 0

    # get unitary matrix
    unitary_matrix = np.array(np.absolute(usim.run(circ).result().get_unitary()))

    # get mct inverse matrix
    inverse_matrix = load_matrix("noancilla", controls_no)
    inverse_matrix = np.kron(identity_matrix(mct.num_ancilla_qubits()), inverse_matrix)

    no_of_qubits = controls_no + mct.num_ancilla_qubits() + 1

    # X_1 * X_2^dagger * np.conj((X_1 * X_2^dagger)[0,0]) - I = 0
    M = np.matmul(unitary_matrix, inverse_matrix)
    generated_unitary = M * np.conjugate(M[0, 0]) - identity_matrix(no_of_qubits)

    # Expected unitary after calculation is 0.
    expected_unitary = zero_matrix(no_of_qubits)

    assert generated_unitary.shape == expected_unitary.shape

    assert (
        check_all_zero(generated_unitary, absolute_error_tol, relative_error_tol) == 1
    ), "Result should close to 0"


@pytest.mark.parametrize("controls_no", [5])
def test_generate_circuit_dirty_ancilla_relative_phase(controls_no):
    mct = implementation(controls_no)

    circ = mct.generate_circuit()

    no_of_qubits = 0

    # get unitary matrix
    unitary_matrix = np.array(np.absolute(usim.run(circ).result().get_unitary()))  # --> U

    # get mct inverse matrix
    inverse_matrix = load_matrix("noancilla", controls_no)

    # I_C,T
    I_ct = identity_matrix(mct._n + 1)

    # I_A
    I_a = identity_matrix(mct.num_ancilla_qubits())

    # |0>_A
    ket_0_A = ket_0_matrix(mct.num_ancilla_qubits())

    # tensor with the I for the Ancilla qubit
    inverse_matrix_I = np.kron(I_a, inverse_matrix)  # --> (U_MCT^\dagger @ I_A)

    # D^R = A * U * B
    # A = ( I_C,T @ <0|_A )
    A = np.kron(ket_0_A, I_ct)

    # B = (U_MCT @ I_A) ( I_C,T @ |0>_A )
    B = np.matmul(inverse_matrix_I, np.kron(ket_0_A, I_ct).T)

    dr = np.matmul(A, np.matmul(unitary_matrix, B))

    no_of_qubits = controls_no + mct.num_ancilla_qubits() + 1

    # ( ( ( D^R )^\dagger @ I_A) * U * inverse_matrix ) - I = 0

    generated_unitary = np.matmul(
        np.kron(I_a, np.linalg.inv(dr)), np.matmul(unitary_matrix, inverse_matrix_I)
    ) - identity_matrix(no_of_qubits)

    # Expected unitary after calculation is 0.
    expected_unitary = zero_matrix(no_of_qubits)

    assert generated_unitary.shape == expected_unitary.shape

    assert (
        check_all_zero(generated_unitary, absolute_error_tol, relative_error_tol) == 1
    ), "Result should close to 0"


@pytest.mark.parametrize("controls_no", [5])
def test_generate_circuit_clean_ancilla(controls_no):
    mct = implementation(controls_no)

    circ = mct.generate_circuit()

    # get unitary matrix
    unitary_matrix = np.array(usim.run(circ).result().get_unitary())

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

    assert (
        check_all_zero(generated_unitary, absolute_error_tol, relative_error_tol) == 1
    ), "Result should close to 0"


@pytest.mark.parametrize("controls_no", [5])
def test_generate_circuit_clean_ancilla_relative_phase(controls_no):
    mct = implementation(controls_no)

    circ = mct.generate_circuit()

    no_of_qubits = 0

    # get unitary matrix
    unitary_matrix = np.array(np.absolute(usim.run(circ).result().get_unitary()))

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

    assert (
        check_all_zero(generated_unitary, absolute_error_tol, relative_error_tol) == 1
    ), "Result should close to 0"


@pytest.mark.parametrize("controls_no", [5])
def test_generate_circuit_clean_wasted_ancilla(controls_no):
    mct = implementation(controls_no)

    circ = mct.generate_circuit()

    # get unitary matrix
    unitary_matrix = np.array(usim.run(circ).result().get_unitary())

    # get mct inverse matrix
    inverse_matrix = load_matrix("noancilla", controls_no)

    # || ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>) ||_2

    # |0>_A
    ket_0_A = ket_0_matrix(mct.num_ancilla_qubits())

    I_A = identity_matrix(mct.num_ancilla_qubits())

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

        res_4 = np.matmul(
            np.conj(res_3).T, res_3
        )  # || ( <b_C,T| @ I_A ) (U_MCT @ I) U_tilde(|b_C,T> @ |0_A>) ||_2

        assert np.round(res_4) == 1, "The length should be 1"


@pytest.mark.parametrize(
    "controls_no", [pytest.param(5, marks=pytest.mark.xfail, id="accepted-fail")]
)
def test_generate_circuit_no_ancilla(controls_no):
    mct = implementation(controls_no)

    circ = mct.generate_circuit()

    no_of_qubits = 0

    # get unitary matrix
    unitary_matrix = np.array(usim.run(circ).result().get_unitary())

    # get mct inverse matrix
    inverse_matrix = load_matrix("noancilla", controls_no)

    no_of_qubits = controls_no + 1

    # X_1 * X_2^dagger * np.conj((X_1 * X_2^dagger)[0,0]) - I = 0
    M = np.matmul(unitary_matrix, inverse_matrix)
    generated_unitary = M * np.conjugate(M[0, 0]) - identity_matrix(no_of_qubits)

    # Expected unitary after calculation is 0.
    expected_unitary = zero_matrix(no_of_qubits)

    assert generated_unitary.shape == expected_unitary.shape

    assert (
        check_all_zero(generated_unitary, absolute_error_tol, relative_error_tol) == 1
    ), "Result should close to 0"


@pytest.mark.parametrize(
    "controls_no", [pytest.param(5, marks=pytest.mark.xfail, id="accepted-fail")]
)
def test_generate_circuit_no_ancilla_relative_phase(controls_no):
    mct = implementation(controls_no)

    circ = mct.generate_circuit()

    no_of_qubits = 0

    # get unitary matrix
    unitary_matrix = np.array(np.absolute(usim.run(circ).result().get_unitary()))

    # get mct inverse matrix
    inverse_matrix = load_matrix("noancilla", controls_no)

    no_of_qubits = controls_no + 1

    # X_1 * X_2^dagger - I = 0
    M = np.matmul(unitary_matrix, inverse_matrix)
    generated_unitary = M - identity_matrix(no_of_qubits)

    # Expected unitary after calculation is 0.
    expected_unitary = zero_matrix(no_of_qubits)

    assert generated_unitary.shape == expected_unitary.shape

    assert (
        check_all_zero(generated_unitary, absolute_error_tol, relative_error_tol) == 1
    ), "Result should close to 0"
