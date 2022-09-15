from copy import deepcopy
from typing import List

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import CCXGate, CXGate, XGate
from qiskit.quantum_info import Operator

from .mct_base import MCTBase


class MCTBarenco75Dirty(MCTBase):
    def __init__(self, controls_no: int, **kwargs) -> None:
        assert controls_no >= 2
        self._n = controls_no
        self._circuit: QuantumCircuit = None
        pass

    def get_V(self, root):
        circ = QuantumCircuit(2, name=f"CX^1/{root}")
        V = XGate().power(1 / root)
        V = V.control(1)
        circ.append(V, [0, 1])
        return circ

    def get_Vdg(self, root):
        circ = QuantumCircuit(2, name=f"CX^1/{root}dg")
        V = XGate().power(1 / root).adjoint()
        V = V.control(1)
        circ.append(V, [0, 1])
        return circ

    def get_mct(self, controls, target):
        if len(controls) == 1:
            return CXGate()
        if len(controls) == 2:
            return CCXGate()
        circ = QuantumCircuit(len(controls) + 1, name="mct")
        # Change with mct implementation
        circ.mcx(controls, target)
        return circ

    def recursive(self, qubitss):
        circ = QuantumCircuit(len(qubitss))

        def make_mct(self, circ, qubits, root=1):
            if len(qubits) == 2:
                circ.append(self.get_V(self, root), qubits)
                return circ

            CV = self.get_V(self, root * 2)
            CVdg = self.get_Vdg(self, root * 2)

            mcx = self.get_mct(self, qubits[:-2], qubits[-2])

            circ.append(CV, [qubits[-2], qubits[-1]])
            circ.append(mcx, qubits[:-1])
            circ.append(CVdg, [qubits[-2], qubits[-1]])
            circ.append(mcx, qubits[:-1])

            ccv = make_mct(self, circ, qubits[:-2] + [qubits[-1]], root * 2)

            return ccv

        circ = make_mct(self, circ, qubitss, 1)

        return circ

    @classmethod
    def generate_mct_cases(cls, controls_no: int, max_ancilla: int, **kwargs) -> List["MCTBase"]:
        """Generate all possible MCT implementation satisfying the requirements

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """
        if max_ancilla < controls_no - 2:
            return []  # if max_ancilla allowed is to small - no representation given
        else:
            return [MCTBarenco75Dirty(controls_no)]  # only one available

    @classmethod
    def MCT(self, controls_no):
        return self.recursive(self, list(range(controls_no + 1)))

    def generate_circuit(self) -> QuantumCircuit:
        """Return a QuantumCircuit implementation

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """

        # print("self._n : ", self._n, ", self.num_ancilla_qubit : ", self.num_ancilla_qubits())

        circ = self.MCT(self._n)

        self._circuit = transpile(circ, basis_gates=["cx", "u3"])

        return deepcopy(self._circuit)

    def num_ancilla_qubits(self):

        return 0


if __name__ == "__main__":
    MCTNQubit = MCTBarenco75Dirty(3)
    circ = MCTNQubit.generate_circuit()
    # print(circ.draw(fold=-1))
    print(circ.depth(), "depth")
    print(dict(circ.count_ops()))
