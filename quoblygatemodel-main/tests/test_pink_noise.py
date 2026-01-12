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

from spin_pulse.environment.noise import PinkNoiseTimeTrace


@pytest.mark.parametrize(
    "T2S, duration, segment_duration",
    [
        (3, 50, 10),
        (20, 60, 6),
    ],
)
def test_pink_noise_init(T2S, duration, segment_duration):
    time_trace = PinkNoiseTimeTrace(T2S, duration, segment_duration)
    expected_S0 = 1 / (4 * np.pi**2 * np.log(segment_duration) * T2S**2)

    assert np.isclose(expected_S0, time_trace.S0)
    assert time_trace.T2S == T2S
    assert len(time_trace.values) % segment_duration == 0
    assert isinstance(time_trace.values, np.ndarray)
    assert isinstance(time_trace.sigma, float)


@pytest.mark.parametrize(
    "T2S, duration, segment_duration",
    [
        (3, 50, 10),
        (20, 60, 6),
    ],
)
def test_pink_noise_seed(T2S, duration, segment_duration):
    time_trace = PinkNoiseTimeTrace(T2S, duration, segment_duration, seed=0)
    time_trace2 = PinkNoiseTimeTrace(T2S, duration, segment_duration, seed=0)
    assert np.array_equal(time_trace.values, time_trace2.values)
    time_trace = PinkNoiseTimeTrace(T2S, duration, segment_duration)
    time_trace2 = PinkNoiseTimeTrace(T2S, duration, segment_duration)
    assert not np.array_equal(time_trace.values, time_trace2.values)


@pytest.mark.parametrize(
    "T2S, duration, segment_duration",
    [
        (3, 60, 30),
        (20, 40, 20),
    ],
)
def test_pink_plot_ramsey_contrast(T2S, duration, segment_duration):
    time_trace = PinkNoiseTimeTrace(T2S, duration, segment_duration)
    ramsey_duration = segment_duration
    time_trace.plot_ramsey_contrast(ramsey_duration)
