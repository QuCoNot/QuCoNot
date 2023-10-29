from typing import Dict

import numpy as np
import pytest
from qiskit.quantum_info.operators import Operator

from quconot.implementations.mct_vchain import MCTVChain
from tests.test_mct_base import BaseTestMCT


class TestMCTVChain(BaseTestMCT):
    _matrix_dict: Dict[int, np.array] = {}
    _controls_no_list = [5]
    _result_dict: Dict[str, bool] = {}

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

    def _take_matrix(self, controls_no: int):
        if controls_no in self._matrix_dict:
            return self._matrix_dict[controls_no]

        circ = MCTVChain(controls_no).generate_circuit()
        unitary_matrix = Operator(circ).data
        self._matrix_dict[controls_no] = unitary_matrix

        return self._matrix_dict[controls_no]

    def test_init(self):
        with pytest.raises(
            ValueError, match="Number of controls must be >= 2 for this implementation"
        ):
            MCTVChain(1)

        try:
            MCTVChain(5)
        except Exception:
            assert False, "object MCTVChain(5) was not created, but it should be"
