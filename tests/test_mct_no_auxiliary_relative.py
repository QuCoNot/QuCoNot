from typing import Dict

import numpy as np
import pytest
from qiskit.quantum_info.operators import Operator

from quconot.implementations.mct_no_auxiliary_relative import MCTNoAuxiliaryRelative

from tests.test_mct_base import BaseTestMCT


@pytest.mark.xfail
class TestMCTNoAuxiliaryRelative(BaseTestMCT):
    _matrix_dict: Dict[np.array, int] = {}
    _reverse_matrix_dict: Dict[np.array, int] = {}
    _controls_no_list = [2, 3]

    _expected_classes: Dict[str, bool] = {
        "SCNW": False,
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

        circ = MCTNoAuxiliaryRelative(controls_no).generate_circuit()
        unitary_matrix = Operator(circ).data
        self._matrix_dict[controls_no] = unitary_matrix

        reverse_unitary_matrix = Operator(circ.reverse_bits()).data
        self._reverse_matrix_dict[controls_no] = reverse_unitary_matrix

        if reverse is True:
            return self._reverse_matrix_dict[controls_no]
        else:
            return self._matrix_dict[controls_no]

    def _take_auxiliaries_no(self, controls_no: int):
        return 0

    def test_init(self):
        with pytest.raises(
            ValueError, match="Number of controls must be 2 or 3 for this implementation"
        ):
            MCTNoAuxiliaryRelative(1)

        try:
            MCTNoAuxiliaryRelative(2)
        except Exception:
            assert False, "object MCTNoAuxiliaryRelative(2) was not created, but it should be"
