import numpy as np
import pytest
from functions import check_all_zero, identity_matrix, load_matrix, zero_matrix
from qiskit import Aer

from qumcat.implementations.mct_no_ancilla import MCTNoAncilla
from qumcat.implementations.mct_no_ancilla_relative_phase import MCTNoAncillaRelativePhase

absolute_error_tol = 1e-3
relative_error_tol = 1e-3
usim = Aer.get_backend("unitary_simulator")


@pytest.mark.parametrize("implementation", [MCTNoAncilla])
@pytest.mark.parametrize("controls_no", [2, 3, 4])
def test_generate_circuit_no_ancilla(implementation, controls_no):
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


@pytest.mark.parametrize("implementation", [MCTNoAncillaRelativePhase])
@pytest.mark.parametrize(
    "controls_no", [2, 3, pytest.param(4, marks=pytest.mark.xfail, id="accepted-fail-example")]
)
def test_generate_circuit_no_ancilla_relative_phase(implementation, controls_no):
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
