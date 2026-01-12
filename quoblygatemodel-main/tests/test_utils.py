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

import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.circuit import Gate
from qiskit.quantum_info import Statevector

from spin_pulse import HardwareSpecs, Shape
from spin_pulse.transpilation.utils import (
    deshuffle_qiskit,
    gate_to_pulse_sequences,
    qiskit_to_quimb,
)

num_qubits = 1
B_field, delta, J_coupling = 0.5, 0.2, 0.01
ramp_duration = 5
hardware_specs = HardwareSpecs(
    num_qubits, B_field, delta, J_coupling, Shape.GAUSSIAN, ramp_duration, optim=3
)


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
    getattr(circ, gate)(1)
    inst = circ.data[0]

    oneq, twoq = gate_to_pulse_sequences(inst, hardware_specs)
    # Should create one 2Q pulse + two 1Q detuned pulses
    assert len(oneq) == 1
    assert twoq == []


def test_gate_to_pulse_sequences_unknown(
    dummy_hardware_specs,
):
    # Unknown gates should trigger an error."""
    qc = QuantumCircuit(1)
    gate = Gate("foo", 1, [])
    instr = qc.to_instruction()
    instr.operation = gate
    instr.qubits = [0]
    with pytest.raises(ValueError):
        _, _ = gate_to_pulse_sequences(instr, dummy_hardware_specs)


def test_deshuffle_qiskit_is_involution_random_complex():
    rng = np.random.default_rng(123)
    n = 3
    d = 2**n
    mat = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))

    out = deshuffle_qiskit(deshuffle_qiskit(mat))
    assert np.allclose(out, mat)


def test_qiskit_to_quimb_matches_statevector_for_1q_only():
    # Checks endianness / mapping for a simple 1-qubit circuit.
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.rz(0.37, 0)
    qc.rx(-0.21, 0)

    quimb_circ = qiskit_to_quimb(qc)
    psi_quimb = np.asarray(quimb_circ.psi.to_dense()).reshape(-1)
    psi_qiskit = Statevector.from_instruction(qc).data
    rho_quimb = np.outer(psi_quimb, np.conj(psi_quimb))
    rho_qiskit = np.outer(psi_qiskit, np.conj(psi_qiskit))
    qiskit_rho_d = deshuffle_qiskit(rho_qiskit)

    overlap = np.vdot(rho_quimb, qiskit_rho_d)
    assert np.isclose(np.abs(overlap), 1.0, atol=1e-10)


def test_qiskit_to_quimb_matches_statevector_for_2q_with_entangling_gate():
    # Checks multi-qubit gate path (deshuffle_qiskit is used).
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.rz(0.19, 1)
    qc.ry(-0.33, 0)

    quimb_circ = qiskit_to_quimb(qc)
    psi_quimb = np.asarray(quimb_circ.psi.to_dense()).reshape(-1)
    psi_qiskit = Statevector.from_instruction(qc).data
    rho_quimb = np.outer(psi_quimb, np.conj(psi_quimb))
    rho_qiskit = np.outer(psi_qiskit, np.conj(psi_qiskit))
    qiskit_rho_d = deshuffle_qiskit(rho_qiskit)

    # Match up to global phase.
    overlap = np.vdot(rho_quimb, qiskit_rho_d)
    assert np.isclose(np.abs(overlap), 1.0, atol=1e-10)


def test_qiskit_to_quimb_matches_operator_action_on_basis_state_3q():
    # A slightly larger regression: compare action on |000>.
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 2)
    qc.ry(0.7, 1)
    qc.cx(1, 2)
    qc.rz(-0.2, 2)

    quimb_circ = qiskit_to_quimb(qc)
    psi_quimb = np.asarray(quimb_circ.psi.to_dense()).reshape(-1)
    psi_qiskit = Statevector.from_instruction(qc).data
    rho_quimb = np.outer(psi_quimb, np.conj(psi_quimb))
    rho_qiskit = np.outer(psi_qiskit, np.conj(psi_qiskit))
    qiskit_rho_d = deshuffle_qiskit(rho_qiskit)

    # Match up to global phase.
    overlap = np.vdot(rho_quimb, qiskit_rho_d)
    assert np.isclose(np.abs(overlap), 1.0, atol=1e-10)
