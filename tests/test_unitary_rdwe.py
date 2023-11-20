from typing import Dict, List

import numpy as np

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

        if controls_no == 0:
            return self._random_unitary_wasted(3) @ np.kron(W, U)

        D = np.diag(np.exp(1.0j * np.arange(3)))
        return self._random_unitary_wasted(3) @ np.kron(W, U @ D)
