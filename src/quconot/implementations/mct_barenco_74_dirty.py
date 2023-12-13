# Quconot/quconot/implementations/mct_barenco_74_dirty.py
#
# This implementation is based on Lemma 7.3 / Corollary 7.4 of
# Barenco et al. 'Elementary gates for quantum computation`
# https://doi.org/10.1103/PhysRevA.52.3457
# NOTE: The current version uses 4 more strict Toffoli gates than mentioned in the paper.

from copy import deepcopy
from typing import List

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import CCXGate

from .mct_base import MCTBase


class MCTBarenco74Dirty(MCTBase):
    def __init__(self, controls_no: int, **kwargs) -> None:
        if controls_no < 5:
            raise ValueError("Number of controls must be >= 5 for this implementation")
        self._n = controls_no
        self._circuit: QuantumCircuit = None

    @staticmethod
    def RTofDecomp():
        '''
        Creates a relative Toffoli gate as described in Section VI B of Barenco et al.
        The Ry gate in the paper is defined differently from the usual convention.
        Ry (from paper) = Ry†
        '''
        qc = QuantumCircuit(3, name='RTOF')
        qc.ry(-np.pi / 4, 2)
        qc.cx(1, 2)
        qc.ry(-np.pi / 4, 2)
        qc.cx(0, 2)
        qc.ry(np.pi / 4, 2)
        qc.cx(1, 2)
        qc.ry(np.pi / 4, 2)
        return qc

    def MCT72(self, n: int):
        '''
        Prepare an MCT using Lemma 7.2 of Barenco et al.
        Replaces all Toffoli gates with Relative Toffoli gates if
        the target of the Toffoli is not the same as the target of the MCT.
        '''
        controls = list(range(n))
        target = n + n - 2
        auxs = list(range(n, n + n - 2))

        qc = QuantumCircuit(n + n - 1, name='MCT72')

        for c1, c2, t in zip(controls[::-1][:n - 2], auxs[::-1][:n - 2], [target] + auxs[::-1][:n - 2]):
            if t == target:
                qc.append(CCXGate(), [c1, c2, t])
            else:
                qc.append(self.RTofDecomp(), [c1, c2, t])

        qc.append(self.RTofDecomp(), [controls[0], controls[1], auxs[0]])

        for c1, c2, t in zip(controls[2:], auxs, auxs[1:] + [target]):
            if t == target:
                qc.append(CCXGate(), [c1, c2, t])
            else:
                qc.append(self.RTofDecomp(), [c1, c2, t])

        ### Second Half

        for c1, c2, t in zip(controls[::-1][1:n - 2], auxs[::-1][1:n - 2], auxs[::-1][:n - 2]):
            qc.append(self.RTofDecomp(), [c1, c2, t])

        qc.append(self.RTofDecomp(), [controls[0], controls[1], auxs[0]])

        for c1, c2, t in zip(controls[2:], auxs, auxs[1:]):
            qc.append(self.RTofDecomp(), [c1, c2, t])
        return qc

    def L7_4(self, n: int):
        '''
        Combine 4 MCT72 to get an MCT with one auxiliary
        '''
        n = n + 2
        c1 = int(np.floor(n / 2))
        c2 = n - c1 - 1
        qc = QuantumCircuit(n)

        qc.append(self.MCT72(c1), list(range(c1)) + list(range(c1, n))[:c1 - 2] + [n - 2])
        qc.append(self.MCT72(c2), list(range(c1, c1 + c2)) + list(range(c1))[:c2 - 2] + [n - 1])
        qc.append(self.MCT72(c1), list(range(c1)) + list(range(c1, n))[:c1 - 2] + [n - 2])
        qc.append(self.MCT72(c2), list(range(c1, c1 + c2)) + list(range(c1))[:c2 - 2] + [n - 1])

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

        circ = self.L7_4(self._n)
        self._circuit = circ

        return deepcopy(self._circuit)

    def num_auxiliary_qubits(self):
        """Return number of auxiliary qubits

        :return: number of auxiliary qubits
        :rtype: int
        """
        return 1
