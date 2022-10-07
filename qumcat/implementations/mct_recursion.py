# Qumcat/qumcat/implementations/mct_recursion.py
#
# Authors:
#  - Handy Kurniawan
#
# Apply the implementation from Qiskit MCT Recursion

from copy import deepcopy
from typing import List

from qiskit import QuantumCircuit, transpile

from .mct_base import MCTBase


class MCTRecursion(MCTBase):
    def __init__(self, controls_no: int, **kwargs) -> None:
        assert controls_no >= 2
        self._n = controls_no
        self._circuit: QuantumCircuit = None
        pass

    @classmethod
    def generate_mct_cases(
        self,
        controls_no: int,
        max_ancilla: int,
        relative_phase: bool = False,
        clean_acilla: bool = True,
        wasted_ancilla: bool = False,
        separable_wasted_ancilla: bool = False,
    ) -> List["MCTBase"]:
        """Generate all possible MCT implementation satisfying the requirements

        relative_phase: true / false (D)
        clean_ancilla: true (D) / false
        wasted_ancilla: true / false (D)
        separable_wasted_ancilla: true / false (D)    # requires wasted_ancilla set to True

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """
        if max_ancilla < controls_no - 2:
            return []  # if max_ancilla allowed is to small - no representation given
        else:
            return [MCTRecursion(controls_no)]  # only one available

    def generate_circuit(self) -> QuantumCircuit:
        """Return a QuantumCircuit implementation

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """
        ancilla_no = self.num_ancilla_qubits()
        ancilla_qubit = []

        if ancilla_no == 1:
            ancilla_qubit = [self._n + 1]
            
        qc = QuantumCircuit(self._n + 1 + ancilla_no)
        qc.mct(
            list(range(self._n)),
            self._n,
            ancilla_qubits = ancilla_qubit,
            mode="recursion",
        )

        # should be done for all implementations
        # TODO: solve issue with reordered qubits
        self._circuit = transpile(qc, basis_gates=["cx", "u3"])
        return deepcopy(self._circuit)

    def num_ancilla_qubits(self):
        """Return number of ancilla qubits

        :return: number of ancilla qubits
        :rtype: int
        """

        if self._n > 4:
            return 1
        else:
            return 0


if __name__ == "__main__":
    pass
