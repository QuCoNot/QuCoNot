# This is where we put fixtures
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info.operators import Operator
from scipy.sparse import identity

# constants
absolute_error_tol = 1e-8
relative_error_tol = 1e-8


def identity_matrix(qubits_no):
    # return np.identity(2**qubits_no, dtype=complex)
    return identity(2**qubits_no).toarray()


def zero_matrix(qubits_no):
    return np.zeros((2**qubits_no, 2**qubits_no), dtype=complex)


def ket0(dim: int):
    ket_0 = np.zeros(dim)
    ket_0[0] = 1.0
    return ket_0


def ket_0_matrix(qubits_no):
    ket_0 = np.array([1, 0])

    res = ket_0

    if qubits_no > 1:
        for i in range(1, qubits_no):
            res = np.kron(ket_0, res)

    return res


def mct_inverse(method, controls_no, auxiliaries_no):
    qc = QuantumCircuit(controls_no + auxiliaries_no + 1)
    qc.mct(
        list(range(controls_no)),
        controls_no,
        ancilla_qubits=list(range(controls_no + 1, controls_no + 1 + auxiliaries_no)),
        mode=method,
    )
    qc = transpile(qc, basis_gates=["cx", "u3"])

    matrix = Operator(qc).data

    # return np.conjugate(matrix).transpose()
    return np.linalg.inv(matrix)


def load_matrix(mode, controls_no):
    container = np.load("./tests/mct_matrices/mct_" + mode + ".npz")
    return container["arr_" + str(controls_no - 1)]


def check_all_zero(matrix, rtol, atol):
    for i in matrix:
        for j in i:
            if np.absolute(j - 0) > (atol + rtol * np.absolute(0)):
                # print("i :", i, ", j: ", j, ", val: ", np.absolute(j - 0))

                return 0

    return 1
