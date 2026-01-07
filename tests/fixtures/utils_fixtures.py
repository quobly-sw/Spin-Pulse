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

from unittest.mock import MagicMock, Mock, patch

import pytest


# === Fixtures: dummy hardware and instructions ===
@pytest.fixture
def dummy_hardware_specs():
    """Mock HardwareSpecs with minimal valid attributes."""
    hw = MagicMock()
    hw.ramp_duration = 5
    hw.fields = {"z": 0.8}

    # Dummy rotation generator with from_angle() returning mock instructions
    rotation_generator = MagicMock()
    rotation_generator.from_angle = MagicMock(
        side_effect=lambda axis, qubits, angle, specs: f"{axis}-rotation({angle})"
    )
    hw.rotation_generator = rotation_generator
    return hw


@pytest.fixture
def dummy_idle_instruction():
    """Patch IdleInstruction to return identifiable mock objects."""
    cls = patch("spin_pulse.pulse_utils.IdleInstruction")
    cls.side_effect = lambda qubits, duration: f"Idle(q={qubits},d={duration})"
    return cls


@pytest.fixture
def dummy_square_rotation_instruction():
    """Patch SquareRotationInstruction to return identifiable mock objects."""
    cls = patch("spin_pulse.pulse_utils.SquareRotationInstruction")
    cls.side_effect = lambda axis, qubits, amp, phase, ramp, dur: (
        f"SquareRot({axis},q={qubits},amp={amp},phase={phase},ramp={ramp},dur={dur})"
    )
    return cls


@pytest.fixture
def dummy_pulse_sequence():
    """Patch PulseSequence to make sequences identifiable."""
    cls = patch("spin_pulse.pulse_utils.PulseSequence")
    cls.side_effect = lambda seq: Mock(instructions=seq, duration=len(seq) * 10)
    return cls
