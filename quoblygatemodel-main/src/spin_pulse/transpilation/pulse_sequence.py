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
"""Low-level representation of pulses applied to qubits."""

import warnings

import matplotlib.pyplot as plt
import numpy as np
from qiskit.quantum_info import Pauli

from .hardware_specs import HardwareSpecs
from .instructions import IdleInstruction, PulseInstruction


class PulseSequence:
    """Sequence of pulse instructions acting on one or several qubits.

    A PulseSequence is an ordered list of PulseInstruction objects consecutive in time. The class computes the total duration of the
    sequence, the starting time of each constituent instruction, and provides
    utilities for plotting. It allows to reconstruct Hamiltonians,
    attach time traces from a noise environment, and apply dynamical
    decoupling on idle segments.

    Attributes:

        - qubits (list[qiskit.circuit.Qubit]): Ordered list of qubits included in the layer.
        - num_qubits (int): Number of qubits in the sequence.
        - pulse_instructions (list[PulseInstruction]): Ordered list of pulse
            instructions that form the sequence.
        - n_pulses (int): Number of instructions in the sequence.
        - duration (int): Total duration of the sequence (sum of individual
            instruction durations).
        - t_start_relative (list[int]): Starting time of each pulse instruction
            relative to the beginning of the sequence.
        - name (str): Concatenated name describing the sequence, formed from
            instruction names and durations.

    """

    def __init__(self, pulse_instructions: list):
        """Initialize a PulseSequence from a list of PulseInstruction objects.

        The constructor computes the total duration, the relative starting
        times of each instruction, and assigns a compact sequence name for
        identification or debugging.

        Parameters:
            pulse_instructions (list[PulseInstruction]): Ordered list of pulse
                instructions to concatenate into a sequence. All instructions
                must act on the same qubit subset.

        """
        self.qubits = pulse_instructions[0].qubits
        self.num_qubits = len(self.qubits)
        self.n_pulses = len(pulse_instructions)

        self.duration = sum([_.duration for _ in pulse_instructions])
        self.t_start_relative = [0]
        self.pulse_instructions = pulse_instructions
        self.name = ""
        for i in range(self.n_pulses - 1):
            self.t_start_relative.append(
                self.t_start_relative[-1] + pulse_instructions[i].duration
            )
            self.name += (
                self.pulse_instructions[i].name
                + f"{self.pulse_instructions[i].duration}"
            )

    def plot(self, ax=None, label_gates: bool = True):
        """Plot the pulse sequence on a matplotlib axis.

        Each instruction is rendered at its relative starting time using the
        ``PulseInstruction.plot`` method. If a time trace has been attached,
        the corresponding stochastic noise signal is plotted on top of the
        sequence.

        Parameters:
            ax (matplotlib.axes.Axes | None): Axis on which to draw the
                sequence. If None, the current axis is used.
            label_gates (bool): Whether to annotate pulse instructions with
                gate labels.

        """
        if ax is None:
            ax = plt.gca()
        for i in range(self.n_pulses):
            self.pulse_instructions[i].plot(
                ax=ax, t_start=self.t_start_relative[i], label_gates=label_gates
            )
        if hasattr(self, "time_trace"):
            ax.plot(
                range(self.duration),
                self.time_trace,
                color="black",
            )

    def to_hamiltonian(self):
        """Construct the Hamiltonian representation of the sequence.

        For each pulse instruction, this method extracts the local Hamiltonian
        generator and its time-dependent coefficient. The coefficients are
        embedded into a global array spanning the full sequence duration,
        resulting in a list of Hamiltonians and a list of time-dependent
        coefficient vectors for each qubit.

        If a noise time trace was previously attached (e.g., from a noise
        model), an additional Z-type Hamiltonian is appended for one-qubit
        sequences (for deviations of the qubit's frequency).

        Returns:
            tuple[np.ndarray, np.ndarray]:
                H: ndarray of Hamiltonian matrices.
                coeff: ndarray of time-dependent coefficient.

        """
        num_H = self.n_pulses + int(hasattr(self, "time_trace"))
        H = np.empty((num_H, 2**self.num_qubits, 2**self.num_qubits), dtype=complex)
        coeff = np.zeros((num_H, self.duration), dtype=complex)
        for i in range(self.n_pulses):
            (
                H[i, :, :],
                coeff[
                    i,
                    self.t_start_relative[i] : self.t_start_relative[i]
                    + self.pulse_instructions[i].duration,
                ],
            ) = self.pulse_instructions[i].to_hamiltonian()
        if hasattr(self, "time_trace"):
            assert self.num_qubits == 1
            H[-1, :, :] = Pauli("Z").to_matrix() * 0.5
            coeff[-1, :] = self.time_trace
        return H, coeff

    def adjust_duration(self, duration: int):
        """Extend individual qubit pulse sequence to match a target duration
        (i.e. usually the maximal duration of a pulse sequence in a pulse layer).

        If the target duration is larger than the current sequence duration,
        an IdleInstruction is appended to pad the sequence. This is used, for
        example, to align pulse durations across a PulseLayer. Otherwise, a warning is
        issued to let know the user that the duration in input was too short.

        Parameters:
            duration (int): Targeted total duration for the sequence.

        """
        if duration > self.duration:
            idle_instruction = IdleInstruction(self.qubits, duration - self.duration)
            self.append(idle_instruction)
            self.duration = duration
        elif duration < self.duration:
            warnings.warn(
                "Cannot adjust the duration of the PulseSequence with a shorter value than "
                "the current duration of the sequence. PulseSequence left untouched."
            )

    def attach_time_trace(self, time_trace: np.ndarray, only_idle: bool):
        """Attach a noise time trace to the sequence.

        The method maps a provided noise signal (typically from a noise
        model) onto the time domain of the sequence. If ``only_idle`` is True,
        the trace is only applied to idle ("delay") instructions; otherwise,
        it is applied to all instructions.

        Parameters:
            time_trace (np.ndarray): Array of classical values sampled over
                the full duration of the parent PulseLayer.
            only_idle (bool): If True, attach the trace only on idle
                instructions; all active pulses receive no time trace.

        """
        self.time_trace = np.zeros(self.duration)
        for i in range(self.n_pulses):
            ta = self.t_start_relative[i]
            tb = ta + self.pulse_instructions[i].duration
            if not (only_idle) or self.pulse_instructions[i].name == "delay":
                self.time_trace[ta:tb] = time_trace[ta:tb]
            else:
                self.time_trace[ta:tb] = np.zeros(self.pulse_instructions[i].duration)

    def to_dynamical_decoupling(self, hardware_specs: HardwareSpecs):
        """Insert dynamical decoupling sequence into the Idle instruction.

        The method scans the pulse list and replaces idle ("delay")
        instructions by a list of pulses generated according to the selected
        dynamical decoupling mode defined in the hardware specifications.
        Non-idle instructions are left unchanged. Only single-qubit sequences
        can be dynamically decoupled.

        Parameters:
            hardware_specs (HardwareSpecs): Hardware configuration specifying
                the dynamical decoupling mode and available pulse shapes.

        Returns:
            PulseSequence: A new sequence with dynamical decoupling applied.

        Raises:
            AssertionError: If the sequence acts on more than one qubit.

        """
        pulse_instructions = []
        if self.num_qubits != 1:
            raise ValueError(
                "Dynamically decouple only possible for one qubit sequences, here n_qubits={self.num_qubits}"
            )
        for i in range(self.n_pulses):
            if self.pulse_instructions[i].name == "delay":
                pulse_instructions += self.pulse_instructions[
                    i
                ].to_dynamical_decoupling(hardware_specs)
            else:
                pulse_instructions.append(self.pulse_instructions[i])
        self.pulse_instructions = pulse_instructions
        return PulseSequence(pulse_instructions)

    def append(self, pulse_instruction: PulseInstruction):
        """Append a pulse instruction at the end of the sequence.

        The starting times and sequence metadata (duration, name, pulse count)
        are updated accordingly.

        Parameters:
            pulse_instruction (PulseInstruction): Instruction to append.

        """
        self.pulse_instructions = [*self.pulse_instructions, pulse_instruction]
        self.t_start_relative = [*self.t_start_relative, self.duration]

        self.duration += pulse_instruction.duration
        self.name += pulse_instruction.name + f"{pulse_instruction.duration}"
        self.n_pulses = len(self.pulse_instructions)

    def insert(self, pos: int, pulse_instruction: PulseInstruction):
        """Insert a pulse instruction at a specified position.

        The method inserts the instruction at index ``pos`` (negative indices
        are accepted and interpreted in Python style). The relative start times
        and total duration are recomputed after insertion.

        Parameters:
            pos (int): Insertion index; negative values count from the end.
            pulse_instruction (PulseInstruction): Instruction to insert.

        """

        if pos < 0:  # Translate back into positive
            pos = self.n_pulses + pos + 1
        self.pulse_instructions.insert(pos, pulse_instruction)
        self.duration += pulse_instruction.duration
        self.t_start_relative = self.generate_relative_time_sequence()
        self.name = pulse_instruction.name + f"{pulse_instruction.duration}" + self.name
        self.n_pulses = len(self.pulse_instructions)

    def generate_relative_time_sequence(self) -> list[int]:
        """Generate the list of starting times for each pulse instruction.

        Returns:
            list[int]: Relative starting times of each instruction, with
            the first entry equal to 0 and each subsequent entry equal to
            the cumulative duration of the preceding pulses.

        """
        sequence: list[int] = [0]
        tot_time: int = 0
        for pulse in self.pulse_instructions[:-1]:
            tot_time += pulse.duration
            sequence.append(tot_time)
        return sequence
