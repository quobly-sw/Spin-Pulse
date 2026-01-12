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
"""Instruction representation used in pulse level description of a circuit."""


class PulseInstruction:
    """Base class representing a pulse-level instruction applied to qubits.

    This class defines the common interface for all pulse instructions,
    including rotation pulses and idle periods. Each instruction targets
    one or more qubits and spans a given discrete duration. Subclasses
    extend this class to implement specific pulse behaviors.

    Attributes:
        - name (str): Name identifying the type of pulse instruction.
        - qubits (list[qiskit.circuit.Qubit]): List of qubits on which the instruction acts.
        - num_qubits (int): Number of qubits targeted by the instruction.
        - duration (int): Duration of the instruction in time steps.

    """

    name = "_name"

    def __init__(self, qubits, duration=1):
        """Initialize a pulse instruction acting on the given qubits.

        Parameters:
            qubits (list[qiskit.circuit.Qubit]): List of qubits on which the instruction is applied.
            duration (int): Duration of the instruction in time steps.
              Default is 1.

        Returns:
            None: The configured instruction is stored in the created object.

        """
        self.qubits = qubits
        self.num_qubits = len(qubits)
        self.duration = duration
