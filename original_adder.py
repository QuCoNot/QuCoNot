from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

qreg_q = QuantumRegister(24, "q")
creg_c = ClassicalRegister(24, "c")
circuit = QuantumCircuit(qreg_q, creg_c)

circuit.x(qreg_q[0])
circuit.x(qreg_q[1])
circuit.x(qreg_q[3])
circuit.x(qreg_q[2])
circuit.barrier(qreg_q)
circuit.ccx(qreg_q[18], qreg_q[19], qreg_q[22])
circuit.ccx(qreg_q[11], qreg_q[12], qreg_q[15])
circuit.ccx(qreg_q[0], qreg_q[1], qreg_q[4])
circuit.ccx(qreg_q[5], qreg_q[6], qreg_q[9])
circuit.cx(qreg_q[22], qreg_q[21])
circuit.cx(qreg_q[15], qreg_q[14])
circuit.cx(qreg_q[4], qreg_q[3])
circuit.cx(qreg_q[9], qreg_q[8])
circuit.cx(qreg_q[22], qreg_q[20])
circuit.cx(qreg_q[15], qreg_q[13])
circuit.cx(qreg_q[4], qreg_q[2])
circuit.cx(qreg_q[9], qreg_q[7])
circuit.ccx(qreg_q[20], qreg_q[21], qreg_q[22])
circuit.ccx(qreg_q[13], qreg_q[14], qreg_q[15])
circuit.ccx(qreg_q[2], qreg_q[3], qreg_q[4])
circuit.ccx(qreg_q[7], qreg_q[8], qreg_q[9])
circuit.ccx(qreg_q[18], qreg_q[19], qreg_q[21])
circuit.ccx(qreg_q[11], qreg_q[12], qreg_q[14])
circuit.ccx(qreg_q[0], qreg_q[1], qreg_q[3])
circuit.ccx(qreg_q[5], qreg_q[6], qreg_q[8])
circuit.ccx(qreg_q[18], qreg_q[19], qreg_q[20])
circuit.ccx(qreg_q[11], qreg_q[12], qreg_q[13])
circuit.ccx(qreg_q[0], qreg_q[1], qreg_q[2])
circuit.ccx(qreg_q[5], qreg_q[6], qreg_q[7])
circuit.cx(qreg_q[18], qreg_q[19])
circuit.cx(qreg_q[20], qreg_q[21])
circuit.cx(qreg_q[11], qreg_q[12])
circuit.cx(qreg_q[13], qreg_q[14])
circuit.cx(qreg_q[5], qreg_q[6])
circuit.cx(qreg_q[7], qreg_q[8])
circuit.ccx(qreg_q[19], qreg_q[21], qreg_q[23])
circuit.ccx(qreg_q[12], qreg_q[14], qreg_q[16])
circuit.ccx(qreg_q[6], qreg_q[8], qreg_q[10])
circuit.barrier(
    qreg_q[0],
    qreg_q[1],
    qreg_q[2],
    qreg_q[3],
    qreg_q[4],
    qreg_q[5],
    qreg_q[6],
    qreg_q[7],
    qreg_q[8],
    qreg_q[9],
    qreg_q[10],
    qreg_q[11],
    qreg_q[12],
    qreg_q[13],
    qreg_q[14],
    qreg_q[15],
    qreg_q[16],
    qreg_q[17],
    qreg_q[18],
    qreg_q[19],
    qreg_q[20],
    qreg_q[21],
    qreg_q[22],
    qreg_q[23],
)
circuit.ccx(qreg_q[3], qreg_q[9], qreg_q[8])
circuit.ccx(qreg_q[16], qreg_q[23], qreg_q[17])
circuit.ccx(qreg_q[15], qreg_q[23], qreg_q[22])
circuit.ccx(qreg_q[8], qreg_q[17], qreg_q[22])
circuit.ccx(qreg_q[8], qreg_q[16], qreg_q[15])
circuit.ccx(qreg_q[16], qreg_q[23], qreg_q[17])
circuit.barrier(
    qreg_q[0],
    qreg_q[1],
    qreg_q[2],
    qreg_q[3],
    qreg_q[4],
    qreg_q[5],
    qreg_q[6],
    qreg_q[7],
    qreg_q[8],
    qreg_q[9],
    qreg_q[10],
    qreg_q[11],
    qreg_q[12],
    qreg_q[13],
    qreg_q[14],
    qreg_q[15],
    qreg_q[16],
    qreg_q[17],
    qreg_q[18],
    qreg_q[19],
    qreg_q[20],
    qreg_q[21],
    qreg_q[22],
    qreg_q[23],
)
circuit.ccx(qreg_q[19], qreg_q[21], qreg_q[23])
circuit.ccx(qreg_q[6], qreg_q[8], qreg_q[10])
circuit.ccx(qreg_q[12], qreg_q[14], qreg_q[16])
circuit.cx(qreg_q[18], qreg_q[19])
circuit.cx(qreg_q[20], qreg_q[21])
circuit.cx(qreg_q[11], qreg_q[12])
circuit.cx(qreg_q[13], qreg_q[14])
circuit.cx(qreg_q[5], qreg_q[6])
circuit.cx(qreg_q[7], qreg_q[8])
circuit.cx(qreg_q[21], qreg_q[18])
circuit.cx(qreg_q[14], qreg_q[11])
circuit.cx(qreg_q[8], qreg_q[5])
circuit.cx(qreg_q[21], qreg_q[19])
circuit.cx(qreg_q[14], qreg_q[12])
circuit.cx(qreg_q[8], qreg_q[6])
circuit.cx(qreg_q[4], qreg_q[8])
circuit.cx(qreg_q[9], qreg_q[14])
circuit.cx(qreg_q[15], qreg_q[21])
circuit.cx(qreg_q[8], qreg_q[6])
circuit.cx(qreg_q[14], qreg_q[12])
circuit.cx(qreg_q[21], qreg_q[19])
circuit.cx(qreg_q[8], qreg_q[5])
circuit.cx(qreg_q[14], qreg_q[11])
circuit.cx(qreg_q[21], qreg_q[18])
circuit.barrier(
    qreg_q[0],
    qreg_q[1],
    qreg_q[2],
    qreg_q[3],
    qreg_q[4],
    qreg_q[5],
    qreg_q[6],
    qreg_q[7],
    qreg_q[8],
    qreg_q[9],
    qreg_q[10],
    qreg_q[11],
    qreg_q[12],
    qreg_q[13],
    qreg_q[14],
    qreg_q[15],
    qreg_q[16],
    qreg_q[17],
    qreg_q[18],
    qreg_q[19],
    qreg_q[20],
    qreg_q[21],
    qreg_q[22],
    qreg_q[23],
)
circuit.ccx(qreg_q[0], qreg_q[1], qreg_q[3])
circuit.ccx(qreg_q[5], qreg_q[6], qreg_q[8])
circuit.ccx(qreg_q[11], qreg_q[12], qreg_q[14])
circuit.ccx(qreg_q[18], qreg_q[19], qreg_q[21])
circuit.cx(qreg_q[4], qreg_q[5])
circuit.cx(qreg_q[9], qreg_q[11])
circuit.cx(qreg_q[15], qreg_q[18])
circuit.barrier(
    qreg_q[0],
    qreg_q[1],
    qreg_q[2],
    qreg_q[3],
    qreg_q[4],
    qreg_q[5],
    qreg_q[6],
    qreg_q[7],
    qreg_q[8],
    qreg_q[9],
    qreg_q[10],
    qreg_q[11],
    qreg_q[12],
    qreg_q[13],
    qreg_q[14],
    qreg_q[15],
    qreg_q[16],
    qreg_q[17],
    qreg_q[18],
    qreg_q[19],
    qreg_q[20],
    qreg_q[21],
    qreg_q[22],
    qreg_q[23],
)
circuit.cx(qreg_q[0], qreg_q[1])
circuit.cx(qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[5], qreg_q[6])
circuit.cx(qreg_q[7], qreg_q[8])
circuit.cx(qreg_q[11], qreg_q[12])
circuit.cx(qreg_q[13], qreg_q[14])
circuit.cx(qreg_q[18], qreg_q[19])
circuit.cx(qreg_q[20], qreg_q[21])
circuit.x(qreg_q[1])
circuit.x(qreg_q[3])
circuit.x(qreg_q[6])
circuit.x(qreg_q[8])
circuit.x(qreg_q[12])
circuit.x(qreg_q[14])
circuit.cx(qreg_q[5], qreg_q[6])
circuit.cx(qreg_q[7], qreg_q[8])
circuit.cx(qreg_q[11], qreg_q[12])
circuit.cx(qreg_q[13], qreg_q[14])
circuit.ccx(qreg_q[12], qreg_q[14], qreg_q[16])
circuit.ccx(qreg_q[6], qreg_q[8], qreg_q[10])
circuit.ccx(qreg_q[9], qreg_q[16], qreg_q[15])
circuit.ccx(qreg_q[4], qreg_q[10], qreg_q[9])
circuit.ccx(qreg_q[12], qreg_q[14], qreg_q[16])
circuit.ccx(qreg_q[6], qreg_q[8], qreg_q[10])
circuit.cx(qreg_q[11], qreg_q[12])
circuit.cx(qreg_q[13], qreg_q[14])
circuit.cx(qreg_q[5], qreg_q[6])
circuit.cx(qreg_q[7], qreg_q[8])
circuit.barrier(
    qreg_q[0],
    qreg_q[1],
    qreg_q[2],
    qreg_q[3],
    qreg_q[4],
    qreg_q[5],
    qreg_q[6],
    qreg_q[7],
    qreg_q[8],
    qreg_q[9],
    qreg_q[10],
    qreg_q[11],
    qreg_q[12],
    qreg_q[13],
    qreg_q[14],
    qreg_q[15],
    qreg_q[16],
    qreg_q[17],
    qreg_q[18],
    qreg_q[19],
    qreg_q[20],
    qreg_q[21],
    qreg_q[22],
    qreg_q[23],
)
circuit.ccx(qreg_q[11], qreg_q[12], qreg_q[13])
circuit.ccx(qreg_q[11], qreg_q[12], qreg_q[14])
circuit.ccx(qreg_q[13], qreg_q[14], qreg_q[15])
circuit.cx(qreg_q[15], qreg_q[13])
circuit.cx(qreg_q[15], qreg_q[14])
circuit.ccx(qreg_q[11], qreg_q[12], qreg_q[15])
circuit.x(qreg_q[12])
circuit.x(qreg_q[14])
circuit.ccx(qreg_q[5], qreg_q[6], qreg_q[7])
circuit.ccx(qreg_q[0], qreg_q[1], qreg_q[2])
circuit.ccx(qreg_q[5], qreg_q[6], qreg_q[8])
circuit.ccx(qreg_q[0], qreg_q[1], qreg_q[3])
circuit.ccx(qreg_q[7], qreg_q[8], qreg_q[9])
circuit.ccx(qreg_q[2], qreg_q[3], qreg_q[4])
circuit.cx(qreg_q[9], qreg_q[7])
circuit.cx(qreg_q[4], qreg_q[2])
circuit.cx(qreg_q[9], qreg_q[8])
circuit.ccx(qreg_q[5], qreg_q[6], qreg_q[9])
circuit.x(qreg_q[6])
circuit.x(qreg_q[8])
circuit.cx(qreg_q[4], qreg_q[3])
circuit.ccx(qreg_q[0], qreg_q[1], qreg_q[4])
circuit.x(qreg_q[1])
circuit.x(qreg_q[3])

circuit.draw(output="mpl", filename="adder_original.png")
