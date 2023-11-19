from typing import Dict, List

import numpy as np

from tests.test_unitary_base import BaseTestUnitary


class TestStrictCleanNonWasting(BaseTestUnitary):
    _controls_no_list: List[int] = [0, 1]

    _expected_classes: Dict[str, bool] = {
        "SCNW": True,
        "RCNW": True,
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
        V = np.eye(3)

        if controls_no == 0:
            return np.kron(V, U) @ self._random_unitary_clean(3)
        return np.exp(1.0j) * np.kron(V, U) @ self._random_unitary_clean(3)
