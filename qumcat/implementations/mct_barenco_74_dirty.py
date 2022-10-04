# Qumcat/qumcat/implementations/mct_barenco_74_dirty.py
#
# Authors:
#  - Ankit Khandelwal
#  - Shraddha Aangiras

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

    def TofDecomp(self):
        qc = QuantumCircuit(3)
        qc.ry(np.pi / 4, 2)
        qc.cx(1, 2)
        qc.ry(np.pi / 4, 2)
        qc.cx(0, 2)
        qc.ry(-np.pi / 4, 2)
        qc.cx(1, 2)
        qc.ry(-np.pi / 4, 2)
        return qc

    def k_gate(self, qc: QuantumCircuit, c: List[int], t: int, a: int, k: int):
        k1 = int(np.floor((len(c) + 1) / 2))
        # k2 = len(c) - k1

        tof = self.TofDecomp()

        if k == 1:
            controls = c[:k1]
            target = a
            auxs = (c[k1:])[: len(controls) - 2]

        elif k == 2:

            controls = c[k1:] + [a]
            target = t
            auxs = (c[:k1] + [a])[: len(controls) - 2]

        for c1, c2, t1 in zip(controls[::-1][:-2], auxs[::-1], [target] + auxs[::-1][:-1]):
            if t1 == t:
                qc.append(CCXGate(), (c1, c2, t1))
            else:
                qc.append(tof, [c1, c2, t1])

        qc.append(tof, [controls[0], controls[1], auxs[0]])
        for c1, c2, t1 in zip(
            controls[::-1][:-2][::-1], auxs[::-1][::-1], ([target] + auxs[::-1][:-1])[::-1]
        ):
            if t1 == t:
                qc.append(CCXGate(), (c1, c2, t1))
            else:
                qc.append(tof, [c1, c2, t1])

        for c1, c2, t1 in zip(controls[::-1][1:-2], auxs[::-1][1:], auxs[::-1][:-1]):
            if t1 == t:
                qc.append(CCXGate(), (c1, c2, t1))
            else:
                qc.append(tof, [c1, c2, t1])

        qc.append(tof, [controls[0], controls[1], auxs[0]])
        for c1, c2, t1 in zip(
            controls[::-1][1:-2][::-1], auxs[::-1][1:][::-1], auxs[::-1][:-1][::-1]
        ):
            if t1 == t:
                qc.append(CCXGate(), (c1, c2, t1))
            else:
                qc.append(tof, [c1, c2, t1])

        return qc

    def L7_4(self, c_qubits: List[int], t_qubit: int, aux_qubit: int):
        n = len(c_qubits) + 2
        qc = QuantumCircuit(n)

        qc = self.k_gate(qc, c_qubits, t_qubit, aux_qubit, 1)
        qc.barrier()
        qc = self.k_gate(qc, c_qubits, t_qubit, aux_qubit, 2)
        qc.barrier()
        qc = self.k_gate(qc, c_qubits, t_qubit, aux_qubit, 1)
        qc.barrier()
        qc = self.k_gate(qc, c_qubits, t_qubit, aux_qubit, 2)

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

        circ = self.L7_4(list(range(self._n)), self._n, self._n + self.num_ancilla_qubits())

        self._circuit = transpile(circ, basis_gates=["cx", "u3"])
        # self._circuit = transpile(circ, basis_gates=["cx", "s", "h", "t", "z", "sdg", "tdg"])

        return deepcopy(self._circuit)

    def num_ancilla_qubits(self):
        """Return number of ancilla qubits

        :return: number of ancilla qubits
        :rtype: int
        """
        return 1


if __name__ == "__main__":
    MCTNQubit = MCTBarenco74Dirty(5)
    circ = MCTNQubit.generate_circuit()
    MCTNQubit.nu
    # print(circ.draw(fold=-1))
    print(circ.depth(), "depth")
    print(dict(circ.count_ops()))
