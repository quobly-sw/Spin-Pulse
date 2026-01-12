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
"""
:mod:`SpinPulse` is an open-source python package for simulating silicon based spin qubits at the pulse-level.

Modules
----------------
:mod:`spin_pulse.transpilation`
    The `transpilation` module provides a set of classes that enable the simulation of quantum circuits defined in `Qiskit` on silicon-based spin-qubit hardware models.

:mod:`spin_pulse.environment`
    The `environment` module provides a set of classes for defining and configuring a quantum experimental environment tailored to spin-qubit systems.

:mod:`spin_pulse.characterization`
    The `characterization` module provides a set of functions for characterizing spin-qubit control operations and quantifying noise strength.

"""

from .environment.experimental_environment import ExperimentalEnvironment
from .transpilation.dynamical_decoupling import DynamicalDecoupling
from .transpilation.hardware_specs import HardwareSpecs, Shape
from .transpilation.pulse_circuit import PulseCircuit

__all__ = [
    "DynamicalDecoupling",
    "ExperimentalEnvironment",
    "HardwareSpecs",
    "PulseCircuit",
    "Shape",
]
