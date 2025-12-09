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
"""Utility functions to interact with circuits."""

import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

from .hardware_specs import HardwareSpecs
from .instructions import IdleInstruction, SquareRotationInstruction
from .pulse_sequence import PulseSequence


def compare(
    circ1: QuantumCircuit,
    circ2: QuantumCircuit,
    ignore1: bool = True,
    ignore2: bool = True,
):
    """
    Compare two quantum circuits by plotting the matrix elements of their
    corresponding unitary operators.

    This function converts both circuits into unitary matrices using
    qiskit.quantum_info.Operator and optionally ignores their layout.
    The global phase is removed before comparison. Three scatter plots are
    generated: real parts, imaginary parts, and absolute values of the matrix
    elements. A diagonal reference line is shown, and the squared distance
    between the two matrices is displayed.

    Parameters:
        - circ1 (qiskit.QuantumCircuit): First circuit to compare.
        - circ2 (qiskit.QuantumCircuit): Second circuit to compare.
        - ignore1 (bool): If True, ignore the layout when converting ``circ1``.
        - ignore2 (bool): If True, ignore the layout when converting ``circ2``.

    Notes:
        The global phase is aligned using the matrix element with maximum magnitude.
        This function is useful to visually validate the equivalence of two circuits
        after transformations such as transpilation or pulse compilation.

    """
    data1 = (Operator.from_circuit(circ1, ignore_set_layout=ignore1).data).flatten()
    data2 = (Operator.from_circuit(circ2, ignore_set_layout=ignore2).data).flatten()
    i_phase = np.argmax(abs(data1))
    phase1 = np.angle(data1[i_phase])
    data1 *= np.exp(-1j * phase1)
    phase2 = np.angle(data2[i_phase])
    data2 *= np.exp(-1j * phase2)
    plt.plot(np.real(data1), np.real(data2), "o", label="real")
    plt.plot(np.imag(data1), np.imag(data2), "x", label="imag")
    plt.plot(np.abs(data1), np.abs(data2), "*", label="abs")

    a = np.max(abs(data1))
    plt.plot([-a, a], [-a, a], "--k")
    plt.text(-a, a, f"distance  {np.sum(np.abs(data1 - data2) ** 2)}")
    plt.xlabel("circ 1 matrix elements")
    plt.ylabel("circ 2 matrix elements")
    plt.legend(loc=0)


def gate_to_pulse_sequences(
    gate, hardware_specs: HardwareSpecs
) -> tuple[list[PulseSequence], list[PulseSequence]]:
    """
    Translate a Qiskit gate (RX, RY, RZ, or RZZ) into hardware-compatible
    pulse sequences.

    This function maps high-level Qiskit rotation gates into low-level pulse
    instructions that follow the hardware specifications. Single-qubit rotations
    generate a single PulseSequence, while the ``rzz`` interaction generate two
    qubit sequence followed by a single qubit sequence on each qubit.

    Parameters:
        - gate (CircuitInstruction): The Qiskit instruction to translate.
            Supported operations are ``rx``, ``ry``, ``rz``, ``rzz`` and ``delay``.
        - hardware_specs (HardwareSpecs): Hardware configuration including available
            fields, ramp durations, and rotation generation routines.

    Returns:
        tuple[list[PulseSequence], list[PulseSequence]]:
            A pair of lists:
            * one-qubit pulse sequences generated from the gate,
            * two-qubit pulse sequences (only for ``rzz``).

    Raises:
        ValueError: If the gate type is not supported.

    Notes:
        For ``rzz`` gates:
            * A central Heisenberg pulse is generated.
            * Pre/post idle ramps are added to ensure smooth pulse shaping.
            * Each qubit receives a compensating detuned Z rotation of equal duration.

        For ``delay`` gates:
            A single IdleInstruction is wrapped in a PulseSequence.

        For single-qubit rotations:
            The corresponding rotation generator in ``hardware_specs`` is invoked.

    """
    # Gate being a Qiskit.CircuitInstruction
    generator = hardware_specs.rotation_generator
    ramp_duration = hardware_specs.ramp_duration
    oneq_pulse_sequences: list[PulseSequence] = []
    twoq_pulse_sequences: list[PulseSequence] = []
    name_: str = gate.operation.name
    if name_ in ["rx", "ry", "rz", "rzz"]:
        qubits = gate.qubits
        angle = gate.operation.params[0]
        if name_ == "rzz":
            heis_instruction = generator.from_angle(
                "Heisenberg", qubits, angle, hardware_specs
            )
            pre_instruction = IdleInstruction(qubits, hardware_specs.ramp_duration)
            post_instruction = IdleInstruction(qubits, hardware_specs.ramp_duration)
            heis_sequence = PulseSequence(
                [pre_instruction, heis_instruction, post_instruction]
            )
            twoq_pulse_sequences.append(heis_sequence)
            duration = heis_sequence.duration
            amplitude = hardware_specs.fields["z"]
            detuned_instruction_0 = SquareRotationInstruction(
                "z", [qubits[0]], amplitude, -1.0, ramp_duration, duration
            )
            detuned_instruction_1 = SquareRotationInstruction(
                "z", [qubits[1]], amplitude, 1.0, ramp_duration, duration
            )
            oneq_pulse_sequences.append(PulseSequence([detuned_instruction_0]))
            oneq_pulse_sequences.append(PulseSequence([detuned_instruction_1]))
        else:
            rotation_instruction = generator.from_angle(
                name_[1:], qubits, angle, hardware_specs
            )
            oneq_pulse_sequences.append(PulseSequence([rotation_instruction]))
    elif gate.operation.name in ["delay"]:
        duration = gate.operation.duration
        oneq_pulse_sequences.append(
            PulseSequence([IdleInstruction(gate.qubits, duration=duration)])
        )
    else:
        raise ValueError(
            f"The gate {name_} pulse is not implemented. Possible gates are rx,ry,rz,rzz"
        )
    return oneq_pulse_sequences, twoq_pulse_sequences
