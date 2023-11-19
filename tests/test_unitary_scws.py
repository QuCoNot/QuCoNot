from typing import Dict, List

import numpy as np
from qiskit.quantum_info import random_unitary

from tests.test_unitary_base import BaseTestUnitary


class TestStrictCleanWastingSeparable(BaseTestUnitary):
    _controls_no_list: List[int] = [0]

    _expected_classes: Dict[str, bool] = {
        "SCNW": False,
        "RCNW": False,
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
        V = np.array(random_unitary(3))
        return np.kron(V, U) @ self._random_unitary_clean(3)
