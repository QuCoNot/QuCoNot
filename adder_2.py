import qiskit
from qiskit import transpile
from qiskit.transpiler.passes import RemoveBarriers

original = qiskit.circuit.QuantumCircuit.from_qasm_file('original_adder_2.qasm')
print(original.draw(fold=-1))

original = RemoveBarriers()(original)
original = transpile(original, basis_gates=['cx', 't', 'h', 's', 'tdg', 'sdg'], optimization_level=1)
print('Original Gate Counts', dict(original.count_ops()), 'Circuit Depth', original.depth(), 'T Depth',
      original.depth(lambda gate: gate[0].name in ['t', 'tdg']), 'Qubits', original.num_qubits)

modified = qiskit.circuit.QuantumCircuit.from_qasm_file('modified_adder_2.qasm')
print(modified.draw(fold=-1))

modified = RemoveBarriers()(modified)
modified = transpile(modified, basis_gates=['cx', 't', 'h', 's', 'tdg', 'sdg'], optimization_level=1)
print('Modified Gate Counts', dict(modified.count_ops()), 'Circuit Depth', modified.depth(), 'T Depth',
      modified.depth(lambda gate: gate[0].name in ['t', 'tdg']), 'Qubits', modified.num_qubits)
