import numpy as np
import pytest
from functions import identity_matrix, ket_0_matrix, load_matrix
from qiskit import Aer

from qumcat.implementations.mct_vchain import MCTVChain

absolute_error_tol = 1e-8
relative_error_tol = 1e-8
usim = Aer.get_backend("unitary_simulator")


@pytest.mark.parametrize("implementation", [MCTVChain])
@pytest.mark.parametrize("controls_no", [4, 5])
def test_generate_circuit_clean_wasted_ancilla(implementation, controls_no):
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
