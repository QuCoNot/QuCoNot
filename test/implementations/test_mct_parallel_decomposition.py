from typing import Dict

import numpy as np
from qiskit.quantum_info.operators import Operator

from quconot.implementations.mct_parallel_decomposition import MCTParallelDecomposition

from .functions_testing import (
    verify_circuit_clean_auxiliary,
    verify_circuit_clean_relative_auxiliary,
)


class TestMCTParallelDecomposition:
    _matrix_dict: Dict[np.array, int] = {}
    _auxiliary_dict: Dict[int, int] = {}
    _controls_no_list = [5]

    def _take_matrix(self, controls_no: int):
        if controls_no in self._matrix_dict:
            return self._matrix_dict[controls_no]

        circ = MCTParallelDecomposition(controls_no).generate_circuit()
        unitary_matrix = Operator(circ).data
        self._matrix_dict[controls_no] = unitary_matrix

        return self._matrix_dict[controls_no]

    def _take_auxiliaries_no(self, controls_no: int):
        if controls_no in self._auxiliary_dict:
            return self._auxiliary_dict[controls_no]

        mct = MCTParallelDecomposition(controls_no)
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
