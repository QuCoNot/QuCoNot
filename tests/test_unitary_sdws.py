from typing import Dict

import numpy as np

from tests.test_unitary_base import BaseTestUnitary


class TestStrictDirtyWastingSeparable(BaseTestUnitary):
    _expected_classes: Dict[str, bool] = {
        "SCNW": False,
        "RCNW": False,
        "SDNW": False,
        "RDNW": False,
        "SCWE": True,
        "SCWS": True,
        "RCWS": True,
        "SDWE": True,
        "SDWS": True,
        "RDWS": True,
    }

    def _take_matrix(self):
        U = self._ref_matrices()

        V = [[1 / np.sqrt(2), 1 / np.sqrt(2)], [1 / np.sqrt(2), -1 * 1 / np.sqrt(2)]]

        # U = np.kron(U, V)
        U = np.exp(1.0j) * np.kron(U, V)

        return U
