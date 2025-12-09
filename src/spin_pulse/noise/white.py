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

from .noise_time_trace import NoiseTimeTrace


class WhiteNoiseTimeTrace(NoiseTimeTrace):
    def __init__(self, T2, duration, segment_duration, seed: int | None = None):
        """Returns a sequence of N time points

        Parameters:
            N (_type_): _description_

        Returns:
            _type_: _description_

        """
        super().__init__(duration)
        assert segment_duration == 1, "White noise must have segment_duration=1"
        rng = np.random.default_rng(seed=seed)

        self.segment_duration = 1
        self.sigma = np.sqrt(2 / T2)
        self.values = np.zeros(duration)
        x = rng.normal(loc=0.0, scale=1.0, size=duration)
        self.values = self.sigma * x
        self.T2 = T2

    def plot_ramsey_contrast(self, ramsey_duration):
        t = np.arange(ramsey_duration)
        plt.plot(np.exp(-t / self.T2), label="$e^{-t/T_2}$", color="orange")
        super().plot_ramsey_contrast(ramsey_duration)
