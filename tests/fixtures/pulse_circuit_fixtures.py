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

import pytest
from qiskit.circuit import Qubit

import tests.fixtures.dummy_objects as dm
from spin_pulse import DynamicalDecoupling


@pytest.fixture
def two_qubits():
    # Build two Qiskit Qubit objects that have a stable ._index
    # qc = QuantumCircuit(2)
    # qc.qubits already have indices 0,1 and an attribute .index, but ._index may differ.
    # We'll simulate by attaching ._index manually.
    q0 = Qubit()
    q1 = Qubit()
    return [q0, q1]


@pytest.fixture
def pulse_layers(two_qubits):
    # first layer duration 5, second duration 7
    l1 = dm.DummyPulseLayer(two_qubits, duration=5)
    l2 = dm.DummyPulseLayer(two_qubits, duration=7)
    return [l1, l2]


@pytest.fixture
def hw_no_dd():
    return dm.DummyHardwareSpecs(dynamical_decoupling=None)


@pytest.fixture
def hw_with_dd():
    return dm.DummyHardwareSpecs(dynamical_decoupling=DynamicalDecoupling.FULL_DRIVE)
