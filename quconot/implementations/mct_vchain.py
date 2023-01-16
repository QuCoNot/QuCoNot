# Quconot/quconot/implementations/mct_vchain.py
#
# Authors:
#  - Handy Kurniawan
#
# Apply the implementation from Qiskit MCT

from copy import deepcopy
from typing import List

from qiskit import QuantumCircuit, transpile

from .mct_base import MCTBase


class MCTVChain(MCTBase):
    def __init__(self, controls_no: int, **kwargs) -> None:
        assert controls_no >= 2
        self._n = controls_no
        self._circuit: QuantumCircuit = None
        pass

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
        separable_wasted_auxiliary: true / false (D)    # requires wasted_auxiliary set to True

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """
        if max_auxiliary < controls_no - 2:
            return []  # if max_auxiliary allowed is to small - no representation given
        else:
            return [MCTVChain(controls_no)]  # only one available

    def generate_circuit(self) -> QuantumCircuit:
        """Return a QuantumCircuit implementation

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """
        qc = QuantumCircuit(2 * self._n - 1)
        qc.mct(
            list(range(self._n)),
            self._n,
            ancilla_qubits=list(range(self._n + 1, 2 * self._n - 1)),
            mode="v-chain",
        )

        # should be done for all implementations
        # TODO: solve issue with reordered qubits
        self._circuit = transpile(qc, basis_gates=["cx", "u3"])
        return deepcopy(self._circuit)

    def num_auxiliary_qubits(self):
        """Return number of auxiliary qubits

        :return: number of auxiliary qubits
        :rtype: int
        """
        return self._n - 2
