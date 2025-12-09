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


class CoherentNoiseTimeTrace(NoiseTimeTrace):
    def __init__(self, T2, duration, segment_duration, seed: int | None = None):
        """Returns a sequence of N time points h(t), t=t_s,..,t_s&N, parametrized
        by a spectral density S_f=S0/(ft_s)^beta
        where f=[1/(Nt_s),...,1/(t_s)]
        The sampling time does not need to be specified

        Parameters:
            N (_type_): _description_
            beta (_type_): _description_
            normalize (bool, optional): _description_. Defaults to False.
            randpower (bool, optional): _description_. Defaults to False.
            seed (int): Seed integer for random generator
        Returns:
            _type_: _description_

        """
        super().__init__(duration)

        self.segment_duration = segment_duration
        assert duration % segment_duration == 0, (
            "segment_duration must be commensurate with duration"
        )
        repeat = duration // segment_duration

        self.sigma = np.sqrt(2) / (T2)
        self.T2 = T2
        self.values = np.zeros(duration)
        rng = np.random.default_rng(seed=seed)
        for i in range(repeat):
            self.values[i * segment_duration : (i + 1) * segment_duration] = (
                self.sigma * rng.normal(loc=0.0, scale=1.0) * np.ones(segment_duration)
            )

    def plot_ramsey_contrast(self, ramsey_duration: int):
        # TODO
        t = np.arange(ramsey_duration)
        plt.plot(np.exp(-(t**2) / self.T2**2), label="$e^{-t^2/T_2^2}$", color="orange")
        super().plot_ramsey_contrast(ramsey_duration)
