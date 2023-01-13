from typing import Dict

import numpy as np
import pytest
from functions_testing import (
    verify_circuit_clean_auxiliary,
    verify_circuit_clean_relative_auxiliary,
    verify_circuit_clean_wasted_entangled_auxiliary,
    verify_circuit_clean_wasted_relative_entangled_auxiliary,
    verify_circuit_clean_wasted_relative_separable_auxiliary,
    verify_circuit_clean_wasted_separable_auxiliary,
    verify_circuit_dirty_auxiliary,
    verify_circuit_dirty_relative_auxiliary,
    verify_circuit_dirty_wasted_entangled_auxiliary,
    verify_circuit_dirty_wasted_relative_separable_auxiliary,
    verify_circuit_dirty_wasted_separable_auxiliary,
    verify_circuit_no_auxiliary,
    verify_circuit_no_auxiliary_relative,
)
from qiskit.quantum_info.operators import Operator

from quconot.implementations.mct_parallel_decomposition import MCTParallelDecomposition


class TestMCTParallelDecomposition:
    _matrix_dict: Dict[np.array, int] = {}
    _reverse_matrix_dict: Dict[np.array, int] = {}
    _auxiliary_dict: Dict[int, int] = {}
    _controls_no_list = [5]
    _result_dict: Dict[str, bool] = {}

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

    def _take_auxiliaries_no(self, controls_no: int):
        if controls_no in self._auxiliary_dict:
            return self._auxiliary_dict[controls_no]

        mct = MCTParallelDecomposition(controls_no)
        self._auxiliary_dict[controls_no] = mct.num_auxiliary_qubits()

        return self._auxiliary_dict[controls_no]

    def test_circuit_no_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_no_auxiliary(unitary_matrix, controls_no, auxiliaries_no)

            self._result_dict["NA"] = res

            assert not res, msg

    def test_circuit_no_auxiliary_relative(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = 0

            res, msg = verify_circuit_no_auxiliary_relative(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["NAR"] = res

            assert not res, msg

    def test_circuit_clean_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_clean_auxiliary(unitary_matrix, controls_no, auxiliaries_no)

            self._result_dict["CNW"] = res

            assert res, msg

    def test_circuit_clean_relative_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_clean_relative_auxiliary(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["CNWR"] = res

            assert res, msg

    def test_circuit_dirty_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_dirty_auxiliary(unitary_matrix, controls_no, auxiliaries_no)

            self._result_dict["DNW"] = res

            assert not res, msg

    def test_circuit_dirty_relative_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_dirty_relative_auxiliary(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["DNWR"] = res

            assert not res, msg

    def test_circuit_clean_wasted_entangled_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_clean_wasted_entangled_auxiliary(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["CWE"] = res

            assert res, msg

    def test_circuit_clean_wasted_relative_entangled_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_clean_wasted_relative_entangled_auxiliary(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["CWRE"] = res

            assert res, msg

    def test_circuit_clean_wasted_separable_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_clean_wasted_separable_auxiliary(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["CWS"] = res

            assert res, msg

    def test_circuit_clean_wasted_relative_separable_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_clean_wasted_relative_separable_auxiliary(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["CWRS"] = res

            assert res, msg

    def test_circuit_dirty_wasted_entangled_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no, True)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_dirty_wasted_entangled_auxiliary(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["DWRE"] = res

            assert not res, msg

    def test_circuit_dirty_wasted_separable_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no, True)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_dirty_wasted_separable_auxiliary(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["DWS"] = res

            assert not res, msg

    def test_circuit_dirty_wasted_relative_separable_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no, True)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_dirty_wasted_relative_separable_auxiliary(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["DWRS"] = res

            assert not res, msg

    def test_dependencies(self):
        rd = self._result_dict

        if rd["DNW"]:
            assert rd["CNW"]
            assert rd["DNWR"]
            assert rd["DWS"]

        if rd["DNWR"]:
            assert rd["CNWR"]
            assert rd["DWRS"]

        if rd["DWS"]:
            assert rd["CWS"]
            assert rd["DWRS"]

        if rd["DWRE"]:
            assert rd["CWRE"]

        if rd["CNW"]:
            assert rd["CNWR"]
            assert rd["CWS"]

        if rd["CWS"]:
            assert rd["CWRS"]

        if rd["CNWR"]:
            assert rd["CWRS"]

        if rd["DWRS"]:
            assert rd["DWRE"]

        if rd["CWRS"]:
            assert rd["CWRE"]
