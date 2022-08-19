from typing import List

from qiskit import QuantumCircuit


class MCTBase:
    def __init__(self, controls_no: int, **kwargs) -> None:
        assert controls_no >= 2
        self._n = controls_no
        self._circuit: QuantumCircuit = None
        pass

    @classmethod
    def generate_mct_cases(self, controls_no: int, max_ancilla: int, **kwargs) -> List["MCTBase"]:
        """Generate all possible MCT implementation satisfying the requirements

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
        if not self._circuit:
            self._circuit = self.generate_circuit()
        ops: dict = self._circuit.count_ops()
        ops.pop("barrier", None)  # TODO verify
        ops.pop("measure", None)  # TODO verify
        # TODO: implement restriction to gates_id
        return sum(ops.values())

    def depth(self) -> int:
        if not self._circuit:
            self._circuit = self.generate_circuit()
        return self._circuit.depth()

    def num_ancilla_qubits(self) -> int:
        if not self._circuit:
            self._circuit = self.generate_circuit()
        return self._circuit.num_qubits() - self._n
