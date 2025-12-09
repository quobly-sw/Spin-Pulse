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


def get_pink_noise(segment_duration, seed: int | None = None):
    """Returns a sequence of duration time points h(t), t=t_s,..,t_s&N, parametrized
    by a spectral density S_freq=1/(freq)
    where freq=[1/(segment_duration),...,1]
    Args:
        duration (): # TODO
        segment_duration (): # TODO
        seed (int): seed integer for random generator
    Returns:
        _type_: _description_

    """
    rng = np.random.default_rng(seed=seed)
    N = segment_duration
    N2 = N // 2 - 1
    f = np.arange(2, N2 + 2)
    beta = 1.0
    A2 = 1 / (f ** (beta / 2))
    p2 = (rng.uniform(size=N2) - 0.5) * 2 * np.pi
    d2 = A2 * np.exp(1j * p2)
    d = np.concatenate(([0], d2, [1 / ((N2 + 2) ** beta)], np.flipud(np.conj(d2))))
    x = np.real(np.fft.ifft(d))
    return N * x


def get_pink_noise_with_repetitions(
    duration, segment_duration, seed: int | None = None
):
    """Returns a sequence of duration time points h(t), t=t_s,..,t_s&N, parametrized
    by a spectral density S_freq=1/(freq)
    where freq=[1/(N),...,1], with a frequency cutoff of fmin=1/segment_duration
    Parameters:

    Returns:
        _type_: _description_

    """
    segments = []
    total_len = 0

    while total_len < duration:
        segment = get_pink_noise(segment_duration, seed)
        segments.append(segment)
        total_len += len(segment)

    # Concatenate all segments and trim to exact length
    return np.concatenate(segments)[:duration]


class PinkNoiseTimeTrace(NoiseTimeTrace):
    def __init__(self, T2, duration, segment_duration, seed: int | None = None):
        """Returns a sequence of N=duration time points h(t), t=t_s,..,t_s&N, parametrized
        by a spectral density S_f=1/(ft_s), with a frequency cutoff of fmin=1/segment_duration
        Parameters:

        Returns:
            _type_: _description_

        """
        super().__init__(duration)

        self.segment_duration = segment_duration

        S0 = 1 / (4 * np.pi**2 * np.log(segment_duration) * T2**2)

        self.values = (
            2
            * np.pi
            * np.sqrt(S0)
            * get_pink_noise_with_repetitions(duration, segment_duration, seed)
        )

        self.S0 = S0
        self.T2 = T2

        self.sigma = np.std(
            np.asarray(self.values), ddof=0
        )  # ddof=0 for population std deviation

    def plot_ramsey_contrast(self, ramsey_duration):
        t = np.arange(ramsey_duration)
        plt.plot(
            np.exp(-(t**2) / self.T2**2), label=" $e^{-t^2/T_2^2}$", color="orange"
        )
        T2_y = self.T2 / np.sqrt(
            np.log(self.segment_duration / t[1:]) / np.log(self.segment_duration)
        )
        plt.plot(
            t[1:],
            np.exp(-(t[1:] ** 2) / T2_y**2),
            label="$e^{-t^2/T_2^2(t)}$",
            color="green",
        )
        super().plot_ramsey_contrast(ramsey_duration)
