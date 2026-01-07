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

from unittest.mock import MagicMock

import numpy as np
from qiskit.circuit import QuantumCircuit

#
# -----------------------
# Dummies / helpers
# -----------------------
#


class DummyInstruction:
    """Mimics a non-Idle instruction in a 2q pulse sequence."""

    def __init__(self, duration):
        self.duration = duration
        self.distort_factor = None


class DummyIdleInstruction:
    """Mimics IdleInstruction (used to check type(instruction) is not IdleInstruction)."""

    def __init__(self, duration):
        self.duration = duration
        self.distort_factor = None


class DummyOneQSequence:
    """Represents a single-qubit pulse sequence inside a PulseLayer."""

    def __init__(self, qubit, duration=5):
        self.qubits = [qubit]
        self.n_pulses = 1
        self.duration = duration
        # required by attach_time_traces()
        self.t_start_relative = [0]
        self.pulse_instructions = [DummyInstruction(duration=duration)]

    def to_hamiltonian(self):
        # Not needed in these tests (handled earlier in PulseLayer tests)
        return [], []

    def attach_time_trace(self, trace_segment, only_idle=False):
        # We'll just store it so we can assert in tests
        self.attached_trace = trace_segment
        self.only_idle_flag = only_idle

    def to_dynamical_decoupling(self, hardware_specs, mode=None):
        # Return a "modified" version of self
        new = DummyOneQSequence(self.qubits[0], duration=self.duration)
        new.dynamical_decoupling = mode
        return new


class DummyTwoQSequence:
    """Represents a 2-qubit pulse sequence inside a PulseLayer."""

    def __init__(self, q0, q1, duration=7):
        self.qubits = [q0, q1]
        self.n_pulses = 2
        self.duration = duration
        # For attach_time_traces() we need:
        self.t_start_relative = [0, 1]
        self.pulse_instructions = [
            DummyInstruction(duration=2),
            DummyInstruction(duration=3),
        ]

    def to_hamiltonian(self):
        return [], []


class DummyTimeTrace:
    """Mimics exp_env.time_traces[i] with a .values 1D array."""

    def __init__(self, values):
        self.values = np.array(values)


class DummyExpEnv:
    """
    Needs:
    - duration
    - only_idle
    - time_traces
    - time_traces_coupling
    - J_coupling
    """

    def __init__(self, duration, hardware_specs, only_idle=False, with_coupling=True):
        self.hardware_specs = hardware_specs
        self.duration = duration
        self.only_idle = only_idle
        base = np.arange(duration)  # 0..duration-1
        self.time_traces = [DummyTrace(base + 10), DummyTrace(base + 20)]
        if with_coupling:
            self.time_traces_coupling = [DummyTrace(base + 100)]
            self.J_coupling = 5.0


class DummyQubit:
    """Minimal stand-in for a Qiskit qubit with an _index attr used by attach_time_traces."""

    def __init__(self, idx=0):
        self._index = idx


class DummyPulseSequence:
    """
    Represents either a one-qubit or two-qubit pulse sequence in a layer.
    We just need:
      - .qubits -> list of qubits
      - .n_pulses
      - .pulse_instructions -> list of instruction-like objs
      - .t_start_relative -> list of ints
      - .attach_time_trace(time_trace, only_idle=...)
    """

    def __init__(self, qubits, n_pulses=1, t_starts=None, pulse_instrs=None):
        self.qubits = qubits
        self.n_pulses = n_pulses
        self.t_start_relative = t_starts or [0] * n_pulses
        self.pulse_instructions = pulse_instrs or [MagicMock(duration=3)]
        # we'll set by attach_time_traces():
        self.attached = []

    def attach_time_trace(self, arr, only_idle=False):
        # record for inspection
        self.attached.append((arr.copy(), only_idle))


class DummyPulseLayer:
    """
    Minimal PulseLayer with attributes used throughout PulseCircuit:
    - duration
    - t_start (filled by assign_starting_times)
    - .oneq_pulse_sequences
    - .twoq_pulse_sequences
    - .plot(axs, label_gates=...)
    - .to_circuit()
    - .attach_dynamical_decoupling(hardware_specs, mode=...)
    """

    def __init__(self, qubits, duration=5, oneq=None, twoq=None):
        self.duration = duration
        self.t_start = None
        self.oneq_pulse_sequences = (
            oneq if oneq is not None else [DummyPulseSequence([qubits[0]])]
        )
        self.twoq_pulse_sequences = (
            twoq if twoq is not None else [DummyPulseSequence([qubits[0]])]
        )
        self.time_traces = None
        self.time_traces_coupling = None

    def plot(self, axs, label_gates=True):
        # for test we just assert it's callable without error
        for ax in axs:
            # pretend we draw something
            ax.plot([0, 1], [0, 1])

    def to_circuit(self):
        # return a tiny QuantumCircuit with same qubit count as first sequence
        nq = len(self.oneq_pulse_sequences[0].qubits)
        circ = QuantumCircuit(nq)
        circ.x(0)
        return circ

    def attach_dynamical_decoupling(self, hw):
        # record that DD was applied
        self.applied_dd = hw.dynamical_decoupling

    @classmethod
    def from_circuit_layer(cls, qubits, layer_circ, hardware_specs):
        # create a layer with duration derived from layer_circ depth-ish
        return cls(qubits, duration=3)


class DummyHardwareSpecs:
    """
    Minimal hardware_specs:
    - .dynamical_decoupling
    - .fields (used in plot ymax calc)
    """

    def __init__(
        self, num_qubits=1, J_coupling=None, rot_duration=1, dynamical_decoupling=None
    ):
        self.dynamical_decoupling = dynamical_decoupling
        self.fields = {"x": 0.5, "y": 0.5, "z": 0.2, "Heisenberg": 0.7}
        self.rotation_generator = DummyRotationGenerator(rot_duration)
        self.ramp_duration = 1
        self.coeff_duration = 2
        self.num_qubits = num_qubits
        self.J_coupling = J_coupling


class DummyTrace:
    """Represents one time trace: just needs .values being indexable."""

    def __init__(self, values):
        self.values = np.array(values)


class DummyRotationGenerator:
    """
    Fake rotation generator that produces mock 'pulse instructions'.
    Each call to .from_angle(...) returns an object with:
      - duration (initially base_duration)
      - axis, angle, qubits
      - adjust_duration(new_dur) to mutate .duration
    We record all calls so we can assert call patterns.
    """

    def __init__(self, base_duration=2):
        self.base_duration = base_duration
        self.calls = []

    def from_angle(self, axis, qubits, angle, hardware_specs):
        instr = MagicMock()
        instr.duration = self.base_duration
        instr.axis = axis
        instr.angle = angle
        instr.qubits = qubits

        def _adjust(d):
            instr.duration = d

        instr.adjust_duration = _adjust

        self.calls.append((axis, angle, tuple(qubits)))
        return instr


# class DummyRotationGenerator:
#     """Fake rotation generator returning mock pulse instructions."""

#     def __init__(self, base_duration=2):
#         self.base_duration = base_duration
#         self.calls = []

#     def from_angle(self, axis, qubits, angle, hardware_specs):
#         """Return a fake pulse instruction with a settable duration."""
#         instr = MagicMock()
#         instr.axis = axis
#         instr.angle = angle
#         instr.duration = self.base_duration
#         instr.adjust_duration = lambda d: setattr(instr, "duration", d)
#         self.calls.append((axis, angle))
#         return instr
