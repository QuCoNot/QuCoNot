OPENQASM 2.0;
include "qelib1.inc";

gate relative_Toffoli q0, q1, q2 {
  h q2;
t q2;
cx q1, q2;
tdg q2;
cx q0, q2;
t q2;
cx q1, q2;
tdg q2;
h q2;
}

gate rcccx q0, q1, q2, q3 {
  h q3;
t q3;
cx q2, q3;
tdg q3;
h q3;
cx q0, q3;
t q3;
cx q1,q3;
tdg q3;
cx q0,q3;
t q3;
cx  q1,q3;
tdg q3;
h q3;
t q3;
cx q2, q3;
tdg q3;
h q3;
}


qreg q[52];
creg c[52];
relative_Toffoli q[0], q[1], q[2];
relative_Toffoli q[3], q[4], q[5];
relative_Toffoli q[6], q[7], q[8];
relative_Toffoli q[10], q[11], q[12];
relative_Toffoli q[13], q[14], q[15];
relative_Toffoli q[16], q[17], q[18];
relative_Toffoli q[21], q[22], q[23];
relative_Toffoli q[24], q[25], q[26];
relative_Toffoli q[27], q[28], q[29];
relative_Toffoli q[32], q[33], q[34];
relative_Toffoli q[35], q[36], q[37];
relative_Toffoli q[38], q[39], q[40];
cx q[0], q[1];
cx q[3], q[4];
cx q[6], q[7];
cx q[10], q[11];
cx q[13], q[14];
cx q[16], q[17];
cx q[21], q[22];
cx q[24], q[25];
cx q[27], q[28];
cx q[32], q[33];
cx q[35], q[36];
cx q[38], q[39];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16], q[17], q[18], q[19], q[20], q[21], q[22], q[23], q[24], q[25], q[26], q[27], q[28], q[29], q[30], q[31], q[32], q[33], q[34], q[35], q[36], q[37], q[38], q[39], q[40], q[41], q[42], q[43], q[44], q[45], q[46], q[47], q[48], q[49];


rcccx q[33], q[36], q[39], q[41];
rcccx q[22], q[25], q[28], q[30];
rcccx q[11], q[14], q[17], q[19];
rcccx q[1], q[4], q[7], q[9];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16], q[17], q[18], q[19], q[20], q[21], q[22], q[23], q[24], q[25], q[26], q[27], q[28], q[29], q[30], q[31], q[32], q[33], q[34], q[35], q[36], q[37], q[38], q[39], q[40], q[41], q[42], q[43], q[44], q[45], q[46], q[47], q[48], q[49];
relative_Toffoli q[2], q[4], q[5];
relative_Toffoli q[34], q[36], q[37];
relative_Toffoli q[23], q[25], q[26];
relative_Toffoli q[12], q[14], q[15];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16], q[17], q[18], q[19], q[20], q[21], q[22], q[23], q[24], q[25], q[26], q[27], q[28], q[29], q[30], q[31], q[32], q[33], q[34], q[35], q[36], q[37], q[38], q[39], q[40], q[41], q[42], q[43], q[44], q[45], q[46], q[47], q[48], q[49];
relative_Toffoli q[5], q[7], q[8];
relative_Toffoli q[15], q[17], q[18];
relative_Toffoli q[26], q[28], q[29];
relative_Toffoli q[37], q[39], q[40];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16], q[17], q[18], q[19], q[20], q[21], q[22], q[23], q[24], q[25], q[26], q[27], q[28], q[29], q[30], q[31], q[32], q[33], q[34], q[35], q[36], q[37], q[38], q[39], q[40], q[41], q[42], q[43], q[44], q[45], q[46], q[47], q[48], q[49];
relative_Toffoli q[9], q[19], q[20];
relative_Toffoli q[30], q[41], q[42];
relative_Toffoli q[8], q[19], q[18];
relative_Toffoli q[20], q[42], q[43];
relative_Toffoli q[29], q[41], q[40];
relative_Toffoli q[18], q[40], q[42];
relative_Toffoli q[20], q[30], q[31];
relative_Toffoli q[18], q[30], q[29];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16], q[17], q[18], q[19], q[20], q[21], q[22], q[23], q[24], q[25], q[26], q[27], q[28], q[29], q[30], q[31], q[32], q[33], q[34], q[35], q[36], q[37], q[38], q[39], q[40], q[41], q[42], q[43], q[44], q[45], q[46], q[47], q[48], q[49];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16], q[17], q[18], q[19], q[20], q[21], q[22], q[23], q[24], q[25], q[26], q[27], q[28], q[29], q[30], q[31], q[32], q[33], q[34], q[35], q[36], q[37], q[38], q[39], q[40], q[41], q[42], q[43], q[44], q[45], q[46], q[47], q[48], q[49];
reset q[5];
reset q[15];
reset q[26];
reset q[37];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16], q[17], q[18], q[19], q[20], q[21], q[22], q[23], q[24], q[25], q[26], q[27], q[28], q[29], q[30], q[31], q[32], q[33], q[34], q[35], q[36], q[37], q[38], q[39], q[40], q[41], q[42], q[43], q[44], q[45], q[46], q[47], q[48], q[49], q[50], q[51];
cx q[0], q[1];
cx q[3], q[4];
cx q[6], q[7];
cx q[10], q[11];
cx q[13], q[14];
cx q[16], q[17];
cx q[21], q[22];
cx q[24], q[25];
cx q[27], q[28];
cx q[32], q[33];
cx q[35], q[36];
cx q[38], q[39];
cx q[40], q[44];
relative_Toffoli q[0], q[1], q[2];
relative_Toffoli q[9], q[10], q[11];
relative_Toffoli q[21], q[22], q[23];
relative_Toffoli q[32], q[33], q[34];
cx q[40], q[45];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16], q[17], q[18], q[19], q[20], q[21], q[22], q[23], q[24], q[25], q[26], q[27], q[28], q[29], q[30], q[31], q[32], q[33], q[34], q[35], q[36], q[37], q[38], q[39], q[40], q[41], q[42], q[43], q[44], q[45], q[46], q[47], q[48], q[49], q[50], q[51];
cx q[29], q[32];
cx q[18], q[21];
cx q[8], q[10];
relative_Toffoli q[0], q[1], q[2];
cx q[29], q[33];
cx q[8], q[11];
cx q[18], q[22];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16], q[17], q[18], q[19], q[20], q[21], q[22], q[23], q[24], q[25], q[26], q[27], q[28], q[29], q[30], q[31], q[32], q[33], q[34], q[35], q[36], q[37], q[38], q[39], q[40], q[41], q[42], q[43], q[44], q[45], q[46], q[47], q[48], q[49], q[50], q[51];
relative_Toffoli q[10], q[11], q[12];
relative_Toffoli q[21], q[22], q[23];
relative_Toffoli q[32], q[33], q[34];
relative_Toffoli q[44], q[45], q[46];
cx q[8], q[12];
cx q[18], q[23];
cx q[29], q[34];
cx q[40], q[46];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16], q[17], q[18], q[19], q[20], q[21], q[22], q[23], q[24], q[25], q[26], q[27], q[28], q[29], q[30], q[31], q[32], q[33], q[34], q[35], q[36], q[37], q[38], q[39], q[40], q[41], q[42], q[43], q[44], q[45], q[46], q[47], q[48], q[49], q[50], q[51];
cx q[46], q[47];
cx q[46], q[48];
relative_Toffoli q[47], q[48], q[49];
cx q[46], q[49];
cx q[49], q[51];
cx q[34], q[35];
cx q[23], q[24];
cx q[12], q[13];
cx q[2], q[3];
cx q[34], q[36];
cx q[23], q[25];
cx q[12], q[14];
cx q[2], q[4];
relative_Toffoli q[35], q[36], q[37];
relative_Toffoli q[24], q[25], q[26];
relative_Toffoli q[13], q[14], q[15];
relative_Toffoli q[3], q[4], q[5];
cx q[34], q[37];
cx q[23], q[26];
cx q[12], q[15];
cx q[2], q[5];
cx q[37], q[39];
cx q[26], q[28];
cx q[15], q[17];
cx q[5], q[7];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16], q[17], q[18], q[19], q[20], q[21], q[22], q[23], q[24], q[25], q[26], q[27], q[28], q[29], q[30], q[31], q[32], q[33], q[34], q[35], q[36], q[37], q[38], q[39], q[40], q[41], q[42], q[43], q[44], q[45], q[46], q[47], q[48], q[49], q[50], q[51];
cx q[8], q[10];
cx q[18], q[21];
cx q[29], q[32];
cx q[40], q[44];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16], q[17], q[18], q[19], q[20], q[21], q[22], q[23], q[24], q[25], q[26], q[27], q[28], q[29], q[30], q[31], q[32], q[33], q[34], q[35], q[36], q[37], q[38], q[39], q[40], q[41], q[42], q[43], q[44], q[45], q[46], q[47], q[48], q[49], q[50], q[51];
cx q[0], q[1];
cx q[6], q[7];
cx q[10], q[11];
cx q[13], q[14];
cx q[16], q[17];
cx q[21], q[22];
cx q[24], q[25];
cx q[27], q[28];
cx q[32], q[33];
cx q[35], q[36];
cx q[38], q[39];
cx q[44], q[45];
cx q[47], q[48];
cx q[50], q[51];
cx q[3], q[4];
