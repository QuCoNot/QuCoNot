from typing import Dict, List

import numpy as np
from qiskit.quantum_info import random_unitary

from tests.test_unitary_base import BaseTestUnitary


class TestRelativeCleanWastingSeparable(BaseTestUnitary):
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
        V = np.array(random_unitary(3))

        matrix_size = len(V)
        Vi = [np.eye(matrix_size)]

        for i in range(1, matrix_size):
            random_matrix = np.array(random_unitary(3))

            while np.allclose(random_matrix, np.eye(matrix_size)):
                random_matrix = np.array(random_unitary(3))

            Vi.append(random_matrix)

        result_terms = []

        basis_states = [np.zeros(matrix_size) for _ in range(matrix_size)]
        for i in range(matrix_size):
            basis_states[i][i] = 1

        for i, basis_state in enumerate(basis_states):
            term = np.kron(np.outer(basis_state, basis_state), Vi[i])
            result_terms.append(term)

        result = sum(result_terms)
        return np.kron(V, U) @ result
