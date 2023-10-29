from typing import Dict

import numpy as np
import pytest
from qiskit.quantum_info.operators import Operator

from quconot.implementations.mct_barenco_75_dirty import MCTBarenco75Dirty
from tests.test_mct_base import BaseTestMCT


@pytest.mark.xfail
class TestMCTBarenco75Dirty(BaseTestMCT):
    _matrix_dict: Dict[int, np.array] = {}
    _reverse_matrix_dict: Dict[np.array, int] = {}
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

    def _take_matrix(self, controls_no: int, reverse: bool = False):
        if reverse is True:
            if controls_no in self._matrix_dict:
                return self._reverse_matrix_dict[controls_no]
        else:
            if controls_no in self._matrix_dict:
                return self._matrix_dict[controls_no]

        circ = MCTBarenco75Dirty(controls_no).generate_circuit()
        unitary_matrix = Operator(circ).data
        self._matrix_dict[controls_no] = unitary_matrix

        reverse_unitary_matrix = Operator(circ.reverse_bits()).data
        self._reverse_matrix_dict[controls_no] = reverse_unitary_matrix

        if reverse is True:
            return self._reverse_matrix_dict[controls_no]
        else:
            return self._matrix_dict[controls_no]

    def test_init(self):
        with pytest.raises(
            ValueError, match="Number of controls must be >= 2 for this implementation"
        ):
            MCTBarenco75Dirty(1)

        try:
            MCTBarenco75Dirty(2)
        except Exception:
            assert False, "object MCTBarenco75Dirty(2) was not created, but it should be"
