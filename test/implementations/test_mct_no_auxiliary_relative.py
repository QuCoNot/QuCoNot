from typing import Dict

import numpy as np
import pytest
from functions_testing import verify_circuit_no_auxiliary, verify_circuit_no_auxiliary_relative
from qiskit.quantum_info.operators import Operator

from quconot.implementations.mct_no_auxiliary_relative import MCTNoAuxiliaryRelative


class TestMCTNoAuxiliaryRelative:
    _matrix_dict: Dict[np.array, int] = {}
    _reverse_matrix_dict: Dict[np.array, int] = {}
    _controls_no_list = [2, 3]

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

    def test_init(self):
        with pytest.raises(Exception) as e_info:
            MCTNoAuxiliaryRelative(1)

        assert e_info.value.args[0] == "Number of controls must be 2 or 3 for this implementation"

        assert MCTNoAuxiliaryRelative(2)

    def test_circuit_no_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = 0

            res, msg = verify_circuit_no_auxiliary(unitary_matrix, controls_no, auxiliaries_no)

            assert not res, msg

    def test_circuit_no_auxiliary_relative(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = 0

            res, msg = verify_circuit_no_auxiliary_relative(
                unitary_matrix, controls_no, auxiliaries_no
            )

            assert res, msg
