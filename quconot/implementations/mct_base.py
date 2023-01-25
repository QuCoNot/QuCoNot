from typing import List

from qiskit import QuantumCircuit


class MCTBase:
    r"""
    Base class for all implementations Circuit depth, number of auxiliary qubits and number of gates used are
    important parameters while considering CNOT gate use.
    """

    def __init__(self, controls_no: int, **kwargs) -> None:
        if controls_no < 2:
            raise ValueError("Number of controls must be >= 2 for this implementation")
        self._n = controls_no
        self._circuit: QuantumCircuit = None

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
        r"""Generate all possible MCT implementation satisfying the requirements

        relative_phase: true / false (D)
        clean_auxiliary: true (D) / false
        wasted_auxiliary: true / false (D)
        separable_wasted_auxiliary: true / false (D), requires wasted_auxiliary set to True

        Returns:
            List: List of decompositions available

        **Example**
            >>> MCTNoAuxiliaryRelativePhase(2).verify_mct_cases(controls_no = 6, max_auxiliary = 0)
            #Raises error as ``MCTNoAuxiliaryRelativePhase`` does not support more than 3 control qubits

            >>> MCTNoAuxiliary(2).verify_mct_cases(3,0)
            [<__main__.MCTNoAuxiliary at 0x7fa7415c47f0>]
        """
        raise NotImplementedError

    def generate_circuit(self) -> QuantumCircuit:
        """Return a QuantumCircuit implementation

        Returns:
            QuantumCircuit: quantum circuit
        **Example**
            >>> MCTNoAuxiliaryRelativePhase(2).generate_circuit().draw()
            q_0: ─────────────────────────────────────────■────────────────────────────────────────
                                                          │
            q_1: ────────────────────■────────────────────┼───────────────────■────────────────────
                 ┌────────────────┐┌─┴─┐┌──────────────┐┌─┴─┐┌─────────────┐┌─┴─┐┌────────────────┐
            q_2: ┤ U3(π/2,π/4,-π) ├┤ X ├┤ U3(0,0,-π/4) ├┤ X ├┤ U3(0,0,π/4) ├┤ X ├┤ U3(π/2,0,3π/4) ├
                 └────────────────┘└───┘└──────────────┘└───┘└─────────────┘└───┘└────────────────┘

        """
        raise NotImplementedError

    def num_gates(self, gates_id: List[str] = None) -> int:
        """Return number of gates used in implementation

        Returns:
            int: number of gates
        **Example**
            >>> MCTParallelDecomposition(8).num_gates()
            195
        """
        if not self._circuit:
            self._circuit = self.generate_circuit()
        ops: dict = self._circuit.count_ops()
        ops.pop("barrier", None)  # TODO verify
        ops.pop("measure", None)  # TODO verify
        # TODO: implement restriction to gates_id
        return sum(ops.values())

    def depth(self) -> int:
        """Return number of circuit depth

        Returns:
            int: circuit depth
        **Example**
            >>> MCTBarenco75Dirty(2).depth()
            35

        """
        if not self._circuit:
            self._circuit = self.generate_circuit()
        return self._circuit.depth()

    def num_auxiliary_qubits(self) -> int:
        """Return number of auxiliary qubits used in implementation

        Returns:
            int: number of auxiliary qubits
        **Example**
            >>> MCTBarenco74Dirty(2).num_auxiliary_qubits()
            0
        """
        if not self._circuit:
            self._circuit = self.generate_circuit()
        return self._circuit.num_qubits() - self._n
