from typing import Dict, List

import numpy as np

from tests.test_unitary_base import BaseTestUnitary


class TestRelativeCleanNonWasting(BaseTestUnitary):
    _controls_no_list: List[int] = [0]

    _expected_classes: Dict[str, bool] = {
        "SCNW": False,
        "RCNW": True,
        "SDNW": False,
        "RDNW": False,
        "SCWE": True,
        "SCWS": False,
        "RCWS": True,
        "SDWE": False,
        "SDWS": False,
        "RDWS": False,
    }

    def _take_matrix(self, controls_no: int) -> np.ndarray:
        U = self._ref_matrix(controls_no)
        V = np.eye(3)
        D = np.diag(np.exp(1.0j * np.arange(3)))

        return np.kron(V, U @ D) @ self._random_unitary_clean(3)
