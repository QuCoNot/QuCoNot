from typing import Dict, List

import numpy as np

from tests.test_unitary_base import BaseTestUnitary


class TestRelativeDirtyWastingSeparable(BaseTestUnitary):
    _controls_no_list: List[int] = [0]

    _expected_classes: Dict[str, bool] = {
        "SCNW": False,
        "RCNW": False,
        "SDNW": False,
        "RDNW": False,
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
        V = np.array(
            [[1 / np.sqrt(2), 1 / np.sqrt(2)], [1 / np.sqrt(2), -1 / np.sqrt(2)]]
        )

        U = np.kron(V, U @ D)

        return U
