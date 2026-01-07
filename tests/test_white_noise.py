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

from spin_pulse.environment.noise import WhiteNoiseTimeTrace


@pytest.mark.parametrize(
    "T2S, duration, segment_duration",
    [
        (3, 5000, 1),
        (20, 4000, 1),
    ],
)
def test_white_noise_init(T2S, duration, segment_duration):
    time_trace = WhiteNoiseTimeTrace(T2S, duration, segment_duration)

    assert time_trace.sigma == np.sqrt(2 / T2S)
    assert time_trace.segment_duration == 1
    assert time_trace.T2S == T2S
    assert len(time_trace.values) % segment_duration == 0


def test_white_noise_invalid_segment_duration():
    with pytest.raises(ValueError):
        WhiteNoiseTimeTrace(T2S=5, duration=50, segment_duration=7)


@pytest.mark.parametrize(
    "T2S, duration, segment_duration",
    [
        (3, 50, 1),
        (20, 40, 1),
    ],
)
def test_white_noise_seed(T2S, duration, segment_duration):
    time_trace = WhiteNoiseTimeTrace(T2S, duration, segment_duration, seed=0)
    time_trace2 = WhiteNoiseTimeTrace(T2S, duration, segment_duration, seed=0)
    assert np.array_equal(time_trace.values, time_trace2.values)
    time_trace = WhiteNoiseTimeTrace(T2S, duration, segment_duration)
    time_trace2 = WhiteNoiseTimeTrace(T2S, duration, segment_duration)
    assert not np.array_equal(time_trace.values, time_trace2.values)


@pytest.mark.parametrize(
    "T2S, duration, segment_duration",
    [
        (3, 50, 1),
        (20, 40, 1),
    ],
)
def test_white_plot_ramsey_contrast(T2S, duration, segment_duration):
    time_trace = WhiteNoiseTimeTrace(T2S, duration, segment_duration)
    ramsey_duration = segment_duration
    time_trace.plot_ramsey_contrast(ramsey_duration)
