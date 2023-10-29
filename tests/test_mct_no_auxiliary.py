from typing import Dict

import numpy as np
import pytest
from qiskit.quantum_info.operators import Operator

from quconot.implementations.mct_no_auxiliary import MCTNoAuxiliary
from tests.test_mct_base import BaseTestMCT


@pytest.mark.xfail
class TestMCTNoAuxiliary(BaseTestMCT):
    _matrix_dict: Dict[int, np.array] = {}
    _controls_no_list = [5]

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

    def _take_matrix(self, controls_no: int):
        if controls_no in self._matrix_dict:
            return self._matrix_dict[controls_no]

        circ = MCTNoAuxiliary(controls_no).generate_circuit()
        unitary_matrix = Operator(circ).data
        self._matrix_dict[controls_no] = unitary_matrix

        return self._matrix_dict[controls_no]

    def test_init(self):
        with pytest.raises(
            ValueError, match="Number of controls must be >= 2 for this implementation"
        ):
            MCTNoAuxiliary(1)

        try:
            MCTNoAuxiliary(3)
        except Exception:
            assert False, "object MCTBarenco74Dirty(3) was not created, but it should be"
