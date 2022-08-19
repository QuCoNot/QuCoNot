# This is where we put fixtures
import numpy as np
from qiskit import Aer, QuantumCircuit, transpile


def identity_matrix(qubits_no):
    return np.identity(2**qubits_no, dtype=complex)


def zero_matrix(qubits_no):
    return np.zeros((2**qubits_no, 2**qubits_no), dtype=complex)


def mct_inverse(method, controls_no, ancillas_no):
    qc = QuantumCircuit(controls_no + ancillas_no + 1)
    qc.mct(
        list(range(controls_no)),
        controls_no,
        ancilla_qubits=list(range(controls_no + 1, controls_no + 1 + ancillas_no)),
        mode=method,
    )
    qc = transpile(qc, basis_gates=["cx", "u3"])

    usim = Aer.get_backend("unitary_simulator")
    matrix = usim.run(qc).result().get_unitary()

    # return np.conjugate(matrix).transpose()
    return np.linalg.inv(matrix)


def load_matrix(mode, controls_no):

    container = np.load("./Test/mct_matrices/mct_" + mode + ".npz")

    return container["arr_" + str(controls_no - 1)]


def check_all_zero(matrix, rtol, atol):

    for i in matrix:
        for j in i:
            if np.absolute(j - 0) > (atol + rtol * np.absolute(0)):
                return 0

    return 1
