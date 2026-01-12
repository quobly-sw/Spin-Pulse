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
from qiskit.quantum_info import Operator, SuperOp

from spin_pulse.characterization.average_superop import (
    compare_circuits,
    get_superop_from_paulidict,
    plot_chi_matrix,
)

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------


def test_compare_circuits():
    circ1 = QuantumCircuit(2)
    circ1.x(0)
    circ1.x(0)
    circ2 = circ1.copy()

    compare_circuits(circ1, circ2)

    # We check that x=y because circ1=circ2
    ax = plt.gca()
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    assert (xmax - xmin) == pytest.approx(ymax - ymin)


# ----------------------------------------------------------------------
# Tests for plot_chi_matrix
# ----------------------------------------------------------------------


def _make_simple_channel():
    # Return a simple 1-qubit identity-like channel.
    u = Operator(np.eye(2))
    return SuperOp(u)


def test_plot_chi_matrix_with_threshold():
    # Test the branch with threshold != None and analytical/non-analytical keys.
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
    # Test the branch with threshold == None.
    chan = _make_simple_channel()
    channels = {"numerical_id": chan}

    fig = plot_chi_matrix(channels, threshold=None)

    assert fig is not None
    plt.close(fig)


# ----------------------------------------------------------------------
# Tests for get_superop_from_paulidict
# ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "pauli_dict", [{"II": (1 + 0.2) / 2, "ZZ": (1 - 0.2) / 2}, {"IZ": 1.0}]
)
def test_get_superop_from_paulidict_two_qubits(pauli_dict):
    op_channel = get_superop_from_paulidict(pauli_dict)

    assert isinstance(op_channel, SuperOp)
    assert op_channel.data.shape == (4, 4)


@pytest.mark.parametrize(
    "pauli_dict", [{"IIII": (1 + 0.2) / 2, "XXZZ": (1 - 0.2) / 2}, {"IZZZ": 1.0}]
)
def test_get_superop_from_paulidict_four_qubits(pauli_dict):
    op_channel = get_superop_from_paulidict(pauli_dict)

    assert isinstance(op_channel, SuperOp)
    assert op_channel.data.shape == (16, 16)


@pytest.mark.parametrize(
    "pauli_dict",
    [
        {"III": (1 + 0.2) / 2, "X": (1 - 0.2) / 2},
        {"IZZ": 1.0},
        {"XYY": 0.5, "ZZX": 0.5},
    ],
)
def test_get_superop_from_paulidict_error(pauli_dict):
    with pytest.raises(ValueError):
        get_superop_from_paulidict(pauli_dict)
