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
"""Helper functions to carry out Ramsey experiments."""

import numpy as np
import qiskit as qi
from qiskit.quantum_info import Operator
from tqdm import tqdm

from ..environment.experimental_environment import ExperimentalEnvironment
from ..transpilation.hardware_specs import HardwareSpecs
from ..transpilation.pulse_circuit import PulseCircuit


def get_ramsey_circuit(
    duration: int,
    hardware_specs: HardwareSpecs,
    exp_env: ExperimentalEnvironment | None = None,
):
    """Construct a pulse-level Ramsey experiment.

    This function builds a single-qubit Ramsey sequence consisting of a
    Hadamard gate, an idle period of a specified duration, and a second
    Hadamard gate. The circuit is transpiled into the hardware native gate
    set and converted into a PulseCircuit. If an experimental environment is
    provided, noise time traces are attached to the resulting pulse-level
    circuit.

    Parameters:
        duration (int): Duration of the free-evolution period (in the discrete
            time unit used by the hardware model).
        hardware_specs (HardwareSpecs): Hardware configuration used to
            transpile the logical Ramsey sequence into native instructions, and
            to generate the pulse sequences of the PulseCircuit.
        exp_env (ExperimentalEnvironment | None): Optional noise environment
            from which time traces are created and attached to the PulseCircuit.

    Returns:
        PulseCircuit: Pulse-level representation of the Ramsey experiment,
        optionally including noise time traces.

    """
    qreg = qi.QuantumRegister(1)
    circ = qi.QuantumCircuit(qreg)
    circ.h(0)
    circ.delay(int(duration))

    circ.h(0)
    isa_circ = hardware_specs.gate_transpile(circ)
    pulse_circuit = PulseCircuit.from_circuit(isa_circ, hardware_specs, exp_env=exp_env)
    return pulse_circuit


def get_contrast(pulse_circuit: PulseCircuit) -> float:
    """Compute the population contrast of a Ramsey experiment.

    The pulse-level circuit is converted back to a unitary qiskit.QuantumCircuit,
    and the resulting unitary matrix is applied to the input state 0.
    The contrast is defined as the population difference between state 0
    and state 1, that is: C = P0 - P1

    Parameters:
        pulse_circuit (PulseCircuit): Pulse-level Ramsey circuit.

    Returns:
        float: Population contrast.

    """

    circ = pulse_circuit.to_circuit()
    unitary = Operator(circ).to_matrix()
    statevector = unitary[:, 0]
    return np.abs(statevector[0]) ** 2 - np.abs(statevector[1]) ** 2


def get_average_ramsey_contrast(
    hardware_specs: HardwareSpecs,
    exp_env: ExperimentalEnvironment,
    durations: list[int],
):
    """Compute the average Ramsey contrast over multiple noise realizations.

    For each free-evolution duration given, a Ramsey pulse circuit is constructed
    and its population contrast is computed by averaging over multiple noise
    realizations drawn from the experimental environment. After each duration,
    the environment time traces are regenerated to ensure independence
    between samples.

    Parameters:
        hardware_specs (HardwareSpecs): Hardware configuration used to
            construct pulse-level Ramsey circuits.
        exp_env (ExperimentalEnvironment): Noise environment providing time
            traces for each sample.
        durations (list[int]): List of free-evolution durations for which the
            Ramsey contrast is evaluated.

    Returns:
        np.ndarray: Array containing the average Ramsey contrast for each
            duration in ``durations``.

    """
    nbp = len(durations)
    average_contrast = np.zeros(nbp)
    for j in tqdm(range(nbp)):
        ramsey_circ = get_ramsey_circuit(durations[j], hardware_specs)
        average_contrast[j] = ramsey_circ.averaging_over_samples(get_contrast, exp_env)
        # regenerate new time traces for the next duration
        exp_env.generate_time_traces()
    return average_contrast
