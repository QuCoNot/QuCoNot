import numpy as np
import pytest
from functions import usim
from functions_testing import generate_circuit_no_ancilla, generate_circuit_no_ancilla_relative

from qumcat.implementations.mct_no_ancilla_relative_phase import MCTNoAncillaRelativePhase

implementation = MCTNoAncillaRelativePhase


@pytest.mark.parametrize("controls_no", [3])
@pytest.mark.parametrize(
    "function_testing",
    [
        # generate_circuit_no_ancilla,
        generate_circuit_no_ancilla_relative,
    ],
)
def test_mct_no_ancilla_relative_phase(controls_no, function_testing):
    mct = implementation(controls_no)

    circ = mct.generate_circuit()

    # get unitary matrix
    unitary_matrix = np.array(np.absolute(usim.run(circ).result().get_unitary()))

    function_testing(unitary_matrix, controls_no, mct.num_ancilla_qubits())
