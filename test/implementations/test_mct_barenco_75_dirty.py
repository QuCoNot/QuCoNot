from typing import Dict

import numpy as np

from qumcat.implementations.mct_barenco_75_dirty import MCTBarenco75Dirty

from .functions import usim  # ket_0_matrix,
from .functions_testing import (
    generate_circuit_clean_ancilla,
    generate_circuit_clean_relative_ancilla,
)

implementation = MCTBarenco75Dirty
controls_no_list = [5]


class Test:
    _matrix_dict: Dict[np.array, int] = {}
    _ancilla_dict: Dict[int, int] = {}

    def _take_matrix(self, controls_no: int):
        if controls_no in self._matrix_dict:
            return self._matrix_dict[controls_no]

        circ = implementation(controls_no).generate_circuit()
        unitary_matrix = np.array(np.absolute(usim.run(circ).result().get_unitary()))
        self._matrix_dict[controls_no] = unitary_matrix

        return self._matrix_dict[controls_no]

    def _take_ancillas_no(self, controls_no: int):
        if controls_no in self._ancilla_dict:
            return self._ancilla_dict[controls_no]

        mct = implementation(controls_no)
        self._ancilla_dict[controls_no] = mct.num_ancilla_qubits()

        return self._matrix_dict[controls_no]

    def test_circuit_clean_ancilla(self):
        for controls_no in controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            ancillas_no = self._take_ancillas_no(controls_no)

            generate_circuit_clean_ancilla(unitary_matrix, controls_no, ancillas_no)

    def test_circuit_clean_relative_ancilla(self):
        for controls_no in controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            ancillas_no = self._take_ancillas_no(controls_no)

            generate_circuit_clean_relative_ancilla(unitary_matrix, controls_no, ancillas_no)


if __name__ == "__main__":
    mct = Test()
    mct.test_circuit_clean_ancilla()
    mct.test_circuit_clean_relative_ancilla()
