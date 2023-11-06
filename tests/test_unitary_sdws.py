from typing import Dict, List

import numpy as np

from tests.test_unitary_base import BaseTestUnitary


class TestStrictDirtyWastingSeparable(BaseTestUnitary):
    _controls_no_list: List[int] = [0, 1]

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

    def _take_matrix(self, controls_no: int) -> np.ndarray:
        U = self._ref_matrix(controls_no)

        V = np.array([[1 / np.sqrt(2), 1 / np.sqrt(2)], [1 / np.sqrt(2), -1 * 1 / np.sqrt(2)]])

        U = np.kron(V, U)
        if controls_no == 0:
            return U

        return np.exp(1.0j) * U
