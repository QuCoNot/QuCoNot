from typing import Dict, List

import numpy as np

from tests.test_unitary_base import BaseTestUnitary


class TestStrictCleanWastingSeparable(BaseTestUnitary):
    _controls_no_list: List[int] = [0]

    _expected_classes: Dict[str, bool] = {
        "SCNW": False,
        "RCNW": False,
        "SDNW": False,
        "RDNW": False,
        "SCWE": True,
        "SCWS": True,
        "RCWS": True,
        "SDWE": False,
        "SDWS": False,
        "RDWS": False,
    }

    def _take_matrix(self, controls_no: int) -> np.ndarray:
        U = self._ref_matrix(controls_no)
        V = np.array([[1 / np.sqrt(2), 1 / np.sqrt(2)], [1 / np.sqrt(2), -1 * 1 / np.sqrt(2)]])

        matrix_size = 3
        Vi = [np.eye(matrix_size)]

        for i in range(1, matrix_size):
            random_matrix = np.random.rand(matrix_size, matrix_size)

            while np.allclose(random_matrix, np.eye(matrix_size)):
                random_matrix = np.random.rand(matrix_size, matrix_size)

            Vi.append(random_matrix)

        result_terms = []

        basis_states = [np.zeros(matrix_size) for _ in range(matrix_size - 1)]
        for i in range(matrix_size - 1):
            basis_states[i][i] = 1

        for i, basis_state in enumerate(basis_states):
            term = np.kron(Vi[i], np.outer(basis_state, basis_state))
            result_terms.append(term)

        result = sum(result_terms)

        return result @ np.kron(U, V)
