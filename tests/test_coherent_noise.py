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

from spin_pulse.noise import CoherentNoiseTimeTrace


@pytest.mark.parametrize(
    "T2, duration, segment_duration",
    [
        (3, 50, 10),
        (20, 40, 5),
    ],
)
def test_coherent_noise_init(T2, duration, segment_duration):
    time_trace = CoherentNoiseTimeTrace(T2, duration, segment_duration)
    assert time_trace.sigma == np.sqrt(2) / (T2)
    assert time_trace.T2 == T2
    assert len(time_trace.values) % segment_duration == 0


# @pytest.mark.filterwarnings("default")
def test_coherent_noise_invalid_segment_duration():
    with pytest.raises(AssertionError):
        CoherentNoiseTimeTrace(T2=5, duration=50, segment_duration=7)


@pytest.mark.parametrize(
    "T2, duration, segment_duration",
    [
        (3, 50, 10),
        (20, 40, 5),
    ],
)
def test_coherent_noise_seed(T2, duration, segment_duration):
    time_trace = CoherentNoiseTimeTrace(T2, duration, segment_duration, seed=0)
    time_trace2 = CoherentNoiseTimeTrace(T2, duration, segment_duration, seed=0)
    assert np.array_equal(time_trace.values, time_trace2.values)
    time_trace = CoherentNoiseTimeTrace(T2, duration, segment_duration)
    time_trace2 = CoherentNoiseTimeTrace(T2, duration, segment_duration)
    assert not np.array_equal(time_trace.values, time_trace2.values)


@pytest.mark.parametrize(
    "T2, duration, segment_duration",
    [
        (3, 50, 25),
        (20, 40, 20),
    ],
)
def test_coherent_plot_ramsey_contrast(T2, duration, segment_duration):
    time_trace = CoherentNoiseTimeTrace(T2, duration, segment_duration)
    ramsey_duration = segment_duration
    time_trace.plot_ramsey_contrast(ramsey_duration)
