from typing import Dict, List

import numpy as np

from tests.test_unitary_base import BaseTestUnitary


class TestRelativeDirtyNonWasting(BaseTestUnitary):
    _controls_no_list: List[int] = [0]

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

    def _take_matrix(self, controls_no: int) -> np.ndarray:
        U = self._ref_matrix(controls_no)

        D = np.diag(np.exp(1.0j * np.arange(3)))

        U = np.kron(np.eye(5), U @ D)

        return U
