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

import matplotlib.pyplot as plt
import numpy as np
import pytest
import qiskit as qi
from matplotlib.figure import Axes, Figure

from spin_pulse import DynamicalDecoupling, HardwareSpecs, Shape
from spin_pulse.transpilation.instructions import (
    IdleInstruction,
    RotationInstruction,
    SquareRotationInstruction,
)
from spin_pulse.transpilation.pulse_sequence import PulseSequence

# --- Tests --------------------------------------------------------------------


def test_init_and_basic_properties():
    qreg = qi.QuantumRegister(3)
    qubits = list(qreg)
    duration1 = 3
    duration2 = 5
    name1 = "x"
    name2 = "z"

    pulse_instructions = [
        RotationInstruction(name1, qubits, duration1),
        RotationInstruction(name2, qubits, duration2),
    ]
    seq = PulseSequence(pulse_instructions)

    assert seq.qubits == qubits
    assert seq.num_qubits == len(qubits)
    assert seq.duration == 3 + 5
    assert seq.n_pulses == 2
    assert seq.t_start_relative == [0, 3]
    assert seq.name == f"{name1}{duration1}"


def test_plot_with_and_without_time_trace(monkeypatch):
    qreg = qi.QuantumRegister(3)
    qubits = list(qreg)
    duration1 = 3
    duration2 = 5

    PI1 = IdleInstruction(qubits, duration1)
    PI2 = IdleInstruction(qubits, duration2)

    pulse_instructions = [PI1, PI2]

    seq = PulseSequence(pulse_instructions)

    # no time_trace
    fig, ax = plt.subplots()
    seq.plot(ax=ax, label_gates=True)
    assert isinstance(fig, Figure)
    assert isinstance(ax, Axes)

    # with time_trace
    time_trace = np.arange(seq.duration, dtype=float)
    seq.attach_time_trace(time_trace, only_idle=False)

    fig, ax = plt.subplots()
    print(type(fig))
    seq.plot(ax=None, label_gates=False)
    assert isinstance(fig, Figure)
    assert isinstance(ax, Axes)


def test_to_hamiltonian_with_and_without_time_trace(monkeypatch):
    qreg = qi.QuantumRegister(1)
    qubits = list(qreg)
    duration1 = 3
    duration2 = 5
    name1 = "x"
    name2 = "y"
    sign = 1
    coeff_duration = 0

    pulse_instructions = [
        SquareRotationInstruction(name1, qubits, 2.0, sign, coeff_duration, duration1),
        SquareRotationInstruction(name2, qubits, 3.0, sign, coeff_duration, duration2),
    ]
    seq = PulseSequence(pulse_instructions)

    # no time_trace
    H, coeff = seq.to_hamiltonian()
    assert len(H) == 2
    assert len(coeff) == 2
    assert coeff[0].shape == (seq.duration,)
    assert coeff[1].shape == (seq.duration,)

    assert np.all(coeff[0][:3] == 2.0)
    assert np.all(coeff[0][3:] == 0.0)
    assert np.all(coeff[1][:3] == 0.0)
    assert np.all(coeff[1][3:] == 3.0)

    # with time trace
    time_trace = np.linspace(0.0, 1.0, seq.duration)
    seq.attach_time_trace(time_trace, only_idle=False)
    H2, coeff2 = seq.to_hamiltonian()

    assert len(H2) == 3
    assert len(coeff2) == 3
    assert np.allclose(coeff2[-1], time_trace)
    assert seq.t_start_relative[-1] == 3


def test_adjust_duration_adds_idle(monkeypatch):
    qreg = qi.QuantumRegister(1)
    qubits = list(qreg)
    duration1 = 3
    name1 = "x"
    sign = 1
    coeff_duration = 0
    pulse_instructions = [
        SquareRotationInstruction(name1, qubits, 2.0, sign, coeff_duration, duration1)
    ]
    seq = PulseSequence(pulse_instructions)

    seq.adjust_duration(3)
    assert seq.duration == 3
    assert seq.n_pulses == 1

    seq.adjust_duration(5)
    assert seq.duration == 5
    assert seq.n_pulses == 2
    assert seq.pulse_instructions[-1].name == "delay"
    assert seq.pulse_instructions[-1].duration == 2


def test_attach_time_trace_only_idle(monkeypatch):
    qreg = qi.QuantumRegister(1)
    qubits = list(qreg)
    duration1 = 3
    duration2 = 5
    name1 = "x"
    name2 = "y"
    sign = 1
    coeff_duration = 0
    pulse_instructions = [
        SquareRotationInstruction(name1, qubits, 2.0, sign, coeff_duration, duration1),
        SquareRotationInstruction(name2, qubits, 3.0, sign, coeff_duration, duration2),
    ]
    seq = PulseSequence(pulse_instructions)

    time_trace = np.arange(seq.duration, dtype=float)
    # only_idle=True :
    seq.attach_time_trace(time_trace, only_idle=True)
    assert np.all(seq.time_trace == 0.0)
    assert len(seq.time_trace) == duration1 + duration2

    # only_idle=False
    seq.attach_time_trace(time_trace, only_idle=False)
    assert np.all(seq.time_trace == time_trace)


def test_to_dynamical_decoupling_single_qubit(monkeypatch):
    qreg = qi.QuantumRegister(1)
    qubits = list(qreg)
    duration1 = 3
    duration2 = 5
    duration3 = 2
    name1 = "x"
    name2 = "y"
    sign = 1
    coeff_duration = 0
    pulse_instructions = [
        SquareRotationInstruction(name1, qubits, 2.0, sign, coeff_duration, duration1),
        IdleInstruction(qubits, duration2),
        SquareRotationInstruction(name2, qubits, 3.0, sign, coeff_duration, duration3),
    ]
    seq = PulseSequence(pulse_instructions)

    B_field, delta, J_coupling = 0.5, 0.2, 0.01
    ramp_duration = 5
    hw = HardwareSpecs(
        len(qubits),
        B_field,
        delta,
        J_coupling,
        Shape.GAUSSIAN,
        ramp_duration,
        optim=3,
        dynamical_decoupling=DynamicalDecoupling.FULL_DRIVE,
    )

    new_seq = seq.to_dynamical_decoupling(hw)

    assert len(seq.pulse_instructions) == len(pulse_instructions)
    assert len(new_seq.pulse_instructions) == len(pulse_instructions)
    assert seq.duration == new_seq.duration == duration1 + duration2 + duration3

    assert seq.pulse_instructions[0].name == "x"
    assert seq.pulse_instructions[1].name == "delay"
    assert seq.pulse_instructions[2].name == "y"

    assert new_seq.pulse_instructions[0].name == "x"
    assert new_seq.pulse_instructions[1].name == "delay"
    assert new_seq.pulse_instructions[2].name == "y"


def test_to_dynamical_decoupling_assert_multiqubit():
    qreg = qi.QuantumRegister(2)
    qubits = list(qreg)
    duration = 5
    pulse_instructions = [
        IdleInstruction(qubits, duration),
    ]
    seq = PulseSequence(pulse_instructions)

    B_field, delta, J_coupling = 0.5, 0.2, 0.01
    ramp_duration = 5
    hw = HardwareSpecs(
        len(qubits), B_field, delta, J_coupling, Shape.GAUSSIAN, ramp_duration, optim=3
    )

    with pytest.raises(ValueError):
        seq.to_dynamical_decoupling(hw)


def test_append_and_insert():
    qreg = qi.QuantumRegister(1)
    qubits = list(qreg)
    duration1 = 5
    pulse_instructions = [
        IdleInstruction(qubits, duration1),
    ]
    seq = PulseSequence(pulse_instructions)

    duration2 = 4
    name1 = "y"
    sign = 1
    coeff_duration = 0
    pi1 = SquareRotationInstruction(name1, qubits, 2.0, sign, coeff_duration, duration2)

    seq.append(pi1)

    assert seq.n_pulses == len(seq.pulse_instructions)
    assert seq.duration == duration1 + duration2
    assert seq.t_start_relative == [0, 5]
    assert seq.name == f"{name1}{duration2}"

    duration3 = 1
    pi2 = IdleInstruction(qubits, duration3)
    seq.insert(0, pi2)

    assert seq.n_pulses == 3
    assert seq.duration == duration1 + duration2 + duration3

    assert seq.t_start_relative == [0, 1, 6]


def test_insert_neg(monkeypatch):
    qreg = qi.QuantumRegister(1)
    qubits = list(qreg)
    duration1 = 5
    duration2 = 4
    name1 = "y"
    sign = 1
    coeff_duration = 0
    pi1 = SquareRotationInstruction(name1, qubits, 2.0, sign, coeff_duration, duration2)

    pulse_instructions = [IdleInstruction(qubits, duration1), pi1]

    seq = PulseSequence(pulse_instructions)

    duration3 = 1
    pi2 = IdleInstruction(qubits, duration3)
    seq.insert(-1, pi2)

    assert seq.n_pulses == 3
    assert seq.duration == duration1 + duration2 + duration3

    assert seq.t_start_relative == [0, 5, 9]

    duration4 = 2
    pi3 = IdleInstruction(qubits, duration4)
    seq.insert(-2, pi3)

    assert seq.t_start_relative == [0, 5, 9, 11]

    duration4 = 10
    pi3 = IdleInstruction(qubits, duration4)
    seq.insert(2, pi3)

    assert seq.t_start_relative == [0, 5, 9, 19, 21]
