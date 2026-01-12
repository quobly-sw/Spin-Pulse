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
"""Pulse description of idle qubit."""

from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np

from spin_pulse.transpilation.dynamical_decoupling import DynamicalDecoupling

from .pulse_instruction import PulseInstruction

if TYPE_CHECKING:  # Stop cyclic implementation
    from ..hardware_specs import HardwareSpecs


class IdleInstruction(PulseInstruction):
    """Represent an idle (delay) operation applied to one or more qubits.

    This instruction models the absence of active control during a time
    interval. It is used both for explicit delays in pulse scheduling and
    as a building block for dynamical decoupling sequences. The duration
    is expressed in time steps.

    Attributes:
        - name (str): Name of the instruction ("delay").
        - qubits (list[qiskit.circuit.Qubit]): List of qubits on which the idle operation acts.
        - duration (int): Duration of the idle period in time steps.

    """

    def __init__(self, qubits: list, duration: int = 1):
        """Initialize an idle instruction on the specified qubits.

        Parameters:
            qubits (list[qiskit.circuit.Qubit]): List of qubits where the idle operation is applied.
            duration (int): Duration of the idle period. Default is 1.

        Returns:
            None: The idle instruction is stored in the created object.

        """
        super().__init__(qubits, duration)
        self.name = "delay"

    def __str__(self):
        """Return a readable string representation of the idle instruction.

        Returns:
            str: Description including the idle duration.

        """
        return f"IdlePulse , duration={self.duration} "

    def adjust_duration(self, duration: int):
        self.duration = duration

    def plot(self, ax=None, t_start=0, label_gates=True):
        """Plot the idle instruction as a flat line segment.

        Parameters:
            ax (matplotlib axis, optional): Axis on which the idle segment
              is drawn. If None, the current axis is used.
            t_start (int): Starting time of the idle segment. Default is 0.
            label_gates (bool): Unused parameter kept for API compatibility.
              Default is True.

        Returns:
            None: The idle segment is drawn on the provided axis.

        """
        if ax is None:
            ax = plt.gca()
        ax.plot([t_start, t_start + self.duration - 1], [0, 0], color="k")

    def to_hamiltonian(self):
        """Convert the idle operation to its Hamiltonian representation.

        The idle period corresponds to zero Hamiltonian evolution, resulting
        in no phase accumulation. This method returns a zero Hamiltonian and
        a zero frequency array compatible with the simulation interface.

        Returns:
            ndarray: Array of zeros of length ``duration``.

        """

        return 0 * np.eye(2**self.num_qubits), 0 * np.arange(self.duration)

    def to_dynamical_decoupling(
        self, hardware_specs: HardwareSpecs, mode: DynamicalDecoupling | None = None
    ):
        r"""Expand the idle instruction into a dynamical decoupling sequence.

        Depending on the hardware_specs dynamical decoupling mode, this
        method replaces the idle period with a sequence of rotations and
        shorter idle segments. Supported dynamical decoupling modes
        include:

        - SPIN_ECHO: Inserts two :math:`\pi` rotations with symmetric idle periods.
        - FULL_DRIVE: Applies repeated :math:`2\pi` rotations to average out noise.
        - None: Returns the idle instruction unchanged.

        Parameters:
            hardware_specs (HardwareSpecs): Hardware configuration specifying
                the dynamical decoupling mode and available pulse shapes.

        Returns:
            list[PulseInstruction]: List of PulseInstruction objects implementing the chosen dynamical decoupling sequence.

        """
        qubit = self.qubits[0]

        if hardware_specs.dynamical_decoupling is None:
            return [self]

        elif hardware_specs.dynamical_decoupling == DynamicalDecoupling.SPIN_ECHO:
            X_instruction_1 = hardware_specs.rotation_generator.from_angle(
                "x", [qubit], np.pi, hardware_specs
            )
            X_duration = X_instruction_1.duration
            X_instruction_2 = hardware_specs.rotation_generator.from_angle(
                "x", [qubit], np.pi, hardware_specs
            )

            duration_idle = int((self.duration - 2 * X_duration) // 2)
            if duration_idle <= 0:
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

        elif hardware_specs.dynamical_decoupling == DynamicalDecoupling.FULL_DRIVE:
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
