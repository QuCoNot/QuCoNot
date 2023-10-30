from abc import ABC, abstractmethod
from typing import Dict, Type

import numpy as np
from qiskit.quantum_info.operators import Operator

from quconot.implementations.mct_base import MCTBase
from quconot.verifications.functions_testing import (
    verify_circuit_relative_clean_non_wasting,
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
from tests.utils import load_matrix


class BaseTest(ABC):
    _matrix_dict: Dict[int, np.ndarray] = {}
    _ref_matrices: Dict[int, np.ndarray] = {}
    _controls_no_list: list[int] = []

    _expected_classes: Dict[str, bool] = {}

    @abstractmethod
    def _take_matrix(self, controls_no: int) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def _ref_matrix(self, controls_no: int) -> np.ndarray:
        raise NotImplementedError

    def test_circuit_clean_auxiliary(self):
        for controls_no in self._controls_no_list:
            ref_matrix = self._ref_matrix(controls_no)
            unitary_matrix = self._take_matrix(controls_no)
            res, msg = verify_circuit_strict_clean_non_wasting(unitary_matrix, ref_matrix)
            assert res == self._expected_classes["SCNW"], msg

    def test_circuit_clean_relative_auxiliary(self):
        for controls_no in self._controls_no_list:
            ref_matrix = self._ref_matrix(controls_no)
            unitary_matrix = self._take_matrix(controls_no)
            res, msg = verify_circuit_relative_clean_non_wasting(unitary_matrix, ref_matrix)
            assert res == self._expected_classes["RCNW"], msg

    def test_circuit_dirty_auxiliary(self):
        for controls_no in self._controls_no_list:
            ref_matrix = self._ref_matrix(controls_no)
            unitary_matrix = self._take_matrix(controls_no)
            res, msg = verify_circuit_strict_dirty_non_wasting(unitary_matrix, ref_matrix)
            assert res == self._expected_classes["SDNW"], msg

    def test_circuit_dirty_relative_auxiliary(self):
        for controls_no in self._controls_no_list:
            ref_matrix = self._ref_matrix(controls_no)
            unitary_matrix = self._take_matrix(controls_no)
            res, msg = verify_circuit_relative_dirty_non_wasting(unitary_matrix, ref_matrix)
            assert res == self._expected_classes["RDNW"], msg

    def test_circuit_clean_wasted_entangled_auxiliary(self):
        for controls_no in self._controls_no_list:
            ref_matrix = self._ref_matrix(controls_no)
            unitary_matrix = self._take_matrix(controls_no)
            res, msg = verify_circuit_strict_clean_wasting_entangled(unitary_matrix, ref_matrix)
            assert res == self._expected_classes["SCWE"], msg

    def test_circuit_clean_wasted_separable_auxiliary(self):
        for controls_no in self._controls_no_list:
            ref_matrix = self._ref_matrix(controls_no)
            unitary_matrix = self._take_matrix(controls_no)
            res, msg = verify_circuit_strict_clean_wasting_separable(unitary_matrix, ref_matrix)
            assert res == self._expected_classes["SCWS"], msg

    def test_circuit_clean_wasted_relative_separable_auxiliary(self):
        for controls_no in self._controls_no_list:
            ref_matrix = self._ref_matrix(controls_no)
            unitary_matrix = self._take_matrix(controls_no)
            res, msg = verify_circuit_relative_clean_wasting_separable(unitary_matrix, ref_matrix)
            assert res == self._expected_classes["RCWS"], msg

    def test_circuit_dirty_wasted_entangled_auxiliary(self):
        for controls_no in self._controls_no_list:
            ref_matrix = self._ref_matrix(controls_no)
            unitary_matrix = self._take_matrix(controls_no)
            res, msg = verify_circuit_strict_dirty_wasting_entangled(unitary_matrix, ref_matrix)
            assert res == self._expected_classes["SDWE"], msg

    def test_circuit_dirty_wasted_separable_auxiliary(self):
        for controls_no in self._controls_no_list:
            ref_matrix = self._ref_matrix(controls_no)
            unitary_matrix = self._take_matrix(controls_no)
            res, msg = verify_circuit_strict_dirty_wasting_separable(unitary_matrix, ref_matrix)
            assert res == self._expected_classes["SDWS"], msg

    def test_circuit_dirty_wasted_relative_separable_auxiliary(self):
        for controls_no in self._controls_no_list:
            ref_matrix = self._ref_matrix(controls_no)
            unitary_matrix = self._take_matrix(controls_no)
            res, msg = verify_circuit_relative_dirty_wasting_separable(unitary_matrix, ref_matrix)
            assert res == self._expected_classes["RDWS"], msg

    def test_dependencies(self):
        rd = self._expected_classes

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
            assert rd["SCWE"]

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
            assert rd["SCWE"]


class BaseTestMCT(BaseTest):
    @property
    @abstractmethod
    def _get_class_name(self) -> Type[MCTBase]:
        raise NotImplementedError

    def _take_matrix(self, controls_no: int):
        if controls_no in self._matrix_dict:
            return self._matrix_dict[controls_no]

        circ = self._get_class_name(controls_no).generate_circuit()
        unitary_matrix = Operator(circ).data
        self._matrix_dict[controls_no] = unitary_matrix

        return self._matrix_dict[controls_no]

    def _ref_matrix(self, controls_no: int):
        if controls_no in self._ref_matrices:
            return self._ref_matrices[controls_no]

        self._ref_matrices[controls_no] = load_matrix("noauxiliary", controls_no)

        return self._ref_matrices[controls_no]
