import numpy as np
import pytest
from functions import usim
from functions_testing import (
    generate_circuit_clean_ancilla,
    generate_circuit_clean_relative_ancilla,
    generate_circuit_clean_wasted_entangled_ancilla,
    generate_circuit_clean_wasted_relative_entangled_ancilla,
    generate_circuit_clean_wasted_relative_separable_ancilla,
    generate_circuit_clean_wasted_separable_ancilla,
)

from qumcat.implementations.mct_recursion import MCTRecursion

implementation = MCTRecursion


@pytest.mark.parametrize("controls_no", [5])
@pytest.mark.parametrize(
    "function_testing",
    [
        generate_circuit_clean_ancilla,
        generate_circuit_clean_relative_ancilla,
        generate_circuit_clean_wasted_entangled_ancilla,
        generate_circuit_clean_wasted_relative_entangled_ancilla,
        generate_circuit_clean_wasted_separable_ancilla,
        generate_circuit_clean_wasted_relative_separable_ancilla,
    ],
)
def test_mct_recursion(controls_no, function_testing):
    mct = implementation(controls_no)

    circ = mct.generate_circuit()

    # get unitary matrix
    unitary_matrix = np.array(np.absolute(usim.run(circ).result().get_unitary()))

    function_testing(unitary_matrix, controls_no, mct.num_ancilla_qubits())
