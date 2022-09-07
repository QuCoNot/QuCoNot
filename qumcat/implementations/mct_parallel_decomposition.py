from copy import deepcopy
from typing import List

from qiskit import QuantumCircuit, transpile

from .mct_base import MCTBase


class MCTParallelDecomposition(MCTBase):
    def __init__(self, controls_no: int, **kwargs) -> None:
        assert controls_no >= 2
        self._n = controls_no
        self._circuit: QuantumCircuit = None
        pass

    def get_toffoli(self, qc, c1, c2, t):
        qc.toffoli(c1, c2, t)

        return qc

    def get_pairs(self, qubits, left):
        if len(qubits) % 2 == 0:
            pairs = [[qubits[i], qubits[i + 1]] for i in range(0, len(qubits), 2)]
            return pairs, left
        else:
            pairs = [[qubits[i], qubits[i + 1]] for i in range(0, len(qubits) - 1, 2)]
            left.append(qubits[-1])
            return pairs, left

    @classmethod
    def generate_mct_cases(cls, controls_no: int, max_ancilla: int, **kwargs) -> List["MCTBase"]:
        """Generate all possible MCT implementation satisfying the requirements

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """
        if max_ancilla < controls_no - 2:
            return []  # if max_ancilla allowed is to small - no representation given
        else:
            return [MCTParallelDecomposition(controls_no)]  # only one available

    @classmethod
    def MCT(self, c_qubits, t_qubit, aux_qubits):
        qc = QuantumCircuit(len(c_qubits) + len(aux_qubits) + 1)

        ps, ls = [], []
        layers, uss = [], []

        p, left = self.get_pairs(self, c_qubits, [])
        ps.append(p)
        ls.append(left)

        layers.append([[p[i], aux_qubits[i]] for i in range(len(p))])
        uss.append([aux_qubits[i] for i in range(len(p))])

        p, left = self.get_pairs(self, uss[-1], ls[-1])

        while True:
            ps.append(p)
            ls.append(left)
            left = sum(len(w) for w in uss)
            layers.append([[ps[-1][i], aux_qubits[i + left]] for i in range(len(ps[-1]))])
            uss.append([aux_qubits[i + left] for i in range(len(ps[-1]))])
            p, left = self.get_pairs(self, uss[-1], ls[-1])
            if len(p) == 0 and len(left) == 2:
                break
            if len(p) == 1 and len(left) == 0:
                break

        for l1 in layers:
            for c, t in l1:
                qc = self.get_toffoli(self, qc, c[0], c[1], t)

        if left:
            qc = self.get_toffoli(self, qc, left[0], left[1], t_qubit)
        if p:
            qc = self.get_toffoli(self, qc, p[0][0], p[0][1], t_qubit)

        for l1 in layers[::-1]:
            for c, t in l1:
                qc = self.get_toffoli(self, qc, c[0], c[1], t)

        return qc

    def generate_circuit(self) -> QuantumCircuit:
        """Return a QuantumCircuit implementation

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """

        control_qubits = list(range(self._n))
        target_qubit = self._n
        num_aux_qubits = self._n - 2
        aux_qubits = list(range(self._n + 1, self._n + num_aux_qubits + 1))

        circ = QuantumCircuit(self._n + 1 + num_aux_qubits, self._n + 1 + num_aux_qubits)

        U = self.MCT(control_qubits, target_qubit, aux_qubits)

        circ.append(U, control_qubits + [target_qubit] + aux_qubits)

        # should be done for all implementations
        # TODO: solve issue with reordered qubits
        self._circuit = transpile(circ, basis_gates=["cx", "s", "h", "t", "z", "sdg", "tdg"])

        return deepcopy(self._circuit)

    def num_ancilla_qubits(self):
        return self._n > 4 - 2


if __name__ == "__main__":
    MCTParallel = MCTParallelDecomposition(6)
    circ = MCTParallel.generate_circuit()
    # print(circ.draw(fold=-1))
    print(circ.depth(), "depth")
    print(dict(circ.count_ops()))