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


class NoiseTimeTrace:
    """"""

    def __init__(self, duration):
        """

        Args:
            duration: _description_

        Returns:
            _type_: _description_

        """

        self.duration = duration
        self.values = np.zeros(duration)

    def ramsey_contrast(self, ramsey_duration):
        """Performs a Ramsey experiment, ie study the dynamics of <X(t)> for a single qubit initialized in
        0 + 1 and subject to H(t)=omega(t) with t=t_s,...,n_max t_s, over over n_exp=length(time_traces)

        Args:
            time_trace (_type_): _description_
            S_0 (_type_): multiplicative factor to obtain a PSD of S_0/f
            n_max (_type_): _description_

        Returns:
            _type_: _description_

        """
        n_exp = self.duration // ramsey_duration
        contrast = 0.0
        i_min = 0
        for i_exp in range(n_exp):
            omega = self.values[i_min : i_min + ramsey_duration]
            contrast += np.real(np.exp(-1j * np.cumsum(omega))) / n_exp
            i_min += ramsey_duration
        return contrast

    def plot_ramsey_contrast(self, ramsey_duration):
        contrast = self.ramsey_contrast(ramsey_duration)
        plt.plot(contrast, label="numerics", color="blue")
        plt.legend(loc=0)
        plt.xlabel("$t$")
        plt.ylabel("$C$")

    def plot(self, n_max=None):
        if n_max is None:
            n_max = self.duration
        plt.plot(self.values[:n_max])
        plt.xlabel("$t$")
        plt.ylabel(r"$\epsilon(t)$")
