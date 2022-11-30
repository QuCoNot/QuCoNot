from typing import Dict

import numpy as np
from functions_testing import verify_circuit_no_auxiliary_relative
from qiskit.quantum_info.operators import Operator

from quconot.implementations.mct_no_auxiliary_relative_phase import MCTNoAuxiliaryRelativePhase


class TestMCTNoAuxiliaryRelativePhase:
    _matrix_dict: Dict[np.array, int] = {}
    _controls_no_list = [2, 3]

    def _take_matrix(self, controls_no: int):
        if controls_no in self._matrix_dict:
            return self._matrix_dict[controls_no]

        circ = MCTNoAuxiliaryRelativePhase(controls_no).generate_circuit()
        unitary_matrix = Operator(circ).data
        self._matrix_dict[controls_no] = unitary_matrix

        return self._matrix_dict[controls_no]

    def test_circuit_no_auxiliary_relative(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = 0

            res, msg = verify_circuit_no_auxiliary_relative(
                unitary_matrix, controls_no, auxiliaries_no
            )

            assert res, msg
