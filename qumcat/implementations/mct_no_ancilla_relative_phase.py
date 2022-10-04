# Qumcat/qumcat/implementations/mct_no_ancilla_relative_phase.py
#
# Authors:
#  - Handy Kurniawan
#
# Apply the implementation from Qiskit MCT

from copy import deepcopy
from typing import List

from qiskit import QuantumCircuit, transpile

from .mct_base import MCTBase


class MCTNoAncillaRelativePhase(MCTBase):
    def __init__(self, controls_no: int, **kwargs) -> None:
        assert (
            controls_no >= 2 and controls_no <= 3
        ), "At the moment we cannot handle controls bigger than 3."
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
            return [MCTNoAncillaRelativePhase(controls_no)]  # only one available

    def generate_circuit(self) -> QuantumCircuit:
        """Return a QuantumCircuit implementation

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """
        qc = QuantumCircuit(self._n + 1)
        if self._n == 2:
            qc.rccx(0, 1, 2)
        elif self._n == 3:
            qc.rcccx(0, 1, 2, 3)
        else:
            raise ValueError("At the moment we cannot handle controls bigger than 3.")

        # should be done for all implementations
        # TODO: solve issue with reordered qubits
        self._circuit = transpile(qc, basis_gates=["cx", "u3"])
        return deepcopy(self._circuit)

    def num_ancilla_qubits(self):
        """Return number of ancilla qubits

        :return: number of ancilla qubits
        :rtype: int
        """
        return 0


if __name__ == "__main__":
    mct = MCTNoAncillaRelativePhase(4)

    circ = mct.generate_circuit()
    # print(circ.draw())
