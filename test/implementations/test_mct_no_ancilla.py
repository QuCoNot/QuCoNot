import numpy as np
import pytest
from functions import usim
from functions_testing import generate_circuit_no_ancilla

from qumcat.implementations.mct_no_ancilla import MCTNoAncilla

implementation = MCTNoAncilla


@pytest.mark.parametrize("controls_no", [10])
def test_unitary_matrix(controls_no):
    mct = implementation(controls_no)

    circ = mct.generate_circuit()

    function_testing_list = [
        generate_circuit_no_ancilla,
    ]

    # get unitary matrix
    unitary_matrix = np.array(np.absolute(usim.run(circ).result().get_unitary()))

    for function_testing in function_testing_list:
        function_testing(unitary_matrix, controls_no, mct.num_ancilla_qubits())
