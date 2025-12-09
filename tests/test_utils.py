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
from qiskit import QuantumCircuit
from qiskit.circuit import Gate

from spin_pulse import HardwareSpecs, Shape

# === Import target functions ===
from spin_pulse.utils import compare, gate_to_pulse_sequences


def test_compare():
    circ1 = QuantumCircuit(2)
    circ1.x(0)
    circ1.x(0)
    circ2 = circ1.copy()

    compare(circ1, circ2, ignore1=True, ignore2=True)

    # We check that x=y because circ1=circ2
    ax = plt.gca()
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    assert (xmax - xmin) == pytest.approx(ymax - ymin)


num_qubits = 1
B_field, delta, J_coupling = 0.5, 0.2, 0.01
ramp_duration = 5
hardware_specs = HardwareSpecs(
    num_qubits, B_field, delta, J_coupling, Shape.GAUSSIAN, ramp_duration, optim=3
)
# # ---- X gate ----
# qc_x = QuantumCircuit(1)
# qc_x.rx(0, np.pi/2)
# inst_x = qc_x.data[0]   # This is a CircuitInstruction object

# # ---- Y gate ----

# qc_y.ry(0, np.pi/2)
# inst_y = qc_y.data[0]

# # ---- Z gate ----
# qc_z = QuantumCircuit(1)
# qc_z.rz(0, np.pi/2)
# inst_z = qc_z.data[0]


@pytest.mark.parametrize(
    "gate, angle, hardware_specs",
    [
        ("rx", np.pi / 3, hardware_specs),
        ("rx", np.pi / 10, hardware_specs),
        ("ry", np.pi / 3, hardware_specs),
        ("rz", np.pi / 3, hardware_specs),
    ],
)
def test_gate_to_pulse_sequences_one_qubit(gate, angle, hardware_specs):
    circ = QuantumCircuit(1)
    getattr(circ, gate)(angle, 0)
    inst = circ.data[0]

    oneq, twoq = gate_to_pulse_sequences(inst, hardware_specs)

    # correct outputs
    assert len(oneq) == 1
    assert twoq == []


@pytest.mark.parametrize(
    "gate, angle, hardware_specs",
    [
        ("rzz", np.pi / 3, hardware_specs),
        ("rzz", np.pi / 10, hardware_specs),
    ],
)
def test_gate_to_pulse_sequences_rzz(gate, angle, hardware_specs):
    circ = QuantumCircuit(2)
    getattr(circ, gate)(angle, 0, 1)
    inst = circ.data[0]

    oneq, twoq = gate_to_pulse_sequences(inst, hardware_specs)
    # Should create one 2Q pulse + two 1Q detuned pulses
    assert len(twoq) == 1
    assert len(oneq) == 2


@pytest.mark.parametrize(
    "gate, hardware_specs",
    [
        ("delay", hardware_specs),
    ],
)
def test_gate_to_pulse_sequences_delay(gate, hardware_specs):
    circ = QuantumCircuit(1)
    getattr(circ, gate)(0)
    inst = circ.data[0]

    oneq, twoq = gate_to_pulse_sequences(inst, hardware_specs)
    # Should create one 2Q pulse + two 1Q detuned pulses
    assert len(oneq) == 1
    assert twoq == []


def test_gate_to_pulse_sequences_unknown(
    dummy_hardware_specs,
):
    """Unknown gates should trigger an error."""
    qc = QuantumCircuit(1)
    gate = Gate("foo", 1, [])
    instr = qc.to_instruction()
    instr.operation = gate
    instr.qubits = [0]
    with pytest.raises(ValueError):
        _, _ = gate_to_pulse_sequences(instr, dummy_hardware_specs)
