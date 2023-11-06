from typing import Dict, List

import numpy as np

from tests.test_unitary_base import BaseTestUnitary


class TestStrictDirtyNonWasting(BaseTestUnitary):
    _controls_no_list: List[int] = [0, 1]

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

    def _take_matrix(self, controls_no: int) -> np.ndarray:
        U = self._ref_matrix(controls_no)
        # U = np.kron(U, np.eye(5))
        U = np.kron(np.eye(5), U)
        if controls_no == 0:
            return U
        return np.exp(1.0j) * U
