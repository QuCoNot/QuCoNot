import sys

from qumcat import Qumcat

sys.path.append("C:\\Github\\qumcat")


q = Qumcat()
print(q._registered_methods)
q.generate_mct_cases(5, 3)

for imp in q._implementations:
    circ = imp.generate_circuit()
    print(circ.count_ops())
