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

from unittest.mock import MagicMock, patch

import matplotlib.pyplot as plt
import numpy as np

import tests.fixtures.dummy_objects as dm
from spin_pulse import DynamicalDecoupling
from spin_pulse.transpilation.instructions import IdleInstruction

# --------------------------------------------------------------------
# TESTS
# --------------------------------------------------------------------


def test_init_sets_name_and_duration_and_qubits():
    q = dm.DummyQubit(idx=3)
    idle = IdleInstruction([q], duration=7)

    # duration, name, qubits
    assert idle.duration == 7
    assert idle.name == "delay"
    assert idle.qubits[0] is q
    assert idle.qubits[0]._index == 3

    as_text = str(idle)
    assert "IdlePulse" in as_text
    assert "duration=7" in as_text
    assert as_text.strip().startswith("IdlePulse")


def test_adjust_duration_mutates_duration_in_place():
    q = dm.DummyQubit()
    idle = IdleInstruction([q], duration=5)
    idle.adjust_duration(11)
    assert idle.duration == 11
    # re-change to ensure it's not write-once
    idle.adjust_duration(1)
    assert idle.duration == 1


def test_plot_calls_matplotlib_with_expected_line_segments():
    q = dm.DummyQubit()
    idle = IdleInstruction([q], duration=4)

    fig, ax = plt.subplots()
    with patch.object(ax, "plot") as mock_plot:
        idle.plot(ax=ax, t_start=10, label_gates=False)

        mock_plot.assert_called_once()
        x_arg, y_arg = mock_plot.call_args[0]

        assert x_arg == [10, 10 + 4 - 1]
        assert y_arg == [0, 0]

        assert "color" in mock_plot.call_args.kwargs
        assert mock_plot.call_args.kwargs["color"] == "k"

    plt.close(fig)


def test_plot_without_ax_uses_gca():
    q = dm.DummyQubit()
    idle = IdleInstruction([q], duration=3)

    fake_ax = MagicMock()
    with (
        patch(
            "spin_pulse.transpilation.instructions.idle.plt.gca", return_value=fake_ax
        ),
        patch.object(fake_ax, "plot") as mock_plot,
    ):
        idle.plot(ax=None, t_start=2, label_gates=True)

        mock_plot.assert_called_once()
        x_arg, y_arg = mock_plot.call_args[0]
        assert x_arg == [2, 2 + 3 - 1]
        assert y_arg == [0, 0]


def test_to_hamiltonian_returns_zero_hamiltonian_and_zero_times():
    q = dm.DummyQubit()
    idle = IdleInstruction([q], duration=5)

    H, t = idle.to_hamiltonian()

    assert isinstance(H, np.ndarray)
    assert H.shape == (2, 2)
    assert np.allclose(H, 0.0)

    assert isinstance(t, np.ndarray)
    assert t.shape == (idle.duration,)
    assert np.allclose(t, 0.0)

    assert not np.isnan(H).any()
    assert not np.isnan(t).any()


# --------------------------------------------------------------------
# to_dynamical_decoupling()
# --------------------------------------------------------------------


def test_dd_mode_none_returns_self_only():
    hw = dm.DummyHardwareSpecs(rot_duration=2, dynamical_decoupling=None)
    q = dm.DummyQubit()
    idle = IdleInstruction([q], duration=10)

    seq = idle.to_dynamical_decoupling(hw)
    assert isinstance(seq, list)
    assert len(seq) == 1
    assert seq[0] is idle

    assert hw.rotation_generator.calls == []


def test_dd_mode_spin_echo_enough_time_happy_path():
    hw = dm.DummyHardwareSpecs(
        rot_duration=3, dynamical_decoupling=DynamicalDecoupling.SPIN_ECHO
    )
    q = dm.DummyQubit(idx=7)
    idle = IdleInstruction([q], duration=20)

    seq = idle.to_dynamical_decoupling(hw)
    assert len(seq) == 4

    idle1, x1, idle2, x2 = seq

    assert isinstance(idle1, IdleInstruction)
    assert isinstance(idle2, IdleInstruction)

    assert hasattr(x1, "axis") and x1.axis == "x"
    assert hasattr(x2, "axis") and x2.axis == "x"
    assert np.isclose(x1.angle, np.pi)
    assert np.isclose(x2.angle, np.pi)

    assert x1.qubits[0] is q
    assert x2.qubits[0] is q

    # duration_idle = int((20 - 2*3)//2) = int((20-6)//2)=int(14//2)=7
    assert idle1.duration == 7
    assert idle2.duration == 7

    assert len(hw.rotation_generator.calls) == 2
    for axis, angle, qubits in hw.rotation_generator.calls:
        assert axis == "x"
        assert np.isclose(angle, np.pi)
        assert qubits == (q,)


def test_dd_mode_spin_echo_not_enough_time_returns_self():
    hw = dm.DummyHardwareSpecs(
        rot_duration=10, dynamical_decoupling=DynamicalDecoupling.SPIN_ECHO
    )  # X_duration = 10
    q = dm.DummyQubit()
    idle = IdleInstruction([q], duration=15)

    seq = idle.to_dynamical_decoupling(hw)

    assert len(seq) == 1
    assert seq[0] is idle

    assert len(hw.rotation_generator.calls) == 2


def test_dd_mode_full_drive_with_positive_loops():
    hw = dm.DummyHardwareSpecs(
        rot_duration=4, dynamical_decoupling=DynamicalDecoupling.FULL_DRIVE
    )
    q = dm.DummyQubit()
    idle = IdleInstruction([q], duration=10)

    seq = idle.to_dynamical_decoupling(hw)
    assert len(seq) == 1
    instr = seq[0]

    assert len(hw.rotation_generator.calls) >= 2

    expected_n_loops = idle.duration // hw.rotation_generator.base_duration
    expected_angle = 2 * np.pi * expected_n_loops

    assert np.isclose(instr.angle, expected_angle)
    assert instr.duration == idle.duration  # doit avoir été ajusté
    assert instr.qubits[0] is q
    assert instr.axis == "x"


def test_dd_mode_full_drive_zero_loops_returns_self():
    hw = dm.DummyHardwareSpecs(
        rot_duration=20, dynamical_decoupling=DynamicalDecoupling.FULL_DRIVE
    )  # twopi duration = 20
    q = dm.DummyQubit()
    idle = IdleInstruction([q], duration=5)  # 5 // 20 = 0 loops

    seq = idle.to_dynamical_decoupling(hw)
    assert len(seq) == 1
    assert seq[0] is idle
    assert len(hw.rotation_generator.calls) >= 1


def test_dd_mode_unknown_is_treated_like_none():
    hw = dm.DummyHardwareSpecs(dynamical_decoupling="totally_weird_mode")
    q = dm.DummyQubit()
    idle = IdleInstruction([q], duration=10)

    result = idle.to_dynamical_decoupling(hw)

    assert result is None
