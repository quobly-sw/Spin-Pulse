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
"""Pulse description of qubit idling."""

from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np

from .pulse_instruction import PulseInstruction

if TYPE_CHECKING:  # Stop cyclic implementation
    from spin_pulse.hardware_specs import HardwareSpecs


class IdleInstruction(PulseInstruction):
    """_summary_

    Parameters:
        PulseInstruction (_type_): _description_

    """

    def __init__(self, qubits: list, duration: int = 1):
        """_summary_

        Parameters:
            qubits (_type_): _description_
            duration (int, optional): _description_. Defaults to 1.

        """
        super().__init__(qubits, duration)
        self.name = "delay"

    def __str__(self):
        """
        Provide a string representation of the PulseDuration object.

        Returns:
        - str: A formatted string describing the PulseDuration object.

        """
        return f"IdlePulse , duration={self.duration} "

    def adjust_duration(self, duration: int):
        self.duration = duration

    def plot(self, ax=None, t_start=0, label_gates=True):
        """_summary_

        Parameters:
            ax (_type_, optional): _description_. Defaults to None.
            t_start (int, optional): _description_. Defaults to 0.
            label_gates (bool, optional): _description_. Defaults to True.

        """
        if ax is None:
            ax = plt.gca()
        ax.plot([t_start, t_start + self.duration - 1], [0, 0], color="k")

    def to_hamiltonian(self):
        """_summary_

        Returns:
            _type_: _description_

        """
        return 0 * np.eye(2**self.num_qubits), 0 * np.arange(self.duration)

    def to_dynamical_decoupling(self, hardware_specs: HardwareSpecs, mode=None):
        # TODO
        qubit = self.qubits[0]

        if mode is None:
            return [self]

        elif mode == "spin_echo":
            X_instruction_1 = hardware_specs.rotation_generator.from_angle(
                "x", [qubit], np.pi, hardware_specs
            )
            X_duration = X_instruction_1.duration
            X_instruction_2 = hardware_specs.rotation_generator.from_angle(
                "x", [qubit], np.pi, hardware_specs
            )

            duration_idle = int((self.duration - 2 * X_duration) // 2)
            if duration_idle < 0:
                return [self]
            else:
                idle_instruction_1 = IdleInstruction([qubit], duration_idle)
                idle_instruction_2 = IdleInstruction([qubit], duration_idle)

                return [
                    idle_instruction_1,
                    X_instruction_1,
                    idle_instruction_2,
                    X_instruction_2,
                ]

        elif mode == "full_drive":
            twopi_instruction = hardware_specs.rotation_generator.from_angle(
                "x", [qubit], 2 * np.pi, hardware_specs
            )
            n_loops = self.duration // (twopi_instruction.duration)
            if n_loops > 0:
                npi_instruction = hardware_specs.rotation_generator.from_angle(
                    "x", [qubit], 2 * np.pi * n_loops, hardware_specs
                )
                npi_instruction.adjust_duration(self.duration)
                return [npi_instruction]
            else:
                return [self]
