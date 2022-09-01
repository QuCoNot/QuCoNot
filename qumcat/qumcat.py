from typing import List

from implementations.mct_n_qubit_decomposition import MCTNQubitDecomposition
from implementations.mct_no_ancilla import MCTNoAncilla
from implementations.mct_no_ancilla_relative_phase import MCTNoAncillaRelativePhase
from implementations.mct_parallel_decomposition import MCTParallelDecomposition
from implementations.mct_vchain import MCTVChain
from qiskit import QuantumCircuit


class Qumcat:

    circuits: List[QuantumCircuit] = []

    def __init__(self, controls_no: int, ancillas_no: int) -> None:
        assert controls_no >= 2, "Need at least 2 controls qubit to process"

        self.controls_no = controls_no
        self.ancillas_no = ancillas_no

        pass

    @classmethod
    def generate_mct_cases(cls, controls_no: int, max_ancilla: int, **kwargs):
        """Generate all possible MCT implementation satisfying the requirements

        :return: Quantum circuits
        :rtype: QuantumCircuit[]
        """
        res = cls(controls_no, max_ancilla)

        # no_ancilla
        no_ancilla = MCTNoAncilla(controls_no)
        res.circuits.append(no_ancilla.generate_circuit())

        if controls_no < 3:
            no_ancilla_relative = MCTNoAncillaRelativePhase(controls_no)
            res.circuits.append(no_ancilla_relative.generate_circuit())

        if max_ancilla > 0:
            # clean_ancilla
            if controls_no > 4:
                n_qubit = MCTNQubitDecomposition(controls_no)
                res.circuits.append(n_qubit.generate_circuit())

                parallel = MCTParallelDecomposition(controls_no)
                res.circuits.append(parallel.generate_circuit())

            vchain = MCTVChain(controls_no)
            res.circuits.append(vchain.generate_circuit())

        return res

    @classmethod
    def make_mct(
        cls,
        controls_no: int,
        ancillas_no: int,
        optimise: str = "cnot",
    ) -> QuantumCircuit:

        return QuantumCircuit(3)
