import numpy as np
import pytest
from functions import check_all_zero, identity_matrix, load_matrix, zero_matrix
from qiskit import Aer

from qumcat.mct_n_qubit_decomposition import MCTNQubitDecomposition

# from qumcat.mct_no_ancilla import MCTNoAncilla
from qumcat.mct_parallel_decomposition import MCTParallelDecomposition
from qumcat.mct_vchain import MCTVChain

# from qumcat.mct_vchain_dirty import MCTVChainDirty

absolute_error_tol = 1e-3
relative_error_tol = 1e-3
usim = Aer.get_backend("unitary_simulator")


@pytest.mark.clean_ancilla
@pytest.mark.parametrize(
    "implementation", [MCTVChain, MCTNQubitDecomposition, MCTParallelDecomposition]
)
@pytest.mark.parametrize("controls_no", [5, 6])
def test_generate_circuit_clean_ancilla(implementation, controls_no):
    mct = implementation(controls_no)

    circ = mct.generate_circuit()

    no_of_qubits = 0

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


@pytest.mark.clean_ancilla
@pytest.mark.parametrize(
    "implementation", [MCTVChain, MCTNQubitDecomposition, MCTParallelDecomposition]
)
@pytest.mark.parametrize("controls_no", [5, 6])
def test_generate_circuit_clean_ancilla_relative_phase(implementation, controls_no):
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
