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

import math as m

import numpy as np
import pytest
import qiskit as qi
from qiskit.circuit.random import random_circuit
from qiskit.quantum_info import Operator, process_fidelity

from spin_pulse import HardwareSpecs, Shape

one_qubit_gates = ["id", "x", "y", "z", "h", "s", "sdg", "t", "tdg", "sx", "sxdg"]
rot_one_qubit_gates = ["rx", "ry", "rz"]
rot_two_qubit_gates = ["crx", "cry", "crz", "rxx", "ryy", "rzz", "rzx"]

two_qubit_gates = ["cx", "cy", "cz", "ch", "cs", "csdg", "swap", "ecr", "dcx"]
pulse_shapes = [Shape.GAUSSIAN, Shape.SQUARE]
angles = [np.pi, np.pi / 2, np.pi / 8]

direct_1q = [
    (gate, 1, pulse_shape) for gate in one_qubit_gates for pulse_shape in pulse_shapes
]

direct_2q = [
    (gate, 2, pulse_shape) for gate in two_qubit_gates for pulse_shape in pulse_shapes
]

rot_1q = [
    (gate, 1, pulse_shape, angle)
    for gate in rot_one_qubit_gates
    for pulse_shape in pulse_shapes
    for angle in angles
]

rot_2q = [
    (gate, 2, pulse_shape, angle)
    for gate in rot_two_qubit_gates
    for pulse_shape in pulse_shapes
    for angle in angles
]

all_direct = direct_1q + direct_2q
all_rot = rot_1q + rot_2q


@pytest.mark.parametrize(
    "gate, n_qb, pulse_shape",
    all_direct,
)
def test_isolated_gates(gate, n_qb, pulse_shape):
    qreg = qi.QuantumRegister(n_qb)
    circ = qi.QuantumCircuit(qreg)

    B0, delta, J_coupling, rotation_shape, ramp_duration, coeff_duration = (
        5,
        1,
        10,
        pulse_shape,
        5,
        7,
    )

    hardware_specs = HardwareSpecs(
        num_qubits=n_qb,
        B_field=B0,
        delta=delta,
        J_coupling=J_coupling,
        rotation_shape=rotation_shape,
        ramp_duration=ramp_duration,
        coeff_duration=coeff_duration,
    )

    if n_qb == 1:
        getattr(circ, gate)(0)
    elif n_qb == 2:
        getattr(circ, gate)(0, 1)

    isa_circ = hardware_specs.gate_transpile(circ)
    # isa_circ = hardware_specs.first_pass.run(circ)
    assert m.isclose(
        process_fidelity(Operator.from_circuit(circ), Operator.from_circuit(isa_circ)),
        1,
    )


@pytest.mark.parametrize(
    "gate, n_qb, pulse_shape, angle",
    all_rot,
)
def test_rotation_insolated_gates(gate, n_qb, pulse_shape, angle):
    qreg = qi.QuantumRegister(n_qb)
    circ = qi.QuantumCircuit(qreg)

    B0, delta, J_coupling, rotation_shape, ramp_duration, coeff_duration = (
        5,
        1,
        10,
        pulse_shape,
        5,
        7,
    )

    hardware_specs = HardwareSpecs(
        num_qubits=n_qb,
        B_field=B0,
        delta=delta,
        J_coupling=J_coupling,
        rotation_shape=rotation_shape,
        ramp_duration=ramp_duration,
        coeff_duration=coeff_duration,
    )
    if n_qb == 1:
        getattr(circ, gate)(angle, 0)
    elif n_qb == 2:
        getattr(circ, gate)(angle, 0, 1)

    isa_circ = hardware_specs.gate_transpile(circ)
    # isa_circ = hardware_specs.first_pass.run(circ)
    assert m.isclose(
        process_fidelity(Operator.from_circuit(circ), Operator.from_circuit(isa_circ)),
        1,
    )


@pytest.mark.parametrize(
    "n_qb, depth",
    [
        (1, 2),
        (1, 10),
        (5, 2),
    ],
)
def test_random_circuit(n_qb, depth):
    circ = random_circuit(n_qb, depth, measure=False)

    B0, delta, J_coupling, rotation_shape, ramp_duration, coeff_duration = (
        5,
        1,
        10,
        Shape.GAUSSIAN,
        5,
        7,
    )
    hardware_specs = HardwareSpecs(
        num_qubits=n_qb,
        B_field=B0,
        delta=delta,
        J_coupling=J_coupling,
        rotation_shape=rotation_shape,
        ramp_duration=ramp_duration,
        coeff_duration=coeff_duration,
    )

    isa_circ = hardware_specs.gate_transpile(circ)
    # isa_circ = hardware_specs.first_pass.run(circ)
    assert m.isclose(
        process_fidelity(Operator.from_circuit(circ), Operator.from_circuit(isa_circ)),
        1,
    )
