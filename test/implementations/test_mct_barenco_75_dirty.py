from typing import Dict

import numpy as np
import pytest
from functions_testing import verify_circuit_no_auxiliary, verify_circuit_no_auxiliary_relative
from qiskit.quantum_info.operators import Operator

from quconot.implementations.mct_barenco_75_dirty import MCTBarenco75Dirty


class TestMCTBarenco75Dirty:
    _matrix_dict: Dict[np.array, int] = {}
    _reverse_matrix_dict: Dict[np.array, int] = {}
    _controls_no_list = [5]

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

        assert MCTBarenco75Dirty(2)

    def test_circuit_no_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = 0

            res, msg = verify_circuit_no_auxiliary(unitary_matrix, controls_no, auxiliaries_no)

            assert res, msg

    def test_circuit_no_auxiliary_relative(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = 0

            res, msg = verify_circuit_no_auxiliary_relative(
                unitary_matrix, controls_no, auxiliaries_no
            )

            assert res, msg
