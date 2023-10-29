from typing import Dict

import numpy as np
import pytest
from qiskit.quantum_info.operators import Operator

from quconot.implementations.mct_barenco_74_dirty import MCTBarenco74Dirty
from tests.test_mct_base import BaseTestMCT


class TestMCTBarenco74Dirty(BaseTestMCT):
    _matrix_dict: Dict[np.array, int] = {}
    _reverse_matrix_dict: Dict[np.array, int] = {}
    _auxiliary_dict: Dict[int, int] = {}
    _controls_no_list = [5]
    _result_dict: Dict[str, bool] = {}

    _expected_classes: Dict[str, bool] = {
        "SCNW": False,
        "RCNW": True,
        "SDNW": False,
        "RDNW": True,
        "SCWE": True,
        "SCWS": False,
        "RCWS": True,
        "SDWE": True,
        "SDWS": False,
        "RDWS": True,
    }

    def _take_matrix(self, controls_no: int, reverse: bool = False):
        if reverse is True:
            if controls_no in self._matrix_dict:
                return self._reverse_matrix_dict[controls_no]
        else:
            if controls_no in self._matrix_dict:
                return self._matrix_dict[controls_no]

        circ = MCTBarenco74Dirty(controls_no).generate_circuit()
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
            ValueError, match="Number of controls must be >= 5 for this implementation"
        ):
            MCTBarenco74Dirty(2)

        try:
            MCTBarenco74Dirty(5)
        except Exception:
            assert False, "object MCTBarenco74Dirty(5) was not created, but it should be"
