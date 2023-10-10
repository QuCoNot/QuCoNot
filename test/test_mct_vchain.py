from typing import Dict

import numpy as np
import pytest
from qiskit.quantum_info.operators import Operator

from quconot.implementations.mct_vchain import MCTVChain
from quconot.verifications.functions_testing import (
    verify_circuit_relative_clean_non_wasting,
    verify_circuit_relative_clean_wasting_entangled,
    verify_circuit_relative_clean_wasting_separable,
    verify_circuit_relative_dirty_non_wasting,
    verify_circuit_relative_dirty_wasting_separable,
    verify_circuit_strict_clean_non_wasting,
    verify_circuit_strict_clean_wasting_entangled,
    verify_circuit_strict_clean_wasting_separable,
    verify_circuit_strict_dirty_non_wasting,
    verify_circuit_strict_dirty_wasting_entangled,
    verify_circuit_strict_dirty_wasting_separable,
)


class TestMCTVChain:
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

        circ = MCTVChain(controls_no).generate_circuit()
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

        mct = MCTVChain(controls_no)
        self._auxiliary_dict[controls_no] = mct.num_auxiliary_qubits()

        return self._auxiliary_dict[controls_no]

    def test_init(self):
        with pytest.raises(
            ValueError, match="Number of controls must be >= 2 for this implementation"
        ):
            MCTVChain(1)

        try:
            MCTVChain(5)
        except Exception:
            assert False, "object MCTVChain(5) was not created, but it should be"

    def test_circuit_clean_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_strict_clean_non_wasting(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["SCNW"] = res

            assert res, msg

    def test_circuit_clean_relative_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_relative_clean_non_wasting(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["RCNW"] = res

            assert res, msg

    def test_circuit_dirty_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_strict_dirty_non_wasting(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["SDNW"] = res

            assert not res, msg

    def test_circuit_dirty_relative_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_relative_dirty_non_wasting(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["RDNW"] = res

            assert not res, msg

    def test_circuit_clean_wasted_entangled_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_strict_clean_wasting_entangled(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["SCWE"] = res

            assert res, msg

    def test_circuit_clean_wasted_relative_entangled_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_relative_clean_wasting_entangled(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["RCWE"] = res

            assert res, msg

    def test_circuit_clean_wasted_separable_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_strict_clean_wasting_separable(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["SCWS"] = res

            assert res, msg

    def test_circuit_clean_wasted_relative_separable_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_relative_clean_wasting_separable(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["RCWS"] = res

            assert res, msg

    def test_circuit_dirty_wasted_entangled_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no, True)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_strict_dirty_wasting_entangled(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["SDWE"] = res

            assert res, msg

    def test_circuit_dirty_wasted_separable_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no, True)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_strict_dirty_wasting_separable(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["SDWS"] = res

            assert not res, msg

    def test_circuit_dirty_wasted_relative_separable_auxiliary(self):
        for controls_no in self._controls_no_list:
            unitary_matrix = self._take_matrix(controls_no, True)
            auxiliaries_no = self._take_auxiliaries_no(controls_no)

            res, msg = verify_circuit_relative_dirty_wasting_separable(
                unitary_matrix, controls_no, auxiliaries_no
            )

            self._result_dict["RDWS"] = res

            assert not res, msg

    def test_dependencies(self):
        rd = self._result_dict

        if rd["SDNW"]:
            assert rd["SCNW"]
            assert rd["RDNW"]
            assert rd["SDWS"]

        if rd["RDNW"]:
            assert rd["RCNW"]
            assert rd["RDWS"]

        if rd["SDWS"]:
            assert rd["SCWS"]
            assert rd["RDWS"]

        if rd["SDWE"]:
            assert rd["RCWE"]

        if rd["SCNW"]:
            assert rd["RCNW"]
            assert rd["SCWS"]

        if rd["SCWS"]:
            assert rd["RCWS"]

        if rd["RCNW"]:
            assert rd["RCWS"]

        if rd["RDWS"]:
            assert rd["SDWE"]

        if rd["RCWS"]:
            assert rd["RCWE"]
