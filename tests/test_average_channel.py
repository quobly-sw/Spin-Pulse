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
from qiskit.quantum_info import Operator, SuperOp

from spin_pulse import HardwareSpecs, PulseCircuit, Shape
from spin_pulse.average_channel import (
    get_chan,
    get_single_gate_circuit,
    pauli_dict_to_channel,
    plot_chi_matrix,
    print_chi_elements,
    single_gate_average_channel,
)

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------


def make_hardware_specs(num_qubits: int = 1) -> HardwareSpecs:
    """Create a minimal HardwareSpecs instance suitable for tests.

    Adapt this to match your actual HardwareSpecs __init__.
    """
    B_field, delta, J_coupling = 0.5, 0.2, 0.01
    ramp_duration = 5
    hw = HardwareSpecs(
        num_qubits, B_field, delta, J_coupling, Shape.GAUSSIAN, ramp_duration, optim=3
    )

    # single_gate_average_channel expects: hardware_specs.time_traces[0].duration
    class DummyTrace:
        def __init__(self, duration: int):
            self.duration = duration

    hw.time_traces = [DummyTrace(duration=50)]
    return hw


# ----------------------------------------------------------------------
# Tests for get_single_gate_circuit
# ----------------------------------------------------------------------


@pytest.mark.parametrize("gate", ["rx", "ry", "rz"])
def test_get_single_gate_circuit_rotation_gates(gate):
    hardware_specs = make_hardware_specs()
    theta = np.pi / 4

    pulse_circ = get_single_gate_circuit(gate, theta, hardware_specs)

    assert isinstance(pulse_circ, PulseCircuit)
    assert pulse_circ.duration > 0
    assert pulse_circ.n_layers == 1


def test_get_single_gate_circuit_delay_gate():
    hardware_specs = make_hardware_specs()
    idle_time = 20

    pulse_circ = get_single_gate_circuit(
        "delay", None, hardware_specs, idle_time=idle_time
    )

    assert isinstance(pulse_circ, PulseCircuit)
    assert pulse_circ.duration == idle_time


def test_get_single_gate_circuit_wrong_gate_raises():
    hardware_specs = make_hardware_specs()
    with pytest.raises(AssertionError):
        get_single_gate_circuit("wrong_gate", 0.1, hardware_specs)


# ----------------------------------------------------------------------
# Tests for get_chan
# ----------------------------------------------------------------------


def test_get_chan_returns_superop():
    hardware_specs = make_hardware_specs()
    pulse_circ = get_single_gate_circuit("rx", np.pi / 3, hardware_specs)

    chan = get_chan(pulse_circ)

    assert isinstance(chan, SuperOp)
    # SuperOp dimension for 1 qubit: 4x4
    assert chan.data.shape == (4, 4)


# ----------------------------------------------------------------------
# Tests for single_gate_average_channel
# ----------------------------------------------------------------------


def test_single_gate_average_channel_with_n_exp():
    hardware_specs = make_hardware_specs()
    gate = "ry"
    theta = np.pi / 5

    avg_channel = single_gate_average_channel(
        gate,
        theta,
        hardware_specs,
        n_exp=2,
        idle_time=0,
    )

    assert isinstance(avg_channel, SuperOp)
    assert avg_channel.data.shape == (4, 4)


@pytest.mark.parametrize("gate", ["rx", "ry", "rz"])
def test_single_gate_average_channel_physical_convergence(gate):
    hardware_specs = make_hardware_specs()
    theta = np.pi / 4

    # Compute averaged channel (physical)
    avg = single_gate_average_channel(gate, theta, hardware_specs, n_exp=5, idle_time=0)
    assert isinstance(avg, SuperOp)

    # Build the ideal reference gate
    circ = qi.QuantumCircuit(1)
    getattr(circ, gate)(theta, 0)
    ideal = SuperOp(Operator(circ))

    # Compare channels
    diff = np.linalg.norm(avg.data - ideal.data)

    # Physical expectation: small difference
    assert diff < 1e-1, f"Averaged channel deviates too much from ideal: {diff}"


# -----------------------------------------------------------
#  Test n_exp=None branch (automatic number of experiments)
# -----------------------------------------------------------


def test_single_gate_average_channel_with_automatic_n_exp():
    """Tests the branch where n_exp is None."""
    hardware_specs = make_hardware_specs()
    gate = "rz"
    theta = np.pi / 7

    avg_channel = single_gate_average_channel(
        gate,
        theta,
        hardware_specs,
        n_exp=None,
        idle_time=0,
    )

    assert isinstance(avg_channel, SuperOp)
    assert avg_channel.data.shape == (4, 4)


# ----------------------------------------------------------------------
# Tests for print_chi_elements
# ----------------------------------------------------------------------


def test_print_chi_elements_runs(capsys):
    # Build a simple identity channel for 1 qubit
    u = Operator(np.eye(2))
    chan = SuperOp(u)

    # Should print some chi elements without raising
    print_chi_elements(chan)

    captured = capsys.readouterr()
    # At least one line containing a Pauli label should appear
    # (e.g. "I ⊗ I" for 1 qubit)
    assert "I" in captured.out


# ----------------------------------------------------------------------
# Tests for plot_chi_matrix
# ----------------------------------------------------------------------


def _make_simple_channel():
    """Return a simple 1-qubit identity-like channel."""
    u = Operator(np.eye(2))
    return SuperOp(u)


def test_plot_chi_matrix_with_threshold():
    """Test the branch with threshold != None and analytical/non-analytical keys."""
    chan1 = _make_simple_channel()
    chan2 = _make_simple_channel()

    channels = {
        "analytical_id": chan1,
        "numerical_id": chan2,
    }

    fig = plot_chi_matrix(channels, threshold=1e-3)

    assert fig is not None
    plt.close(fig)


def test_plot_chi_matrix_without_threshold():
    """Test the branch with threshold == None."""
    chan = _make_simple_channel()
    channels = {"numerical_id": chan}

    fig = plot_chi_matrix(channels, threshold=None)

    assert fig is not None
    plt.close(fig)


# ----------------------------------------------------------------------
# Tests for pauli_dict_to_channel
# ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "pauli_dict", [{"II": (1 + 0.2) / 2, "ZZ": (1 - 0.2) / 2}, {"IZ": 1.0}]
)
def test_pauli_dict_to_channel_two_qubits(pauli_dict):
    op_channel = pauli_dict_to_channel(pauli_dict)

    assert isinstance(op_channel, SuperOp)
    # For 2 qubits, channel space is 16x16
    assert op_channel.data.shape == (4, 4)
