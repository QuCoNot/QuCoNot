# Quconot/quconot/implementations/mct_barenco_74_dirty.py
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
    r"""
    **Multi-controlled not implementation using Corollary 7.4 of Barenco et al:**

    On an :math:`n`-bit network (where :math:`n ≥ 7`), a :math:`∧_{n-2}(\sigma_{x})` gate can be simulated by ``8(
    n−5)`` :math:`∧_{2}(\sigma_{x})` gates (3-bit Toffoli gates), as well as by ``48n−204`` basic operations. In this
    implementation, at least one auxiliary qubit is required i.e. in an :math:`n` qubit network is required for an
    :math:`(n-1)` qubit gate :math:`∧_{n-2}(\sigma_{x})`

    First, Lemma 7.2 is applied, with :math:`m_{1} = \lceil \frac{n}{2} \rceil` and :math:`m_{2} = n - m_{1} - 1` to
    simulate :math:`∧_{m_1}(\sigma_{x})` and :math:`∧_{m_2}(\sigma_{x})` gates. It allows a :math:`∧_{m}(\sigma_{x})`
    gate to be simulated by a network consisting of ``4(m-2)`` :math:`∧_{2}(\sigma_{x})` gates and is of the form:

    Using Lemma 7.3, these gates are combined to simulate the :math:`∧_{n-2}(\sigma_{x})` gate. It allows a
    :math:`∧_{n-2}(\sigma_{x})` gate to be simulated by a network of two :math:`∧_{m}(\sigma_{x})` and two :math:`∧_{
    n-m-1}(\sigma_{x})` gates.

    Almost all of the Toffoli gates need only to be simulated modulo phase factors, except 4 Toffoli gates which
    involve the last bit which need to be simulated without it. Thus, these 4 gates are simulated by 16 basic
    operations, while the other ``8n-36`` Toffoli gates are simulated in just 6 basic operations.
    """

    def __init__(self, controls_no: int, **kwargs) -> None:
        if controls_no < 5:
            raise ValueError("Number of controls must be >= 5 for this implementation")
        self._n = controls_no
        self._circuit: QuantumCircuit = None

    def TofDecomp(self):
        r"""Decomposition of Toffoli gate into RY and CX gates

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
        r"""Generates network of ``4(m-2)`` gates that simulates a controlled not gate with m controls. Uses
        ``TofDecomp`` when target qubit of the Toffoli gate is not target of the k gate

        Args:
            qc (QuantumCircuit): Quantum circuit to which gates are to be appended
            c(list[int]): list of control qubits of Toffoli gate
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
        r"""Returns multi-controlled not implementation of Lemma 7.4

        Args:
            c_qubits(list[int]): list of control qubits of Toffoli gate
            t_qubit (int): target qubit of Toffoli gate
            aux_qubit (int): auxiliary qubit of Toffoli gate

        Returns:
            QuantumCircuit: returns quantum circuit containing required MCT gate

        """
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
            return [MCTBarenco74Dirty(controls_no)]  # only one available

    def generate_circuit(self) -> QuantumCircuit:
        """Return a QuantumCircuit implementation

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """

        circ = self.L7_4(list(range(self._n)), self._n, self._n + self.num_auxiliary_qubits())

        self._circuit = circ

        return deepcopy(self._circuit)

    def num_auxiliary_qubits(self):
        """Return number of auxiliary qubits

        :return: number of auxiliary qubits
        :rtype: int
        """
        return 1
