from copy import deepcopy
from typing import List

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import CCXGate

from .mct_base import MCTBase


class MCTBarenco74Dirty(MCTBase):
    def __init__(self, controls_no: int, **kwargs) -> None:
        assert controls_no >= 2
        self._n = controls_no
        self._circuit: QuantumCircuit = None
        pass

    # Lemma 7.2
    def L7_2(self, c: int, a: int, t: bool = False):

        total_qubits = c + a + 1

        qc = QuantumCircuit(total_qubits)
        tof = CCXGate()

        # print("c : ", c, ", a : ", a, ", t:", t)

        def netw(c: int, a: int, t: bool = False, sec: int = 0):
            n = 2 * c - 1 + sec
            for i in range(n - 1, c + sec, -1):
                qc.append(tof, [c + i - n, i - 1, i])

            if t == True:
                qc.append(CCXGate(), [0, 1, c + sec])
            else:
                qc.append(tof, [0, 1, c + sec])

            for i in range(c + sec + 1, n):
                qc.append(tof, [c + i - n, i - 1, i])

        if c == 2:
            qc.ccx(0, 1, c)
        else:
            netw(c, a, t=t)
            netw(c - 1, a, t=t, sec=1)

        return qc

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
            return [MCTBarenco74Dirty(controls_no)]  # only one available

    def generate_circuit(self) -> QuantumCircuit:
        """Return a QuantumCircuit implementation

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """
        controls_no = self._n
        ancillas_no = self.num_ancilla_qubits()

        circ = QuantumCircuit(controls_no + ancillas_no + 1)

        n = controls_no + ancillas_no + 1
        m1 = controls_no
        m2 = ancillas_no

        # print(list(range(n)))
        # print(list(range(m1, n)), list(range(0, m1)))
        # print(list(range(m1, n)) + list(range(0, m1)))

        circ.append(self.L7_2(m1, m2), list(range(n)))
        circ.append(self.L7_2(m2, m1, t=True), list(range(m1, n)) + list(range(0, m1)))
        circ.append(self.L7_2(m1, m2), list(range(n)))
        circ.append(self.L7_2(m2, m1, t=True), list(range(m1, n)) + list(range(0, m1)))

        self._circuit = transpile(circ, basis_gates=["cx", "s", "h", "t", "z", "sdg", "tdg"])

        return deepcopy(self._circuit)

    def num_ancilla_qubits(self):

        return (self._n * 2) - self._n - 1


if __name__ == "__main__":
    MCTNQubit = MCTBarenco74Dirty(3)
    circ = MCTNQubit.generate_circuit()
    # print(circ.draw(fold=-1))
    print(circ.depth(), "depth")
    print(dict(circ.count_ops()))
