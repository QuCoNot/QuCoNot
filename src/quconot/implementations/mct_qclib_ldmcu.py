# Quconot/quconot/implementations/mct_qclib_ldmcu.py
#
# Authors:
#  - Adam Glos
#
# Apply the implementation from https://arxiv.org/abs/2203.11882

from copy import deepcopy
from typing import List

import numpy as np
from qclib.gates.ldmcu import Ldmcu
from qiskit import QuantumCircuit

from .mct_base import MCTBase


class MCTQclibLdmcu(MCTBase):
    def __init__(self, controls_no: int, **kwargs) -> None:
        if controls_no < 2:
            raise ValueError("Number of controls must be >= 2 for this implementation")
        self._n = controls_no
        self._circuit: QuantumCircuit = None

    @classmethod
    def verify_mct_cases(
        self,
        controls_no: int,
        max_auxiliary: int,
        relative_phase: bool = False,
        clean_acilla: bool = True,
        wasted_auxiliary: bool = False,
        separable_wasted_auxiliary: bool = False,
    ) -> List["MCTBase"]:
        """Generate all possible MCT implementation satisfying the requirements

        relative_phase: true / false (D)
        clean_auxiliary: true (D) / false
        wasted_auxiliary: true / false (D)
        separable_wasted_auxiliary: true / false (D), requires wasted_auxiliary set to True

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """
        return [MCTQclibLdmcu(controls_no)]

    def generate_circuit(self) -> QuantumCircuit:
        """Return a QuantumCircuit implementation

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """
        qc = QuantumCircuit(self._n + 1)
        qc.append(Ldmcu(np.array([[0, 1], [1, 0]]), self._n), list(range(self._n + 1)))
        self._circuit = qc
        return deepcopy(self._circuit)

    def num_auxiliary_qubits(self):
        """Return number of auxiliary qubits

        :return: number of auxiliary qubits
        :rtype: int
        """
        return 0
