# Quconot/quconot/implementations/mct_no_auxiliary_relative_phase.py
#
# Authors:
#  - Handy Kurniawan
#
# Apply the implementation from Qiskit MCT

from copy import deepcopy
from typing import List

from qiskit import QuantumCircuit, transpile

from .mct_base import MCTBase


class MCTNoAuxiliaryRelative(MCTBase):

    r"""

    This is an implementation of the simplified Toffoli gates according to Qiskit. Currently,
    for this implementation, the number of controls is restricted to 2 or 3 only. They have been implemented using
    the RCCXGate and the RC3XGate in Qiskit. It implements the 2 or 3 controlled Toffoli gate up to relative phases.

    The simplified Toffoli is not equivalent to the Toffoli, but can be used in places where the Toffoli is
    uncomputed again.

    The implementation follows https://arxiv.org/abs/1508.03273, the dashed box of Fig. 3 and Fig. 4.

    No auxiliary qubits are used for the implementation.


    For two controls, the ``RCCXGate`` is implemented, which uses ``3`` CX gates.

    **Matrix representation**

    .. image:: ../_static/RCCX_gate.png
        :width: 400

    **Decomposition**
            >>>
            q_0: ────────────────────────■────────────────────────
                                         │
            q_1: ────────────■───────────┼─────────■──────────────
                 ┌───┐┌───┐┌─┴─┐┌─────┐┌─┴─┐┌───┐┌─┴─┐┌─────┐┌───┐
            q_2: ┤ H ├┤ T ├┤ X ├┤ Tdg ├┤ X ├┤ T ├┤ X ├┤ Tdg ├┤ H ├
                 └───┘└───┘└───┘└─────┘└───┘└───┘└───┘└─────┘└───┘


    For three controls, the ``RC3XGate`` is implemented, which uses ``6`` CX gates.

    **Matrix representation**

    .. image:: ../_static/RC3X_gate.png
        :width: 400

    **Decomposition**
            >>>
            q_0: ─────────────────────────────■─────────────────────■──────────────────────────────────────────────
                                              │                     │
            q_1: ─────────────────────────────┼─────────■───────────┼─────────■────────────────────────────────────
                                              │         │           │         │
            q_2: ────────────■────────────────┼─────────┼───────────┼─────────┼─────────────────────■──────────────
                 ┌───┐┌───┐┌─┴─┐┌─────┐┌───┐┌─┴─┐┌───┐┌─┴─┐┌─────┐┌─┴─┐┌───┐┌─┴─┐┌─────┐┌───┐┌───┐┌─┴─┐┌─────┐┌───┐
            q_3: ┤ H ├┤ T ├┤ X ├┤ Tdg ├┤ H ├┤ X ├┤ T ├┤ X ├┤ Tdg ├┤ X ├┤ T ├┤ X ├┤ Tdg ├┤ H ├┤ T ├┤ X ├┤ Tdg ├┤ H ├
                 └───┘└───┘└───┘└─────┘└───┘└───┘└───┘└───┘└─────┘└───┘└───┘└───┘└─────┘└───┘└───┘└───┘└─────┘└───┘



    """

    def __init__(self, controls_no: int, **kwargs) -> None:
        assert (
            controls_no >= 2 and controls_no <= 3
        ), "At the moment we cannot handle controls bigger than 3."
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
        separable_wasted_auxiliary: true / false (D), requires wasted_auxiliary set to True

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """
        return [MCTNoAuxiliaryRelative(controls_no)]

    def generate_circuit(self) -> QuantumCircuit:
        r"""

        Returns simplified Toffoli gate

        Returns:
            QuantumCircuit: quantum circuit containing simplified Toffoli gate

        """
        qc = QuantumCircuit(self._n + 1)
        if self._n == 2:
            qc.rccx(0, 1, 2)
        elif self._n == 3:
            qc.rcccx(0, 1, 2, 3)

        # should be done for all implementations
        # TODO: solve issue with reordered qubits
        self._circuit = transpile(qc, basis_gates=["cx", "u3"])
        return deepcopy(self._circuit)

    def num_auxiliary_qubits(self):
        """Return number of auxiliary qubits

        :return: number of auxiliary qubits
        :rtype: int
        """
        return 0
