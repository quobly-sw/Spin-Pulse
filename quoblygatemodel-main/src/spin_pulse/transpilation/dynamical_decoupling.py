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
"""Description of dynamical decoupling."""

from enum import Enum


class DynamicalDecoupling(Enum):
    """Enumeration of supported dynamical decoupling sequences.

    This enumeration identifies the available pulse-based methods used to
    mitigate phase noise in spin qubit experiments. The selected sequence
    determines how control pulses are applied during idle periods in order
    to reduce the effect of low-frequency noise.

    Attributes:
        - FULL_DRIVE: Continuous driving of the qubit during the idle period.
        - SPIN_ECHO: Single refocusing pulse applied at the midpoint of the
          idle period.

    """

    FULL_DRIVE = "full_drive"
    SPIN_ECHO = "spin_echo"
