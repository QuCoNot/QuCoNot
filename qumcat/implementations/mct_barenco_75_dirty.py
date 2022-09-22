from copy import deepcopy
from typing import List

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import CCXGate, CXGate, XGate

from .mct_base import MCTBase


class MCTBarenco75Dirty(MCTBase):
    def __init__(self, controls_no: int, **kwargs) -> None:
        assert controls_no >= 2
        self._n = controls_no
        self._circuit: QuantumCircuit = None
        pass

    def get_V(self, root: int):
        circ = QuantumCircuit(2, name=f"CX^1/{root}")
        V = XGate().power(1 / root)
        V = V.control(1)
        circ.append(V, [0, 1])
        return circ

    def get_Vdg(self, root: int):
        circ = QuantumCircuit(2, name=f"CX^1/{root}dg")
        V = XGate().power(1 / root).adjoint()
        V = V.control(1)
        circ.append(V, [0, 1])
        return circ

    def get_mct(self, controls: List[int], target: int):
        if len(controls) == 1:
            return CXGate()
        if len(controls) == 2:
            return CCXGate()
        circ = QuantumCircuit(len(controls) + 1, name="mct")
        # Change with mct implementation
        circ.mcx(controls, target)
        return circ

    def recursive(self, qubitss: List[int]):
        circ = QuantumCircuit(len(qubitss))

        def make_mct(circ: QuantumCircuit, qubits: List[int], root: int = 1):
            if len(qubits) == 2:
                circ.append(self.get_V(root), qubits)
                return circ

            CV = self.get_V(root * 2)
            CVdg = self.get_Vdg(root * 2)

            mcx = self.get_mct(qubits[:-2], qubits[-2])

            circ.append(CV, [qubits[-2], qubits[-1]])
            circ.append(mcx, qubits[:-1])
            circ.append(CVdg, [qubits[-2], qubits[-1]])
            circ.append(mcx, qubits[:-1])

            ccv = make_mct(circ, qubits[:-2] + [qubits[-1]], root * 2)

            return ccv

        circ = make_mct(circ, qubitss, 1)

        return circ

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
            return [MCTBarenco75Dirty(controls_no)]  # only one available

    def generate_circuit(self) -> QuantumCircuit:
        """Return a QuantumCircuit implementation

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """

        circ = self.recursive(list(range(self._n + 1)))

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
