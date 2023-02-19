# Quconot/quconot/implementations/mct_barenco_75_dirty.py
#
# Authors:
#  - Ankit Khandelwal
#  - Shraddha Aangiras

from copy import deepcopy
from typing import List

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import CCXGate, CXGate, XGate

from .mct_base import MCTBase


class MCTBarenco75Dirty(MCTBase):
    r"""
    **Multi-controlled not implementation using Corollary 7.5 of Barenco et al:**

    For any unitary ``2 × 2 matrix U``, :math:`∧_{n-1}(U)` gate can be simulated by a network of the form:

    .. image:: ../_static/Lemma_75.png
       :width: 400

    (illustrated for ``n = 9``) where V is unitary.

    **Proof:** Let :math:`V` be such that :math:`V^2 = U`. If the any of the first ``n-1`` qubits are ``0`` then
    the transformation applied to the last qubit is either :math:`I` or :math:`V · V^† = I`. If the first ``n-1``
    qubits are all ``1`` then the transformation applied to the last qubit is :math:`V · V = U`

    """

    def __init__(self, controls_no: int, **kwargs) -> None:
        if controls_no < 2:
            raise ValueError("Number of controls must be >= 2 for this implementation")
        self._n = controls_no
        self._circuit: QuantumCircuit = None

    def get_V(self, root: int):
        r"""
        Returns controlled V gate
        :math: `V_{k} = X^{frac{1}{k}}`

        Args:
            root (int): specifies value of k for kth root of Pauli-X

        Returns:
            QuantumCircuit: quantum circuit containing controlled V gate

        **Example**
            >>> print(MCTBarenco75Dirty(controls_no=5).get_V(2))
            q_0: ────■────
                 ┌───┴───┐
            q_1: ┤ x^0.5 ├
                 └───────┘

        """

        circ = QuantumCircuit(2, name=f"CX^1/{root}")
        V = XGate().power(1 / root)
        V = V.control(1)
        circ.append(V, [0, 1])
        return circ

    def get_Vdg(self, root: int):
        r"""
        Returns controlled V adjoint gate

        Args:
            root (int): specifies value of k for the adjoint gate of kth root of Pauli-X

        Returns:
            QuantumCircuit: quantum circuit containing controlled adjoint gate of controlled V gate

        **Example**
            >>> print(MCTBarenco75Dirty(controls_no=5).get_Vdg(2))
            q_0: ─────■─────
                 ┌────┴────┐
            q_1: ┤ Unitary ├
                 └─────────┘

        """

        circ = QuantumCircuit(2, name=f"CX^1/{root}dg")
        V = XGate().power(1 / root).adjoint()
        V = V.control(1)
        circ.append(V, [0, 1])
        return circ

    def get_mct(self, controls: List[int], target: int):
        r"""
        Returns MCT gate

        Args:
            controls (List[int]): specify number of control qubits

        Returns:
            QuantumCircuit: quantum circuit containing required MCT gate

        **Example**
            >>> MCTBarenco75Dirty(controls_no = 5).get_mct([0,1],2)
            Instruction(name='ccx', num_qubits=3, num_clbits=0, params=[])

        """

        if len(controls) == 1:
            return CXGate()
        if len(controls) == 2:
            return CCXGate()
        circ = QuantumCircuit(len(controls) + 1, name="mct")
        # Change with mct implementation
        circ.mcx(controls, target)
        return circ

    def recursive(self, qubits: List[int]):
        r"""
        Uses Lemma 7.5 from Barenco et al to implement :math: `∧_{n-1}(X)` gate

        Args:
            qubits (List[int]): specify number of control qubits

        Returns:
            QuantumCircuit: quantum circuit containing required MCT gate using lemma 7.5

        **Example**
            >>> print(MCTBarenco75Dirty(controls_no = 5).recursive([0,1,2]))
                                                       ┌─────────┐
                q_0: ─────────────■─────────────────■──┤0        ├
                     ┌─────────┐┌─┴─┐┌───────────┐┌─┴─┐│         │
                q_1: ┤0        ├┤ X ├┤0          ├┤ X ├┤  CX^1/2 ├
                     │  CX^1/2 │└───┘│  CX^1/2dg │└───┘│         │
                q_2: ┤1        ├─────┤1          ├─────┤1        ├
                     └─────────┘     └───────────┘     └─────────┘

        """

        circ = QuantumCircuit(len(qubits))

        def make_mct(circ: QuantumCircuit, qubits: List[int], root: int = 1):
            if len(qubits) == 2:
                circ.append(self.get_V(root), qubits)
                return circ

            CV = self.get_V(root * 2)
            CVdg = self.get_Vdg(root * 2)

            mcx = self.get_mct(qubits[:-2], qubits[-2])

            circ.append(CV, [qubits[-2], qubits[-1]])
            circ.append(mcx, qubits[:-1])
            circ.append(CVdg, [qubits[-2], qubits[-1]])
            circ.append(mcx, qubits[:-1])

            ccv = make_mct(circ, qubits[:-2] + [qubits[-1]], root * 2)

            return ccv

        circ = make_mct(circ, qubits, 1)

        return circ

    @classmethod
    def verify_mct_cases(
        self,
        controls_no: int,
        max_auxiliary: int,
        relative_phase: bool = False,
        clean_acilla: bool = True,
        wasted_auxiliary: bool = False,
        separable_wasted_auxiliary: bool = False,
    ) -> List["MCTBase"]:
        """Generate all possible MCT implementation satisfying the requirements

        relative_phase: true / false (D)
        clean_auxiliary: true (D) / false
        wasted_auxiliary: true / false (D)
        separable_wasted_auxiliary: true / false (D), requires wasted_auxiliary set to True

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """

        if max_auxiliary < controls_no - 2:
            return []  # if max_auxiliary allowed is to small - no representation given
        else:
            return [MCTBarenco75Dirty(controls_no)]  # only one available

    def generate_circuit(self) -> QuantumCircuit:
        """Return a QuantumCircuit implementation

        :return: a quantum circuit
        :rtype: QuantumCircuit
        """

        circ = self.recursive(list(range(self._n + 1)))
        # print(circ.draw())
        self._circuit = transpile(circ, basis_gates=["cx", "u3"])

        return deepcopy(self._circuit)

    def num_auxiliary_qubits(self):
        """Return number of auxiliary qubits

        :return: number of auxiliary qubits
        :rtype: int
        """
        return 0
