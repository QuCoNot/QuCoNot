from typing import Dict

import numpy as np
import pytest
from qiskit.quantum_info.operators import Operator

from quconot.implementations.mct_parallel_decomposition import MCTParallelDecomposition
from tests.test_mct_base import BaseTestMCT


class TestMCTParallelDecomposition(BaseTestMCT):
    _matrix_dict: Dict[int, np.array] = {}
    _reverse_matrix_dict: Dict[np.array, int] = {}
    _controls_no_list = [5]
    _result_dict: Dict[str, bool] = {}

    _expected_classes: Dict[str, bool] = {
        "SCNW": True,
        "RCNW": True,
        "SDNW": False,
        "RDNW": False,
        "SCWE": True,
        "SCWS": True,
        "RCWS": True,
        "SDWE": False,
        "SDWS": False,
        "RDWS": False,
    }

    def _take_matrix(self, controls_no: int, reverse: bool = False):
        if reverse is True:
            if controls_no in self._matrix_dict:
                return self._reverse_matrix_dict[controls_no]
        else:
            if controls_no in self._matrix_dict:
                return self._matrix_dict[controls_no]

        circ = MCTParallelDecomposition(controls_no).generate_circuit()
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
            ValueError, match="Number of controls must be >= 3 for this implementation"
        ):
            MCTParallelDecomposition(2)

        try:
            MCTParallelDecomposition(4)
        except Exception:
            assert False, "object MCTParallelDecomposition(4) was not created, but it should be"

    def test_circuit_dirty_wasted_entangled_auxiliary(self):
        return super().test_circuit_dirty_wasted_entangled_auxiliary()
