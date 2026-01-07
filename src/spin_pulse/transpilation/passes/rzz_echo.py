# --------------------------------------------------------------------------------------
# This code is part of SpinPulse.
#
# (C) Copyright Quobly 2025.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
# --------------------------------------------------------------------------------------
""""""

import numpy as np
from qiskit.circuit import QuantumRegister
from qiskit.circuit.library import RXGate, RZZGate
from qiskit.dagcircuit import DAGCircuit
from qiskit.transpiler.basepasses import TransformationPass


class RZZEchoPass(TransformationPass):
    """Echoes RZZ gates with X pulses to mitigate Stark shifts.

    This transpiler pass replaces each two-qubit RZZ gate by an echoed
    sequence consisting of interleaved pi rotations around the X axis and
    RZZ gates with half the original angle. The echo sequence is applied
    locally on each occurrence of an RZZ gate in the input DAG circuit.
    """

    def run(
        self,
        dag: DAGCircuit,
    ) -> DAGCircuit:
        """Applies the RZZ echo transformation to all RZZ gates in the DAG.

        Each RZZ(theta) operation is replaced by the following pattern
        on the two involved qubits:
        - RX(pi) on both qubits
        - RZZ(theta / 2)
        - RX(pi) on both qubits
        - RZZ(theta / 2)

        All other operations are left unchanged.

        Parameters:
            - dag (DAGCircuit): Input circuit represented as a DAG on which
              the transformation is applied.

        Returns:
            - DAGCircuit: New DAG circuit where each RZZ gate has been
              replaced by the echoed RZZ sequence.

        """
        for node in dag.op_nodes():
            if not node.op.name == "rzz":
                continue
            theta = node.op.params[0]
            # instantiate mini_dag and attach quantum register
            mini_dag = DAGCircuit()
            register = QuantumRegister(2)
            mini_dag.add_qreg(register)

            for _ in range(2):
                mini_dag.apply_operation_back(RXGate(np.pi), [register[0]])
                mini_dag.apply_operation_back(RXGate(np.pi), [register[1]])
                mini_dag.apply_operation_back(
                    RZZGate(theta / 2), [register[0], register[1]]
                )

            dag.substitute_node_with_dag(node, mini_dag)

        return dag
