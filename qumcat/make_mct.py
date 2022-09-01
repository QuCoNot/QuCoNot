# import sys

# from qiskit import QuantumCircuit

from qumcat import Qumcat

if __name__ == "__main__":

    mct = Qumcat.make_mct(controls_no=5, ancillas_no=3, optimise="cnot")
