from copy import deepcopy
from typing import List

import numpy as np
from qiskit import QuantumCircuit, transpile

from qumcat.mct_base import MCTBase


class MCTNQubitDecomposition(MCTBase):
    def __init__(self, controls_no: int, **kwargs) -> None:
        assert controls_no >= 2
        self._n = controls_no
        self._circuit: QuantumCircuit = None
        pass

    def RyDecomp(self):
        ry_circuit = QuantumCircuit(1)
        ry_circuit.z(0)
        ry_circuit.s(0)
        ry_circuit.h(0)
        ry_circuit.t(0)
        ry_circuit.h(0)
        ry_circuit.s(0)

        return ry_circuit, ry_circuit.inverse()

    def TofDecomp(self):
        ry, ry_inv = self.RyDecomp(self)
        qc = QuantumCircuit(3)
        qc.append(ry, [2])
        qc.cx(1, 2)
        qc.append(ry, [2])
        qc.cx(0, 2)
        qc.append(ry_inv, [2])
        qc.cx(1, 2)
        qc.append(ry_inv, [2])
        return qc

    def k_gate(self, qc, c, t, a, k):
        from qiskit.circuit.library import CCXGate

        k1 = int(np.ceil((len(c) + 1) / 2))
        k2 = len(c) - k1

        tof = self.TofDecomp(self)
        # tof = CCXGate()

        if k == 1:
            controls = c[:k1]
            target = a
            auxs = c[::-1][: k1 - 3][::-1] + [t]
        elif k == 2:
            controls = c[::-1][:k2][::-1] + [t]
            target = a
            auxs = c[:k1][::-1][: k2 - 1]

        for c1, c2, t1 in zip(controls[::-1][:-2], auxs[::-1], [target] + auxs[::-1][:-1]):
            if t1 == a:
                qc.append(CCXGate(), (c1, c2, t1))
            else:
                qc.append(tof, [c1, c2, t1])
        qc.append(tof, [controls[0], controls[1], auxs[0]])
        for c1, c2, t1 in zip(
            controls[::-1][:-2][::-1], auxs[::-1][::-1], ([target] + auxs[::-1][:-1])[::-1]
        ):
            if t1 == a:
                qc.append(CCXGate(), (c1, c2, t1))
            else:
                qc.append(tof, [c1, c2, t1])

        for c1, c2, t1 in zip(controls[::-1][1:-2], auxs[::-1][1:], auxs[::-1][:-1]):
            if t1 == a:
                qc.append(CCXGate(), (c1, c2, t1))
            else:
                qc.append(tof, [c1, c2, t1])

        qc.append(tof, [controls[0], controls[1], auxs[0]])
        for c1, c2, t1 in zip(
            controls[::-1][1:-2][::-1], auxs[::-1][1:][::-1], auxs[::-1][:-1][::-1]
        ):
            if t1 == a:
                qc.append(CCXGate(), (c1, c2, t1))
            else:
                qc.append(tof, [c1, c2, t1])

        return qc

    @classmethod
    def generate_mct_cases(cls, controls_no: int, max_ancilla: int, **kwargs) -> List["MCTBase"]:
        """Generate all possible MCT implementation satisfying the requirements

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """
        if max_ancilla < controls_no - 2:
            return []  # if max_ancilla allowed is to small - no representation given
        else:
            return [MCTNQubitDecomposition(controls_no)]  # only one available

    @classmethod
    def MCT(self, c_qubits, t_qubit, aux_qubit):
        qc = QuantumCircuit(len(c_qubits) + 2)

        qc.h(t_qubit)
        qc = self.k_gate(self, qc, c_qubits, t_qubit, aux_qubit, 1)
        qc.s(aux_qubit)
        qc = self.k_gate(self, qc, c_qubits, t_qubit, aux_qubit, 2)
        qc.sdg(aux_qubit)
        qc = self.k_gate(self, qc, c_qubits, t_qubit, aux_qubit, 1)
        qc.s(aux_qubit)
        qc = self.k_gate(self, qc, c_qubits, t_qubit, aux_qubit, 2)
        qc.sdg(aux_qubit)
        qc.h(t_qubit)

        return qc

    def generate_circuit(self) -> QuantumCircuit:
        """Return a QuantumCircuit implementation

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """

        control_qubits = list(range(self._n))
        target_qubit = self._n
        aux_qubit = self._n + 1

        circ = QuantumCircuit(self._n + 2, self._n + 1)
        circ.append(
            self.MCT(control_qubits, target_qubit, aux_qubit),
            control_qubits + [target_qubit] + [aux_qubit],
        )

        # should be done for all implementations
        # TODO: solve issue with reordered qubits
        self._circuit = transpile(circ, basis_gates=["cx", "s", "h", "t", "z", "sdg", "tdg"])

        return deepcopy(self._circuit)

    def num_ancilla_qubits(self):
        if self._n > 4:
            return 1
        else:
            return 0


if __name__ == "__main__":
    MCTNQubit = MCTNQubitDecomposition(6)
    circ = MCTNQubit.generate_circuit()
    # print(circ.draw(fold=-1))
    print(circ.depth(), "depth")
    print(dict(circ.count_ops()))
