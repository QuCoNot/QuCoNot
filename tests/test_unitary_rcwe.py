from typing import Dict, List

import numpy as np
from qiskit.quantum_info import random_unitary

from tests.test_unitary_base import BaseTestUnitary


class TestRelativeCleanWastingEntangled(BaseTestUnitary):
    _controls_no_list: List[int] = [0]

    _expected_classes: Dict[str, bool] = {
        "SCNW": False,
        "RCNW": False,
        "SDNW": False,
        "RDNW": False,
        "SCWE": True,
        "SCWS": False,
        "RCWS": False,
        "SDWE": False,
        "SDWS": False,
        "RDWS": False,
    }

    def _take_matrix(self, controls_no: int) -> np.ndarray:
        U = self._ref_matrix(controls_no)
        W = np.eye(3)

        matrix_size = len(W)
        Wi = []
        Vi = [np.eye(matrix_size)]

        for i in range(0, matrix_size):
            random_matrix = np.array(random_unitary(matrix_size))

            while np.allclose(random_matrix, np.eye(matrix_size)):
                random_matrix = np.array(random_unitary(matrix_size))

            Wi.append(random_matrix)
            if i > 0:
                Vi.append(random_matrix)

        result_terms_w = []
        result_terms_v = []

        basis_states = [np.zeros(matrix_size) for _ in range(matrix_size)]
        for i in range(matrix_size):
            basis_states[i][i] = 1

        for i, basis_state in enumerate(basis_states):
            term_w = np.kron(Wi[i], np.outer(basis_state, basis_state))
            result_terms_w.append(term_w)

            term_v = np.kron(np.outer(basis_state, basis_state), Vi[i])
            result_terms_v.append(term_v)

        result_w = sum(result_terms_w)
        result_v = sum(result_terms_v)
        if controls_no == 0:
            return result_w @ np.kron(W, U) @ result_v

        D = np.diag(np.exp(1.0j * np.arange(3)))
        return result_w @ np.kron(W, U @ D) @ result_v
