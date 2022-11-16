from typing import Dict

import numpy as np
from functions_testing import generate_circuit_no_ancilla_relative
from qiskit.quantum_info.operators import Operator

from qumcat.implementations.mct_no_ancilla_relative_phase import MCTNoAncillaRelativePhase

implementation = MCTNoAncillaRelativePhase
controls_no_list = [3]


class Test:
    _matrix_dict: Dict[np.array, int] = {}
    _ancilla_dict: Dict[int, int] = {}

    def _take_matrix(self, controls_no: int):
        if controls_no in self._matrix_dict:
            return self._matrix_dict[controls_no]

        circ = implementation(controls_no).generate_circuit()
        unitary_matrix = Operator(circ).data
        self._matrix_dict[controls_no] = unitary_matrix

        return self._matrix_dict[controls_no]

    def _take_ancillas_no(self, controls_no: int):
        if controls_no in self._ancilla_dict:
            return self._ancilla_dict[controls_no]

        mct = implementation(controls_no)
        self._ancilla_dict[controls_no] = mct.num_ancilla_qubits()

        return self._matrix_dict[controls_no]

    def test_circuit_no_ancilla_relative(self):
        for controls_no in controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            ancillas_no = self._take_ancillas_no(controls_no)

            generate_circuit_no_ancilla_relative(unitary_matrix, controls_no, ancillas_no)


if __name__ == "__main__":
    mct = Test()
    mct.test_circuit_no_ancilla_relative()
