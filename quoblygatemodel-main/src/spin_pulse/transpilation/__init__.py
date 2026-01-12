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
The `transpilation` module provides a set of classes that enable the simulation of quantum  circuits defined in `Qiskit` on silicon-based spin-qubit hardware models.
The given circuit is first transpiled into the native gate set of the model and then converted into a pulse sequence. This pulse sequence is subsequently integrated numerically in the presence
of a simulated noisy experimental environment, yielding a noisy quantum-circuit representation of the original `Qiskit` circuit.

    - :mod:`spin_pulse.transpilation.hardware_specs`, define the classes `HardwareSpecs`, that defines the hardware specifications for a spin qubit device model, and `Shape` that defines the functional form of the pulse envelope used for control operations in spin-qubit pulse sequences.


    - :mod:`spin_pulse.transpilation.pulse_circuit`, define the class `PulseCircuit` that stores a layered decomposition of a qiskit.QuantumCircuit into PulseLayer objects and, optionally, a stochastic noise environment.


    - :mod:`spin_pulse.transpilation.pulse_layer`, define the class `PulseLayer` that groups single-qubit and two-qubit PulseSequence objects that act over a common time interval.


    - :mod:`spin_pulse.transpilation.pulse_sequence`, define the class `PulseSequence` that is an ordered list of PulseInstruction objects consecutive in time. The class computes the total duration of the sequence, the starting time of each constituent instruction, and provides utilities for plotting.


    - :mod:`spin_pulse.transpilation.dynamical_decoupling`, define the class `DynamicalDecoupling` that identifies the available pulse-based methods used to mitigate phase noise in spin qubit experiments. The selected sequence determines how control pulses are applied during idle periods in order to reduce the effect of low-frequency noise.


The utility functions used in this module are defined in :mod:`spin_pulse.transpilation.utils`.

The :mod:`spin_pulse.transpilation.instructions` module defines the various `PulseInstruction` classes, which represent the low-level operations used to construct `PulseSequence` objects.

The :mod:`spin_pulse.transpilation.passes`, include custom Qiskit transpiler passes used to optimize quantum circuits for spin qubit hardware models.
"""
