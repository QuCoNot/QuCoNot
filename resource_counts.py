import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import CCXGate
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("ticks")


def RTofDecomp():
    '''
    Creates a relative Toffoli gate as described in Section VI B of Barenco et al.
    The Ry gate in the paper is defined differently from the usual convention.
    Ry (from paper) = Ry†
    '''
    qc = QuantumCircuit(3, name='RTOF')
    qc.h(2)
    qc.t(2)
    qc.cx(1, 2)
    qc.tdg(2)
    qc.cx(0, 2)
    qc.t(2)
    qc.cx(1, 2)
    qc.tdg(2)
    qc.h(2)
    return qc


def fig2(n):
    controls = list(range(n))
    target = n + n - 2
    auxs = list(range(n, n + n - 2))

    qc = QuantumCircuit(n + n - 1)

    for c1, c2, t in zip(controls[::-1][:n - 2], auxs[::-1][:n - 2], [target] + auxs[::-1][:n - 2]):
        qc.append(CCXGate() if t == target else CCXGate(), [c1, c2, t])

    qc.append(CCXGate(), [controls[0], controls[1], auxs[0]])

    for c1, c2, t in zip(controls[2:], auxs, auxs[1:] + [target]):
        qc.append(CCXGate() if t == target else CCXGate(), [c1, c2, t])

    for c1, c2, t in zip(controls[::-1][1:n - 2], auxs[::-1][1:n - 2], auxs[::-1][:n - 2]):
        qc.append(CCXGate(), [c1, c2, t])

    qc.append(CCXGate(), [controls[0], controls[1], auxs[0]])

    for c1, c2, t in zip(controls[2:], auxs, auxs[1:]):
        qc.append(CCXGate(), [c1, c2, t])
    return qc


def fig3(n):
    controls = list(range(n))
    target = n + n - 2
    auxs = list(range(n, n + n - 2))

    qc = QuantumCircuit(n + n - 1)

    for c1, c2, t in zip(controls[::-1][:n - 2], auxs[::-1][:n - 2], [target] + auxs[::-1][:n - 2]):
        qc.append(CCXGate(), [c1, c2, t])

    qc.append(RTofDecomp(), [controls[0], controls[1], auxs[0]])

    for c1, c2, t in zip(controls[2:], auxs, auxs[1:] + [target]):
        qc.append(CCXGate() if t == target else RTofDecomp(), [c1, c2, t])

    for c1, c2, t in zip(controls[::-1][1:n - 2], auxs[::-1][1:n - 2], auxs[::-1][:n - 2]):
        qc.append(CCXGate() if t == target else RTofDecomp(), [c1, c2, t])

    qc.append(RTofDecomp(), [controls[0], controls[1], auxs[0]])

    for c1, c2, t in zip(controls[2:], auxs, auxs[1:]):
        qc.append(CCXGate(), [c1, c2, t])
    return qc


def fig4l(n):
    controls = list(range(n))
    target = n + n - 2
    auxs = list(range(n, n + n - 2))

    qc = QuantumCircuit(n + n - 1)

    for c1, c2, t in zip(controls[::-1][:n - 2], auxs[::-1][:n - 2], [target] + auxs[::-1][:n - 2]):
        qc.append(CCXGate(), [c1, c2, t])

    qc.append(CCXGate(), [controls[0], controls[1], auxs[0]])

    for c1, c2, t in zip(controls[2:], auxs, auxs[1:] + [target]):
        qc.append(CCXGate(), [c1, c2, t])

    return qc


def fig4r(n):
    controls = list(range(n))
    target = n + n - 2
    auxs = list(range(n, n + n - 2))

    qc = QuantumCircuit(n + n - 1)

    qc.append(CCXGate(), [controls[0], controls[1], auxs[0]])

    for c1, c2, t in zip(controls[2:], auxs, auxs[1:] + [target]):
        qc.append(CCXGate(), [c1, c2, t])

    for c1, c2, t in zip(controls[::-1][1:n - 2], auxs[::-1][1:n - 2], auxs[::-1][:n - 2]):
        qc.append(CCXGate(), [c1, c2, t])

    qc.append(CCXGate(), [controls[0], controls[1], auxs[0]])

    return qc


def fig6(n):
    controls = list(range(n))
    target = n + n - 2
    auxs = list(range(n, n + n - 2))

    qc = QuantumCircuit(n + n - 1)

    qc.append(RTofDecomp(), [controls[0], controls[1], auxs[0]])

    for c1, c2, t in zip(controls[2:], auxs, auxs[1:] + [target]):
        qc.append(RTofDecomp() if t == target else RTofDecomp(), [c1, c2, t])

    return qc


def fig7(n: int):
    controls = list(range(n))
    target = n + n - 2
    auxs = list(range(n, n + n - 2))

    qc = QuantumCircuit(n + n - 1)

    for c1, c2, t in zip(controls[::-1][:n - 2], auxs[::-1][:n - 2], [target] + auxs[::-1][:n - 2]):
        qc.append(RTofDecomp(), [c1, c2, t])

    qc.append(RTofDecomp(), [controls[0], controls[1], auxs[0]])

    for c1, c2, t in zip(controls[2:], auxs, auxs[1:] + [target]):
        qc.append(RTofDecomp(), [c1, c2, t])

    return qc


circ_fig2 = fig2(5)
circ_fig2 = transpile(circ_fig2, basis_gates=['cx', 't', 'h', 's', 'tdg', 'sdg'], optimization_level=1)
print('Gate Counts', dict(circ_fig2.count_ops()), 'Circuit Depth', circ_fig2.depth(), 'T Depth',
      circ_fig2.depth(lambda gate: gate[0].name in ['t', 'tdg']))

circ_fig3 = fig3(5)
circ_fig3 = transpile(circ_fig3, basis_gates=['cx', 't', 'h', 's', 'tdg', 'sdg'], optimization_level=1)
print('Gate Counts', dict(circ_fig3.count_ops()), 'Circuit Depth', circ_fig3.depth(), 'T Depth',
      circ_fig3.depth(lambda gate: gate[0].name in ['t', 'tdg']))

circ_fig4l = fig4l(5)
circ_fig4l = transpile(circ_fig4l, basis_gates=['cx', 't', 'h', 's', 'tdg', 'sdg'], optimization_level=1)
print('Gate Counts', dict(circ_fig4l.count_ops()), 'Circuit Depth', circ_fig4l.depth(), 'T Depth',
      circ_fig4l.depth(lambda gate: gate[0].name in ['t', 'tdg']))

circ_fig4r = fig4r(5)
circ_fig4r = transpile(circ_fig4r, basis_gates=['cx', 't', 'h', 's', 'tdg', 'sdg'], optimization_level=1)
print('Gate Counts', dict(circ_fig4r.count_ops()), 'Circuit Depth', circ_fig4r.depth(), 'T Depth',
      circ_fig4r.depth(lambda gate: gate[0].name in ['t', 'tdg']))

circ_fig6 = fig6(5)
circ_fig6 = transpile(circ_fig6, basis_gates=['cx', 't', 'h', 's', 'tdg', 'sdg'], optimization_level=1)
print('Gate Counts', dict(circ_fig6.count_ops()), 'Circuit Depth', circ_fig6.depth(), 'T Depth',
      circ_fig6.depth(lambda gate: gate[0].name in ['t', 'tdg']))

circ_fig7 = fig7(5)
circ_fig7 = transpile(circ_fig7, basis_gates=['cx', 't', 'h', 's', 'tdg', 'sdg'], optimization_level=1)
print('Gate Counts', dict(circ_fig7.count_ops()), 'Circuit Depth', circ_fig7.depth(), 'T Depth',
      circ_fig7.depth(lambda gate: gate[0].name in ['t', 'tdg']))

num_controls = 20
all_tc = []
all_cxc = []
all_depth = []
all_tdepth = []
for n in range(5, num_controls + 1):
    f2 = fig2(n)
    f3 = fig3(n)
    f4l = fig4l(n)
    f4r = fig4r(n)
    f6 = fig6(n)
    f7 = fig7(n)

    t = []
    cx = []
    d = []
    td = []
    for f in [f2, f3, f4l, f4r, f6, f7]:
        f_trans = transpile(f, basis_gates=['cx', 't', 'h', 's', 'tdg', 'sdg'], optimization_level=1)
        counts = f_trans.count_ops()
        t.append(counts['t'] + counts['tdg'])
        cx.append(counts['cx'])
        d.append(f_trans.depth())
        td.append(f_trans.depth(lambda gate: gate[0].name in ['t', 'tdg']))
    all_tc.append(t)
    all_cxc.append(cx)
    all_depth.append(d)
    all_tdepth.append(td)

all_tc = np.asarray(all_tc)
all_cxc = np.asarray(all_cxc)
all_depth = np.asarray(all_depth)
all_tdepth = np.asarray(all_tdepth)

plt.rcParams["figure.figsize"] = (11.7, 4.15)
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Helvetica"
})

ax1 = plt.subplot(1, 2, 1)
plt.plot(range(5, num_controls + 1), all_tc[:, 0], color='C0')
plt.plot(range(5, num_controls + 1), all_tc[:, 1], color='C1', linestyle='dashed')
plt.plot(range(5, num_controls + 1), all_tc[:, 2], color='C2', linestyle='dotted')
plt.plot(range(5, num_controls + 1), all_tc[:, 3], color='C3', linestyle=(0, (5, 10)))
plt.plot(range(5, num_controls + 1), all_tc[:, 4], color='C4', linestyle=(0, (5, 1)))
plt.plot(range(5, num_controls + 1), all_tc[:, 5], color='C5', linestyle='dashdot')

plt.legend(['Fig. 2', 'Fig. 3', 'Fig. 4 (left)', 'Fig. 4 (right)', 'Fig. 6', 'Fig. 7'])
plt.ylabel('$T$ count')
plt.xlabel('Number of control qubits')
# plt.xticks([5, 200, 400, 600, 800, 1000], [5, 200, 400, 600, 800, 1000]) #Ticks for 1000 controls
plt.tight_layout()

ax2 = plt.subplot(1, 2, 2, sharey=ax1)
plt.plot(range(5, num_controls + 1), all_cxc[:, 0], color='C0')
plt.plot(range(5, num_controls + 1), all_cxc[:, 1], color='C1', linestyle='dashed')
plt.plot(range(5, num_controls + 1), all_cxc[:, 2], color='C2', linestyle='dotted')
plt.plot(range(5, num_controls + 1), all_cxc[:, 3], color='C3', linestyle=(0, (5, 10)))
plt.plot(range(5, num_controls + 1), all_cxc[:, 4], color='C4', linestyle=(0, (5, 1)))
plt.plot(range(5, num_controls + 1), all_cxc[:, 5], color='C5', linestyle='dashdot')
plt.legend(['Fig. 2', 'Fig. 3', 'Fig. 4 (left)', 'Fig. 4 (right)', 'Fig. 6', 'Fig. 7'])
plt.ylabel('CNOT count')
plt.xlabel('Number of control qubits')
# plt.xticks([5, 200, 400, 600, 800, 1000], [5, 200, 400, 600, 800, 1000]) #Ticks for 1000 controls
plt.tight_layout()
# plt.savefig(f'counts_{num_controls}.pdf', bbox_inches='tight', dpi=1200, format='pdf')
plt.show()
