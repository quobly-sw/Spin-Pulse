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
from scipy.linalg import expm

from spin_pulse.transpilation.utils import propagate  # Replace with actual module name


@pytest.fixture
def sample_hamiltonians():
    # Pauli-X and Pauli-Z matrices
    H1 = np.array([[0, 1], [1, 0]], dtype=complex)
    H2 = np.array([[1, 0], [0, -1]], dtype=complex)
    return [H1, H2]


@pytest.fixture
def sample_coefficients():
    # Two time steps
    return [
        [0.5, 0.5],  # Coefficients for H1
        [0.2, 0.3],  # Coefficients for H2
    ]


def test_propagate_unitary_shape(sample_hamiltonians, sample_coefficients):
    U = propagate(sample_hamiltonians, sample_coefficients)
    assert U.shape == (2, 2), "Unitary matrix should be 2x2"


def test_propagate_unitarity(sample_hamiltonians, sample_coefficients):
    U = propagate(sample_hamiltonians, sample_coefficients)
    identity = np.eye(U.shape[0])
    assert np.allclose(U.conj().T @ U, identity), "Matrix should be unitary"


def test_propagate_consistency():
    # Identity Hamiltonian should yield a global phase
    H = [np.eye(2, dtype=complex)]
    coeff = [[np.pi, np.pi]]
    U = propagate(H, coeff)
    expected = expm(-1j * 2 * np.pi * np.eye(2))
    assert np.allclose(U, expected), "Should match expected phase evolution"
