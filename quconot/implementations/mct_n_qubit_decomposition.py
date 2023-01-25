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
    r"""
    **Decompositions of n-qubit Toffoli Gates with Linear Circuit Complexity Yong He et al.:**

    An n-qubit Toffoli gate :math:`∧_{n-1}(\sigma_{x})` can be implemented by a circuit depth of ``216n − 648``
    assisted by a recyclable auxiliary qubit. Moreover, :math:`∧_{n-1}(\sigma_{x})` requires ``24n − 72`` CNOT gates
    and ``32n−96`` :math:`T` or  :math:`T^{†}`

    .. image:: ../_static/n_qubit_tof.png
       :width: 400

    Efficient decomposition of an approximate Toffoli gate :math:`∧_{4}(\sigma_{x})` without auxiliary qubit. This
    approximate Toffoli gate is different from the Toffoli gate with the phase −1 at the \|101⟩

    .. image:: ../_static/n_qubit_tof2.png
       :width: 800

    Efficient decomposition of a 7-qubit Toffoli gate :math:`∧_{6}(\sigma_{x})` using an 8-qubit system. Here,
    one qubit is used as auxiliary qubit.

    """

    def __init__(self, controls_no: int, **kwargs) -> None:
        if controls_no < 5:
            raise ValueError("Number of controls must be >= 5 for this implementation")
        self._n = controls_no
        self._circuit: QuantumCircuit = None

    def RyDecomp(self):
        r"""Decomposition of :math: `R_{y}(frac{\pi}{4})` and its inverse :math: `R_{y}(frac{- \pi}{4})`

        Returns:
            QuantumCircuit: two 1-qubit circuits containing the decomposition and its inverse

        **Example**
            >>> print(MCTNQubitDecomposition(controls_no = 2).RyDecomp()[0])
            >>> print(MCTNQubitDecomposition(controls_no = 2).RyDecomp()[1])
               ┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐
            q: ┤ Z ├┤ S ├┤ H ├┤ T ├┤ H ├┤ S ├
               └───┘└───┘└───┘└───┘└───┘└───┘
               ┌─────┐┌───┐┌─────┐┌───┐┌─────┐┌───┐
            q: ┤ Sdg ├┤ H ├┤ Tdg ├┤ H ├┤ Sdg ├┤ Z ├
               └─────┘└───┘└─────┘└───┘└─────┘└───┘

        """
        ry_circuit = QuantumCircuit(1)
        ry_circuit.z(0)
        ry_circuit.s(0)
        ry_circuit.h(0)
        ry_circuit.t(0)
        ry_circuit.h(0)
        ry_circuit.s(0)

        return ry_circuit, ry_circuit.inverse()

    def TofDecomp(self):
        r"""Decomposition of Toffoli gate into RY and CX gates. Uses RyDecomp() for decomposition of the RY gates

        Returns:
            QuantumCircuit: A 3-qubit quantum circuit containing decomposition

        **Example**
            >>> print(MCTBarenco74Dirty(controls_no = 3).TofDecomp())
            q_0: ─────────────────────────────■───────────────────────────────
                                              │
            q_1: ─────────────■───────────────┼────────────────■──────────────
                 ┌─────────┐┌─┴─┐┌─────────┐┌─┴─┐┌──────────┐┌─┴─┐┌──────────┐
            q_2: ┤ Ry(π/4) ├┤ X ├┤ Ry(π/4) ├┤ X ├┤ Ry(-π/4) ├┤ X ├┤ Ry(-π/4) ├
                 └─────────┘└───┘└─────────┘└───┘└──────────┘└───┘└──────────┘

        """
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

        r"""Generates network of ``4(m-2)`` gates that simulates a controlled not gate with m controls. Uses
        ``TofDecomp`` when target qubit of the Toffoli gate is not target of the k gate

        Args:
            qc (QuantumCircuit): Quantum circuit to which gates are to be appended
            c (list[int]): list of control qubits of Toffoli gate
            t (int): target qubit of Toffoli gate
            a (int): auxiliary qubit of Toffoli gate
            k (int): takes values ``1`` or ``2`` depending on type of k-gate required


        Returns:
            QuantumCircuit: Appends network of gates to qc

        **Example**
            >>> qc = QuantumCircuit(9)
            >>> print(MCTBarenco74Dirty(controls_no = 5).k_gate(qc, list(range(9)), 5, 8,1))
            q_0: ─────────────────■─────────────────────────────■────────────
                                  │                             │
            q_1: ─────────────────■─────────────────────────────■────────────
                                  │                             │
            q_2: ────────────■────┼────■───────────────────■────┼────■───────
                             │    │    │                   │    │    │
            q_3: ───────■────┼────┼────┼────■─────────■────┼────┼────┼────■──
                        │    │    │    │    │         │    │    │    │    │
            q_4: ──■────┼────┼────┼────┼────┼────■────┼────┼────┼────┼────┼──
                   │    │    │  ┌─┴─┐  │    │    │    │    │  ┌─┴─┐  │    │
            q_5: ──┼────┼────■──┤ X ├──■────┼────┼────┼────■──┤ X ├──■────┼──
                   │    │  ┌─┴─┐└───┘┌─┴─┐  │    │    │  ┌─┴─┐└───┘┌─┴─┐  │
            q_6: ──┼────■──┤ X ├─────┤ X ├──■────┼────■──┤ X ├─────┤ X ├──■──
                   │  ┌─┴─┐└───┘     └───┘┌─┴─┐  │  ┌─┴─┐└───┘     └───┘┌─┴─┐
            q_7: ──■──┤ X ├───────────────┤ X ├──■──┤ X ├───────────────┤ X ├
                 ┌─┴─┐└───┘               └───┘┌─┴─┐└───┘               └───┘
            q_8: ┤ X ├─────────────────────────┤ X ├─────────────────────────
                 └───┘                         └───┘


            >>> qc = QuantumCircuit(9)
            >>> print(MCTBarenco74Dirty(controls_no = 5).k_gate(qc, list(range(9)), 5, 8,1))
                                ┌───┐                         ┌───┐
            q_0: ────────────■──┤ X ├──■───────────────────■──┤ X ├──■───────
                           ┌─┴─┐└─┬─┘┌─┴─┐               ┌─┴─┐└─┬─┘┌─┴─┐
            q_1: ───────■──┤ X ├──┼──┤ X ├──■─────────■──┤ X ├──┼──┤ X ├──■──
                      ┌─┴─┐└─┬─┘  │  └─┬─┘┌─┴─┐     ┌─┴─┐└─┬─┘  │  └─┬─┘┌─┴─┐
            q_2: ──■──┤ X ├──┼────┼────┼──┤ X ├──■──┤ X ├──┼────┼────┼──┤ X ├
                   │  └─┬─┘  │    │    │  └─┬─┘  │  └─┬─┘  │    │    │  └─┬─┘
            q_3: ──┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼──
                   │    │    │    │    │    │    │    │    │    │    │    │
            q_4: ──┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼──
                 ┌─┴─┐  │    │    │    │    │  ┌─┴─┐  │    │    │    │    │
            q_5: ┤ X ├──┼────┼────■────┼────┼──┤ X ├──┼────┼────■────┼────┼──
                 └─┬─┘  │    │    │    │    │  └─┬─┘  │    │    │    │    │
            q_6: ──┼────┼────┼────■────┼────┼────┼────┼────┼────■────┼────┼──
                   │    │    │         │    │    │    │    │         │    │
            q_7: ──┼────┼────■─────────■────┼────┼────┼────■─────────■────┼──
                   │    │                   │    │    │                   │
            q_8: ──■────■───────────────────■────■────■───────────────────■──

        """
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
        r"""Implements theorem 1 of "Decompositions of n-qubit Toffoli Gates with Linear Circuit Complexity"

        Args:
            c_qubits (list[int]): list of control qubits of Toffoli gate
            t_qubit (int): target qubit of Toffoli gate
            aux_qubit (int): auxiliary qubit of Toffoli gate

        Returns:
            QuantumCircuit: returns decomposition as quantum circuit

        **Example**
            >>> print(MCTNQubitDecomposition(controls_no = 2).MCT(c_qubits = [0,1,2,3,4], t_qubit = 5, aux_qubit = 6))
                           ┌───────────────┐     ┌───────────────┐                      »
            q_0: ──────────┤0              ├─────┤0              ├──────────────────────»
                           │               │     │               │                      »
            q_1: ──────────┤1              ├─────┤1              ├──────────────────────»
                           │               │     │               │     ┌───────────────┐»
            q_2: ───────■──┤               ├──■──┤               ├──■──┤2              ├»
                        │  │  circuit-1849 │  │  │  circuit-1849 │  │  │               │»
            q_3: ───────┼──┤               ├──┼──┤               ├──┼──┤0 circuit-1864 ├»
                        │  │               │  │  │               │  │  │               │»
            q_4: ───────┼──┤               ├──┼──┤               ├──┼──┤1              ├»
                 ┌───┐  │  │               │  │  │               │  │  └───────────────┘»
            q_5: ┤ H ├──■──┤2              ├──■──┤2              ├──■───────────────────»
                 └───┘┌─┴─┐└───────────────┘┌─┴─┐└─────┬───┬─────┘┌─┴─┐                 »
            q_6: ─────┤ X ├─────────────────┤ X ├──────┤ S ├──────┤ X ├─────────────────»
                      └───┘                 └───┘      └───┘      └───┘                 »
            «                                ┌───────────────┐     ┌───────────────┐     »
            «q_0: ───────────────────────────┤0              ├─────┤0              ├─────»
            «                                │               │     │               │     »
            «q_1: ───────────────────────────┤1              ├─────┤1              ├─────»
            «          ┌───────────────┐     │               │     │               │     »
            «q_2: ──■──┤2              ├──■──┤               ├──■──┤               ├──■──»
            «       │  │               │  │  │  circuit-1879 │  │  │  circuit-1879 │  │  »
            «q_3: ──┼──┤0 circuit-1864 ├──┼──┤               ├──┼──┤               ├──┼──»
            «       │  │               │  │  │               │  │  │               │  │  »
            «q_4: ──┼──┤1              ├──┼──┤               ├──┼──┤               ├──┼──»
            «       │  └───────────────┘  │  │               │  │  │               │  │  »
            «q_5: ──■─────────────────────■──┤2              ├──■──┤2              ├──■──»
            «     ┌─┴─┐     ┌─────┐     ┌─┴─┐└───────────────┘┌─┴─┐└─────┬───┬─────┘┌─┴─┐»
            «q_6: ┤ X ├─────┤ Sdg ├─────┤ X ├─────────────────┤ X ├──────┤ S ├──────┤ X ├»
            «     └───┘     └─────┘     └───┘                 └───┘      └───┘      └───┘»
            «
            «q_0: ───────────────────────────────────────
            «
            «q_1: ───────────────────────────────────────
            «     ┌───────────────┐     ┌───────────────┐
            «q_2: ┤2              ├──■──┤2              ├
            «     │               │  │  │               │
            «q_3: ┤0 circuit-1894 ├──┼──┤0 circuit-1894 ├
            «     │               │  │  │               │
            «q_4: ┤1              ├──┼──┤1              ├
            «     └───────────────┘  │  └─────┬───┬─────┘
            «q_5: ───────────────────■────────┤ H ├──────
            «                      ┌─┴─┐     ┌┴───┴┐
            «q_6: ─────────────────┤ X ├─────┤ Sdg ├─────
            «                      └───┘     └─────┘

        """

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
        separable_wasted_auxiliary: true / false (D), requires wasted_auxiliary set to True

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

        mct = self.MCT(control_qubits, target_qubit, aux_qubit)

        # should be done for all implementations
        # TODO: solve issue with reordered qubits
        self._circuit = transpile(mct, basis_gates=["cx", "s", "h", "t", "z", "sdg", "tdg"])

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
