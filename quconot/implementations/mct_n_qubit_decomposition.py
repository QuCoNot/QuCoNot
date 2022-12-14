# Quconot/quconot/implementations/mct_n_qubit_decomposition.py
#
# Authors:
#  - Ankit Khandelwal
#  - Shraddha Aangiras
#############
# Decompositions of n-qubit Toffoli Gates with Linear Circuit Complexity
# This implementation is based on part 1 of the paper "Decompositions of n-qubit
# Toffoli Gates with Linear Circuit Complexity".
# https://doi.org/10.1007/s10773-017-3389-4
# From our testing, it looks like the implementation in the paper is incorrect.
# Some of the phase Toffoli gates
# that are in the decomposition must be replaced with actual Toffolis for the
# implementation to work.
# The implementation in this file contains this fix.
# We do not find any advantage in this implementation. The original
# implementation from the paper "Elementary gates for quantum computation",
# is basically the same decomposition. There it also says which gates need
# to be actual Toffolis.
# The depth mentioned in the paper is also a naive calculation and offers an
# upper bound. The actual depth of the circuit is lower.
#############

from copy import deepcopy
from typing import List

import numpy as np
from qiskit import QuantumCircuit, transpile

from .mct_base import MCTBase


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
        ry, ry_inv = self.RyDecomp()
        qc = QuantumCircuit(3)
        qc.append(ry, [2])
        qc.cx(1, 2)
        qc.append(ry, [2])
        qc.cx(0, 2)
        qc.append(ry_inv, [2])
        qc.cx(1, 2)
        qc.append(ry_inv, [2])
        return qc

    def k_gate(self, qc: QuantumCircuit, c: List[int], t: int, a: int, k: int):
        from qiskit.circuit.library import CCXGate

        k1 = int(np.ceil((len(c) + 1) / 2))
        k2 = len(c) - k1

        tof = self.TofDecomp()
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

    def MCT(self, c_qubits: List[int], t_qubit: int, aux_qubit: int):
        qc = QuantumCircuit(len(c_qubits) + 2)

        qc.h(t_qubit)
        qc = self.k_gate(qc, c_qubits, t_qubit, aux_qubit, 1)
        qc.s(aux_qubit)
        qc = self.k_gate(qc, c_qubits, t_qubit, aux_qubit, 2)
        qc.sdg(aux_qubit)
        qc = self.k_gate(qc, c_qubits, t_qubit, aux_qubit, 1)
        qc.s(aux_qubit)
        qc = self.k_gate(qc, c_qubits, t_qubit, aux_qubit, 2)
        qc.sdg(aux_qubit)
        qc.h(t_qubit)

        return qc

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
        separable_wasted_auxiliary: true / false (D)    # requires wasted_auxiliary set to True

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """
        if max_auxiliary < controls_no - 2:
            return []  # if max_auxiliary allowed is to small - no representation given
        else:
            return [MCTNQubitDecomposition(controls_no)]  # only one available

    def generate_circuit(self) -> QuantumCircuit:
        """Return a QuantumCircuit implementation

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """

        control_qubits = list(range(self._n))
        target_qubit = self._n
        aux_qubit = self._n + 1

        circ = QuantumCircuit(self._n + 2, self._n + 1)

        mct = self.MCT(control_qubits, target_qubit, aux_qubit)

        circ.append(mct, control_qubits + [target_qubit] + [aux_qubit])

        # should be done for all implementations
        # TODO: solve issue with reordered qubits
        self._circuit = transpile(circ, basis_gates=["cx", "s", "h", "t", "z", "sdg", "tdg"])

        return deepcopy(self._circuit)

    def num_auxiliary_qubits(self):
        """Return number of auxiliary qubits

        :return: number of auxiliary qubits
        :rtype: int
        """
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
