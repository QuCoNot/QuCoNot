from typing import List

from qiskit import QuantumCircuit


class MCTBase:
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
        separable_wasted_auxiliary: true / false (D), requires wasted_auxiliary set to True

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """
        raise NotImplementedError

    def generate_circuit(self) -> QuantumCircuit:
        """Return a QuantumCircuit implementation

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """
        raise NotImplementedError

    def num_gates(self, gates_id: List[str] = None) -> int:
        """Return number of gates

        :return: number of gates
        :rtype: int
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

        :return: number of depth
        :rtype: int
        """
        if not self._circuit:
            self._circuit = self.generate_circuit()
        return self._circuit.depth()

    def num_auxiliary_qubits(self) -> int:
        """Return number of auxiliary qubits

        :return: number of auxiliary qubits
        :rtype: int
        """
        if not self._circuit:
            self._circuit = self.generate_circuit()
        return self._circuit.num_qubits() - self._n
