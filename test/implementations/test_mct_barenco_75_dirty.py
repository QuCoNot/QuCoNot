from typing import Dict

import numpy as np
from qiskit.quantum_info.operators import Operator

from quconot.implementations.mct_barenco_75_dirty import MCTBarenco75Dirty

from .functions_testing import (
    verify_circuit_clean_auxiliary,
    verify_circuit_clean_relative_auxiliary,
    verify_circuit_dirty_wasted_entangled_auxiliary,
    verify_circuit_dirty_wasted_separable_auxiliary,
)


class TestMCTBarenco75Dirty:
    _matrix_dict: Dict[np.array, int] = {}
    _reverse_matrix_dict: Dict[np.array, int] = {}
    _auxiliary_dict: Dict[int, int] = {}
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

    def _take_auxiliaries_no(self, controls_no: int):
        if controls_no in self._auxiliary_dict:
            return self._auxiliary_dict[controls_no]

        mct = MCTBarenco75Dirty(controls_no)
        self._auxiliary_dict[controls_no] = mct.num_auxiliary_qubits()

        return self._auxiliary_dict[controls_no]

    def test_circuit_clean_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_clean_auxiliary(unitary_matrix, controls_no, auxiliaries_no)

            assert res, msg

    def test_circuit_clean_relative_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_clean_relative_auxiliary(
                unitary_matrix, controls_no, auxiliaries_no
            )

            assert res, msg

    def test_circuit_dirty_wasted_entangled_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_dirty_wasted_entangled_auxiliary(
                unitary_matrix, controls_no, auxiliaries_no
            )

            assert res, msg

    def test_circuit_dirty_wasted_entangled_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no, True)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_dirty_wasted_entangled_auxiliary(
                unitary_matrix, controls_no, auxiliaries_no
            )

            assert res, msg

    def test_circuit_dirty_wasted_separable_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no, True)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_dirty_wasted_separable_auxiliary(
                unitary_matrix, controls_no, auxiliaries_no
            )

            assert res, msg
