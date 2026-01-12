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

from spin_pulse.environment.noise import NoiseTimeTrace


def test_init_ramsey_contrast():
    duration = 10
    ramsey_duration = 10

    noise_trace = NoiseTimeTrace(duration)
    assert noise_trace.duration == duration

    contrast = noise_trace.ramsey_contrast(ramsey_duration)

    assert np.issubdtype(contrast.dtype, np.floating)

    noise_trace.plot_ramsey_contrast(ramsey_duration)
    noise_trace.plot()
