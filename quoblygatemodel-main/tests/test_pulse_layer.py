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

from spin_pulse import HardwareSpecs, Shape
from spin_pulse.transpilation.instructions import IdleInstruction
from spin_pulse.transpilation.pulse_layer import PulseLayer
from spin_pulse.transpilation.pulse_sequence import PulseSequence


def make_hardware(num_qubits):
    # Create a minimal HardwareSpecs instance.
    B_field, delta, J_coupling = 0.5, 0.2, 0.01
    ramp_duration = 5
    return HardwareSpecs(
        num_qubits, B_field, delta, J_coupling, Shape.GAUSSIAN, ramp_duration, optim=3
    )


def make_single_qubit_layer(qubits):
    # Return a simple one-qubit PulseSequence of fixed duration.
    instr = IdleInstruction([qubits[0]], duration=10)
    return [PulseSequence([instr])]


def make_two_qubit_layer(qubits):
    # Return a simple two-qubit PulseSequence.
    instr = IdleInstruction(qubits, duration=12)
    return [PulseSequence([instr])]


def test_pulse_layer_init():
    qreg = qi.QuantumRegister(2)
    qubits = list(qreg)

    oneq = make_single_qubit_layer(qubits)
    twoq = make_two_qubit_layer(qubits)

    pl = PulseLayer(qubits, oneq, twoq)

    assert pl.duration == 12  # max of (10,12)
    assert pl.num_qubits == 2
    assert len(pl.oneq_pulse_sequences) == 2
    assert len(pl.twoq_pulse_sequences) == 1


def test_pulse_layer_str():
    qreg = qi.QuantumRegister(1)
    qubits = list(qreg)

    oneq = make_single_qubit_layer(qubits)
    pl = PulseLayer(qubits, oneq, [])

    s = str(pl)
    assert "Pulse Layer" in s
    assert str(pl.duration) in s


@pytest.mark.parametrize(
    "num_qubits, gate, angle, depth",
    [
        (3, "rx", np.pi / 2, 2),
        (5, "ry", np.pi / 2, 3),
        (5, "rz", np.pi / 2, 3),
        (5, "rzz", np.pi / 2, 1),
    ],
)
def test_from_circuit_layer_runs(num_qubits, gate, angle, depth):
    hardware = make_hardware(num_qubits)

    qreg = qi.QuantumRegister(num_qubits)
    circ = qi.QuantumCircuit(qreg)
    for _ in range(depth):
        if gate == "rzz":
            getattr(circ, gate)(angle, 0, 1)
        else:
            getattr(circ, gate)(angle, 0)

    layer = PulseLayer.from_circuit_layer(list(qreg), circ, hardware)

    assert isinstance(layer, PulseLayer)
    assert layer.duration > 0
    assert len(layer.oneq_pulse_sequences) == num_qubits
    if gate == "rzz":
        assert len(layer.twoq_pulse_sequences) == 1
    else:
        assert len(layer.twoq_pulse_sequences) == 0


def test_plot_runs():
    qreg = qi.QuantumRegister(2)
    qubits = list(qreg)

    oneq = make_single_qubit_layer(qubits)
    twoq = make_two_qubit_layer(qubits)

    pl = PulseLayer(qubits, oneq, twoq)

    pl.plot()  # must not raise
    plt.close("all")


def test_to_circuit_builds_valid_qiskit_circuit():
    qreg = qi.QuantumRegister(2)
    qubits = list(qreg)

    oneq = make_single_qubit_layer(qubits)
    twoq = make_two_qubit_layer(qubits)

    pl = PulseLayer(qubits, oneq, twoq)
    qc = pl.to_circuit()

    assert isinstance(qc, qi.QuantumCircuit)
    assert qc.num_qubits == 2
    print(qc.data)
    assert len(qc.data) == 1


def test_attach_dynamical_decoupling_runs():
    num_qubits = 1
    hardware = make_hardware(num_qubits)

    qreg = qi.QuantumRegister(num_qubits)
    qubits = list(qreg)

    oneq = make_single_qubit_layer(qubits)
    pl = PulseLayer(qubits, oneq, [])

    pl.attach_dynamical_decoupling(hardware)  # should not crash
