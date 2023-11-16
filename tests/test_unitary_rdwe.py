from typing import Dict, List

import numpy as np
from qiskit.quantum_info import random_unitary

from tests.test_unitary_base import BaseTestUnitary


class TestRelativeDirtyWastingEntangled(BaseTestUnitary):
    _controls_no_list: List[int] = [0, 1]

    _expected_classes: Dict[str, bool] = {
        "SCNW": False,
        "RCNW": False,
        "SDNW": False,
        "RDNW": False,
        "SCWE": True,
        "SCWS": False,
        "RCWS": False,
        "SDWE": True,
        "SDWS": False,
        "RDWS": False,
    }

    def _take_matrix(self, controls_no: int) -> np.ndarray:
        U = self._ref_matrix(controls_no)
        W = np.eye(3)

        matrix_size = len(W)
        Wi = []

        for i in range(0, matrix_size):
            random_matrix = np.array(random_unitary(matrix_size))

            while np.allclose(random_matrix, np.eye(matrix_size)):
                random_matrix = np.array(random_unitary(matrix_size))

            Wi.append(random_matrix)

        result_terms = []

        basis_states = [np.zeros(matrix_size) for _ in range(matrix_size)]
        for i in range(matrix_size):
            basis_states[i][i] = 1

        for i, basis_state in enumerate(basis_states):
            term = np.kron(Wi[i], np.outer(basis_state, basis_state))
            result_terms.append(term)

        result = sum(result_terms)
        if controls_no == 0:
            return np.kron(W, U) @ result

        D = np.diag(np.exp(1.0j * np.arange(3)))
        return np.kron(W, U @ D) @ result
