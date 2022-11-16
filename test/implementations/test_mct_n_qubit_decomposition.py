from typing import Dict

import numpy as np
from .functions import usim
from .functions_testing import (
    generate_circuit_clean_auxiliary,
    generate_circuit_clean_relative_auxiliary,
    generate_circuit_clean_wasted_entangled_auxiliary,
    generate_circuit_clean_wasted_relative_entangled_auxiliary,
    generate_circuit_clean_wasted_relative_separable_auxiliary,
    generate_circuit_clean_wasted_separable_auxiliary,
)

from qumcat.implementations.mct_n_qubit_decomposition import MCTNQubitDecomposition

implementation = MCTNQubitDecomposition
controls_no_list = [5]


class Test:
    _matrix_dict: Dict[np.array, int] = {}
    _auxiliary_dict: Dict[int, int] = {}

    def _take_matrix(self, controls_no: int):
        if controls_no in self._matrix_dict:
            return self._matrix_dict[controls_no]

        circ = implementation(controls_no).generate_circuit()
        unitary_matrix = np.array(np.absolute(usim.run(circ).result().get_unitary()))
        self._matrix_dict[controls_no] = unitary_matrix

        return self._matrix_dict[controls_no]

    def _take_auxiliaries_no(self, controls_no: int):
        if controls_no in self._auxiliary_dict:
            return self._auxiliary_dict[controls_no]

        mct = implementation(controls_no)
        self._auxiliary_dict[controls_no] = mct.num_auxiliary_qubits()

        return self._matrix_dict[controls_no]

    def test_circuit_clean_auxiliary(self):
        for controls_no in controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            generate_circuit_clean_auxiliary(unitary_matrix, controls_no, auxiliaries_no)

    def test_circuit_clean_relative_auxiliary(self):
        for controls_no in controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            generate_circuit_clean_relative_auxiliary(unitary_matrix, controls_no, auxiliaries_no)

    def test_circuit_clean_wasted_entangled_auxiliary(self):
        for controls_no in controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            generate_circuit_clean_wasted_entangled_auxiliary(
                unitary_matrix, controls_no, auxiliaries_no
            )

    def test_circuit_clean_wasted_relative_entangled_auxiliary(self):
        for controls_no in controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            generate_circuit_clean_wasted_relative_entangled_auxiliary(
                unitary_matrix, controls_no, auxiliaries_no
            )

    def test_circuit_clean_wasted_relative_separable_auxiliary(self):
        for controls_no in controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            generate_circuit_clean_wasted_relative_separable_auxiliary(
                unitary_matrix, controls_no, auxiliaries_no
            )

    def test_circuit_clean_wasted_separable_auxiliary(self):
        for controls_no in controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            generate_circuit_clean_wasted_separable_auxiliary(
                unitary_matrix, controls_no, auxiliaries_no
            )


if __name__ == "__main__":
    mct = Test()
    mct.test_circuit_clean_auxiliary()
    mct.test_circuit_clean_relative_auxiliary()
    mct.test_circuit_clean_wasted_entangled_auxiliary()
    mct.test_circuit_clean_wasted_relative_entangled_auxiliary()
    mct.test_circuit_clean_wasted_relative_separable_auxiliary()
    mct.test_circuit_clean_wasted_separable_auxiliary()
