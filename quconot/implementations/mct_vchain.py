# Quconot/quconot/implementations/mct_vchain.py
#
# Authors:
#  - Handy Kurniawan
#
# Apply the implementation from Qiskit MCT

from copy import deepcopy
from typing import List

from qiskit import QuantumCircuit, transpile

from .mct_base import MCTBase


class MCTVChain(MCTBase):
    r"""
    Implementation of the multi-controlled not gate with no auxiliary qubits using Qiskit’s ``v-chain`` mode.
    This is implemented using MCXVChain, using a V-chain of CX gates.
    Requires 2 less auxiliary than the number of control qubits
    """
    def __init__(self, controls_no: int, **kwargs) -> None:
        assert controls_no >= 2
        self._n = controls_no
        self._circuit: QuantumCircuit = None
        pass

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
            return [MCTVChain(controls_no)]  # only one available

    def generate_circuit(self) -> QuantumCircuit:
        """Return a QuantumCircuit implementation

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """
        qc = QuantumCircuit(2 * self._n - 1)
        qc.mct(
            list(range(self._n)),
            self._n,
            ancilla_qubits=list(range(self._n + 1, 2 * self._n - 1)),
            mode="v-chain",
        )

        # should be done for all implementations
        # TODO: solve issue with reordered qubits
        self._circuit = transpile(qc, basis_gates=["cx", "u3"])
        return deepcopy(self._circuit)

    def num_auxiliary_qubits(self):
        """Return number of auxiliary qubits

        :return: number of auxiliary qubits
        :rtype: int
        """
        return self._n - 2


if __name__ == "__main__":
    print(MCTVChain.verify_mct_cases(5, 1))  # not enough auxiliary - empty list

    cases = MCTVChain.verify_mct_cases(5, 3)
    assert len(cases) == 1  # here only one case
    case = cases[0]

    circ = case.generate_circuit()
    # print(circ.draw())

    # I can get quickly statistics out of it now
    print(case.num_auxiliary_qubits())  # this is very fast as always known
    print(case.num_gates())
    print(case.depth())

    cases = MCTVChain.verify_mct_cases(5, 3)
    assert len(cases) == 1  # here only one case
    case = cases[0]

    # if depth not previously known, generate circuit and compute (see base)
    cases = MCTVChain.verify_mct_cases(5, 3)
    assert len(cases) == 1  # here only one case
    case = cases[0]
    print(case.depth())
