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
    """Add Pauli X to two-qubit gates to cancel Stark-Shifts"""

    def run(
        self,
        dag: DAGCircuit,
    ) -> DAGCircuit:
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
