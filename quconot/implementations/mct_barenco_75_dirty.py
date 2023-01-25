# Quconot/quconot/implementations/mct_barenco_75_dirty.py
#
# Authors:
#  - Ankit Khandelwal
#  - Shraddha Aangiras

from copy import deepcopy
from typing import List

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import CCXGate, CXGate, XGate

from .mct_base import MCTBase


class MCTBarenco75Dirty(MCTBase):
    def __init__(self, controls_no: int, **kwargs) -> None:
        if controls_no < 2:
            raise ValueError("Number of controls must be >= 2 for this implementation")
        self._n = controls_no
        self._circuit: QuantumCircuit = None

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
        if max_auxiliary < controls_no - 2:
            return []  # if max_auxiliary allowed is to small - no representation given
        else:
            return [MCTBarenco75Dirty(controls_no)]  # only one available

    def generate_circuit(self) -> QuantumCircuit:
        """Return a QuantumCircuit implementation

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """

        circ = self.recursive(list(range(self._n + 1)))
        # print(circ.draw())
        self._circuit = transpile(circ, basis_gates=["cx", "u3"])

        return deepcopy(self._circuit)

    def num_auxiliary_qubits(self):
        """Return number of auxiliary qubits

        :return: number of auxiliary qubits
        :rtype: int
        """
        return 0
