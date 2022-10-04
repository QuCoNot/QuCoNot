# Qumcat/qumcat/implementations/mct_vchain_dirty.py
#
# Authors:
#  - Handy Kurniawan
#
# Apply the implementation from Qiskit MCT

from copy import deepcopy
from typing import List

from qiskit import QuantumCircuit, transpile

from .mct_base import MCTBase


class MCTVChainDirty(MCTBase):
    def __init__(self, controls_no: int, **kwargs) -> None:
        assert controls_no >= 2
        self._n = controls_no
        self._circuit: QuantumCircuit = None
        pass

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
            return [MCTVChainDirty(controls_no)]  # only one available

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
            mode="v-chain-dirty",
        )

        # should be done for all implementations
        # TODO: solve issue with reordered qubits
        self._circuit = transpile(qc, basis_gates=["cx", "u3"])
        return deepcopy(self._circuit)

    def num_ancilla_qubits(self):
        """Return number of ancilla qubits

        :return: number of ancilla qubits
        :rtype: int
        """
        return self._n - 2


if __name__ == "__main__":
    print(MCTVChainDirty.generate_mct_cases(5, 1))  # not enough ancilla - empty list

    cases = MCTVChainDirty.generate_mct_cases(5, 3)
    assert len(cases) == 1  # here only one case
    case = cases[0]

    circ = case.generate_circuit()
    # print(circ.draw())

    # I can get quickly statistics out of it now
    print(case.num_ancilla_qubits())  # this is very fast as always known
    print(case.num_gates())
    print(case.depth())

    cases = MCTVChainDirty.generate_mct_cases(5, 3)
    assert len(cases) == 1  # here only one case
    case = cases[0]

    # if depth not previously known, generate circuit and compute (see base)
    cases = MCTVChainDirty.generate_mct_cases(5, 3)
    assert len(cases) == 1  # here only one case
    case = cases[0]
    print(case.depth())
