from copy import deepcopy

from qiskit import QuantumCircuit, transpile

from qumcat.mct_base import MCTBase


class MCTNoAncilla(MCTBase):
    def __init__(self, controls_no: int, **kwargs) -> None:
        assert controls_no >= 2
        self._n = controls_no
        self._circuit: QuantumCircuit = None
        pass

    def generate_circuit(self) -> QuantumCircuit:
        """Return a QuantumCircuit implementation

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """
        qc = QuantumCircuit(self._n + 1)
        qc.mct(
            list(range(self._n)),
            self._n,
            mode="noancilla",
        )

        # should be done for all implementations
        # TODO: solve issue with reordered qubits
        self._circuit = transpile(qc, basis_gates=["cx", "u3"])
        return deepcopy(self._circuit)

    def num_ancilla_qubits(self):
        return 0


if __name__ == "__main__":
    mct = MCTNoAncilla(4)

    circ = mct.generate_circuit()
    # print(circ.draw())
