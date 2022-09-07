import numpy as np
import pytest
from functions import check_all_zero, identity_matrix, ket_0_matrix, load_matrix, zero_matrix
from qiskit import Aer

from qumcat.implementations.mct_vchain_dirty import MCTVChainDirty

absolute_error_tol = 1e-3
relative_error_tol = 1e-3
usim = Aer.get_backend("unitary_simulator")


@pytest.mark.parametrize("implementation", [MCTVChainDirty])
@pytest.mark.parametrize("controls_no", [4, 5, 6])
def test_generate_circuit_dirty_ancilla(implementation, controls_no):
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


@pytest.mark.dirty_relative
@pytest.mark.parametrize("implementation", [MCTVChainDirty])
@pytest.mark.parametrize("controls_no", [3, 4, 5, 6])
def test_generate_circuit_dirty_ancilla_relative_phase(implementation, controls_no):
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
