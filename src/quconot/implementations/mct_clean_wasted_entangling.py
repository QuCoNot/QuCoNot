# Quconot/quconot/implementations/mct_clean_wasted_entangling.py
#
# Authors:
#  - Adam Glos

from typing import List

from qiskit import QuantumCircuit

from .mct_base import MCTBase


class MCTCleanWastedEntangling(MCTBase):
    def __init__(self, controls_no: int, **kwargs) -> None:
        if controls_no < 3:
            raise ValueError("Number of controls must be >= 3 for this implementation")
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
        if max_auxiliary != controls_no - 1:
            return []  # if max_auxiliary allowed is incorrect - no representation given
        else:
            return [MCTCleanWastedEntangling(controls_no)]  # only one available

    def generate_circuit(self) -> QuantumCircuit:
        """Return a QuantumCircuit implementation

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """
        qc = QuantumCircuit(self._n + 1 + self.num_auxiliary_qubits())

        ancilla_ind = self._n + 1
        if self.num_auxiliary_qubits():
            qc.rccx(0, 1, ancilla_ind)
        for i in range(0, self.num_auxiliary_qubits() - 1):
            qc.rccx(1 + i, ancilla_ind + i, ancilla_ind + i + 1)
        qc.rccx(self._n - 1, qc.num_qubits - 1, self._n)
        return qc

    def num_auxiliary_qubits(self):
        """Return number of auxiliary qubits

        :return: number of auxiliary qubits
        :rtype: int
        """
        return self._n - 1
