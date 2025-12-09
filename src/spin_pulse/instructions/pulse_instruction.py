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
    name = "_name"

    def __init__(
        self, qubits, duration=1
    ):  # circuit_instruction,t_start=0,duration=1):
        """
        Initialize a PulseInstruction with ...

        Parameters:
        - ..: ..

        """
        self.qubits = qubits
        self.num_qubits = len(qubits)
        self.duration = duration
