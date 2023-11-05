from typing import Dict

import numpy as np

from tests.test_unitary_base import BaseTestUnitary


class TestStrictDirtyNonWasting(BaseTestUnitary):
    _expected_classes: Dict[str, bool] = {
        "SCNW": True,
        "RCNW": True,
        "SDNW": True,
        "RDNW": True,
        "SCWE": True,
        "SCWS": True,
        "RCWS": True,
        "SDWE": True,
        "SDWS": True,
        "RDWS": True,
    }

    def _take_matrix(self):
        U = self._ref_matrices()
        # U = np.kron(U, np.eye(5))
        U = np.exp(1.0j) * np.kron(U, np.eye(5))

        return U
