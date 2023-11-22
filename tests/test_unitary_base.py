import numpy as np
from qiskit.quantum_info import random_unitary

from tests.test_mct_base import BaseTest


class BaseTestUnitary(BaseTest):
    def _ref_matrix(self, controls_no: int) -> np.ndarray:
        return np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])

    def _random_unitary_clean(self, matrix_size: int) -> np.ndarray:
        matrix_list = [np.eye(matrix_size)]

        for i in range(1, matrix_size):
            random_matrix = np.array(random_unitary(matrix_size))

            while np.allclose(random_matrix, np.eye(matrix_size)):
                random_matrix = np.array(random_unitary(matrix_size))

            matrix_list.append(random_matrix)

        result_terms = []

        basis_states = [np.zeros(matrix_size) for _ in range(matrix_size)]
        for i in range(matrix_size):
            basis_states[i][i] = 1

        for i, basis_state in enumerate(basis_states):
            term = np.kron(np.outer(basis_state, basis_state), matrix_list[i])
            result_terms.append(term)

        return sum(result_terms)

    def _random_unitary_wasted(self, matrix_size: int) -> np.ndarray:
        matrix_list = []

        for i in range(0, matrix_size):
            random_matrix = np.array(random_unitary(matrix_size))

            while np.allclose(random_matrix, np.eye(matrix_size)):
                random_matrix = np.array(random_unitary(matrix_size))

            matrix_list.append(random_matrix)

        result_terms = []

        basis_states = [np.zeros(matrix_size) for _ in range(matrix_size)]
        for i in range(matrix_size):
            basis_states[i][i] = 1

        for i, basis_state in enumerate(basis_states):
            term = np.kron(matrix_list[i], np.outer(basis_state, basis_state))
            result_terms.append(term)

        return sum(result_terms)
