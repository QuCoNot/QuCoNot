import numpy as np
import pytest
from functions import usim  # ket_0_matrix,
from functions_testing import (
    generate_circuit_clean_ancilla,
    generate_circuit_clean_relative_ancilla,
    generate_circuit_clean_wasted_entangled_ancilla,
    generate_circuit_clean_wasted_relative_entangled_ancilla,
    generate_circuit_clean_wasted_relative_separable_ancilla,
    generate_circuit_clean_wasted_separable_ancilla,
)

from qumcat.implementations.mct_barenco_75_dirty import MCTBarenco75Dirty

implementation = MCTBarenco75Dirty


@pytest.mark.parametrize("controls_no", [5])
def test_unitary_matrix(controls_no):
    mct = implementation(controls_no)

    circ = mct.generate_circuit()

    function_testing_list = [
        generate_circuit_clean_ancilla,
        generate_circuit_clean_relative_ancilla,
        # generate_circuit_clean_wasted_entangled_ancilla,
        # generate_circuit_clean_wasted_relative_entangled_ancilla,
        # generate_circuit_clean_wasted_relative_separable_ancilla,
        # generate_circuit_clean_wasted_separable_ancilla,
    ]

    # get unitary matrix
    unitary_matrix = np.array(np.absolute(usim.run(circ).result().get_unitary()))

    for function_testing in function_testing_list:
        function_testing(unitary_matrix, controls_no, mct.num_ancilla_qubits())
