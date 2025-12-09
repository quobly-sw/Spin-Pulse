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

import itertools
from typing import Literal

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import qiskit as qi
from qiskit.quantum_info import (
    Chi,
    Operator,
    Pauli,
    PauliList,
    SuperOp,
)
from tqdm import tqdm

from .pulse_circuit import PulseCircuit


def get_single_gate_circuit(
    gate: Literal["rx", "ry", "rz", "delay"],
    theta,
    hardware_specs,
    idle_time=0,
) -> PulseCircuit:
    # TODO
    assert gate in ["rx", "ry", "rz", "delay"], "Wrong gate name"

    qreg = qi.QuantumRegister(1)
    circ = qi.QuantumCircuit(qreg)

    if gate == "delay":
        circ.delay(int(idle_time))
    else:
        getattr(circ, gate)(theta, 0)

    pulse_circuit = PulseCircuit.from_circuit(circ, hardware_specs)

    return pulse_circuit


def get_chan(
    pulse_circ: PulseCircuit,
) -> SuperOp:
    # TODO
    qi_circ = pulse_circ.to_circuit()
    return SuperOp(Operator(qi_circ))


def single_gate_average_channel(gate, theta, hardware_specs, n_exp=None, idle_time=0):
    # TODO
    pulse_circuit = get_single_gate_circuit(
        gate, theta, hardware_specs, idle_time=idle_time
    )
    circuit_duration = pulse_circuit.duration

    if n_exp is None:
        n_exp_ = hardware_specs.time_traces[0].duration // (10 * circuit_duration)
    else:
        n_exp_ = n_exp

    average_channel = SuperOp(Operator(np.zeros((2, 2), dtype=complex)))
    for _ in tqdm(range(n_exp_)):
        pulse_circuit = get_single_gate_circuit(
            gate, theta, hardware_specs, idle_time=idle_time
        )
        matrix = pulse_circuit.to_circuit().data[0].matrix
        average_channel += SuperOp(Operator(matrix)) / n_exp_
    return average_channel


def print_chi_elements(channel):
    # TODO
    chi_matrix = Chi(channel).data

    # Generate the n-qubit Pauli basis
    paulis = ["I", "X", "Y", "Z"]
    pauli_labels = ["".join(p) for p in itertools.product(paulis)]
    pauli_basis = PauliList(pauli_labels)

    # Print non-zero elements with Pauli label indices
    for i, j in itertools.product(range(len(pauli_basis)), repeat=2):
        value = chi_matrix[i, j]
        if np.abs(value) > 1e-10:  # Skip near-zero terms
            re = round(value.real, 6)
            im = round(value.imag, 6)
            print(f"{pauli_basis[i]} ⊗ {pauli_basis[j]}: {re} + {im}j")


def plot_chi_matrix(channels, threshold=None):
    # TODO
    n_qb = int(np.log2(next(iter(channels.values())).data.shape[0]) / 2)
    mpl.rcParams["font.size"] = 22
    fig = plt.figure(figsize=(10, 5))
    # Generate Pauli basis labels
    paulis = ["I", "X", "Y", "Z"]
    pauli_labels = ["".join(p) for p in itertools.product(paulis, repeat=n_qb)]
    full_labels = [f"${p1}.{p2}$" for p1 in pauli_labels for p2 in pauli_labels]

    counter = 0
    lines_style = ["-", "--", ":", "-."]

    x = np.arange(len(full_labels))

    for index, key in enumerate(channels.keys()):
        chi_matrix = Chi(channels[key]).data

        # Flatten matrix into list of values and labels
        values = chi_matrix.flatten()

        if threshold is not None and index == 0:
            indices = [i for i in range(len(values)) if np.abs(values[i]) > threshold]
            x = range(len(indices))
            full_labels = [full_labels[i] for i in indices]
        if threshold is not None:
            values = values[indices]

        if "analytical" in key:
            plt.bar(
                x,
                np.real(values),
                tick_label=full_labels,
                label=f"{key}" + " (real)",
                facecolor="none",
                edgecolor="tab:blue",
                linestyle=lines_style[counter % len(lines_style)],
                linewidth=1.0,
            )
            plt.bar(
                x,
                np.imag(values),
                tick_label=full_labels,
                label=f"{key}" + " (imag)",
                facecolor="none",
                edgecolor="tab:orange",
                linestyle=lines_style[counter % len(lines_style)],
                linewidth=1.0,
            )
            # edgecolor='black'
            counter += 1

        else:
            plt.bar(
                x,
                np.real(values),
                alpha=0.3,
                tick_label=full_labels,
                label=f"{key}" + " (real)",
            )
            plt.bar(
                x,
                np.imag(values),
                alpha=0.3,
                tick_label=full_labels,
                label=f"{key}" + " (imag)",
            )

    plt.xticks(rotation=90)
    plt.ylabel(r"$\chi$")
    plt.legend()
    plt.grid(True, axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    return fig


def pauli_dict_to_channel(pauli_dict):
    """Convert a dictionary of Pauli operator coefficients into a quantum channel.

    Parameters:
        pauli_dict (dict): keys are strings like 'I', 'X', 'YZ', etc.
                           values are real or complex coefficients.

    Returns:
        Chi: Qiskit's Chi object representing the quantum channel.

    """
    keys = list(pauli_dict.keys())
    num_qubits = len(keys[0])  # assumes all keys have same length
    d = 2**num_qubits

    # Build total operator matrix from weighted Pauli operators
    total_op = np.zeros((d, d), dtype=complex)

    for label, coeff in pauli_dict.items():
        P = Pauli(label)
        op = Operator(P).data
        total_op += coeff * op

    # Convert to a SuperOp and then to Chi
    op_channel = SuperOp(total_op)
    # chi = Chi(op_channel)

    return op_channel
