from typing import Dict

import numpy as np

from tests.test_unitary_base import BaseTestUnitary


class TestRelativeDirtyNonWasting(BaseTestUnitary):
    _expected_classes: Dict[str, bool] = {
        "SCNW": False,
        "RCNW": True,
        "SDNW": False,
        "RDNW": True,
        "SCWE": True,
        "SCWS": False,
        "RCWS": True,
        "SDWE": True,
        "SDWS": False,
        "RDWS": True,
    }

    def _take_matrix(self):
        U = self._ref_matrices()

        D = np.diag(np.exp(1.0j * np.range(3)))

        U = np.kron(U @ D, np.eye(5))

        return U
