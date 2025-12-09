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
"""Description of the hardware to simulate circuit execution."""

from enum import Enum

from qiskit import QuantumCircuit
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit.transpiler import (
    PassManager,
    generate_preset_pass_manager,
)
from qiskit.transpiler.passes import Optimize1qGatesDecomposition

from .instructions import (
    GaussianRotationInstruction,
    RotationInstruction,
    SquareRotationInstruction,
)
from .passes.rzz_echo import RZZEchoPass


class Shape(Enum):
    GAUSSIAN = "gaussian"
    SQUARE = "square"


class HardwareSpecs:
    """
    TODO:: describe attributes and class.
    """

    rotation_generator: type[RotationInstruction]

    def __init__(
        self,
        num_qubits: int,
        B_field: float,
        delta: float,
        J_coupling: float,
        rotation_shape: Shape,
        ramp_duration: int = 1,
        coeff_duration: int = 5,
        dynamical_decoupling=None,
        optim: int = 0,
    ):
        """
        Initialize the HardwareSpecs object that defines the hardware specifications.

        Parameters:
            - num_qubits (int): Number of qubits considered.
            - B_field (float): Maximal magnetic field strength.
            - delta (float): Maximal energy difference between two qubits.
            - J_coupling (float): Maximal coupling strength between two qubit.
            - rotation_shape (Shape): Pulse shape used for qubit manipulation.
            - ramp_duration (int, optional): Duration of the pulse ramp for square pulse. Default is 1.
            - coeff_duration (int, optional): Duration coefficient for Gaussian pulses. Default is 5.
            - dynamical_decoupling (str, optional): If not None, defines the dynamical decoupling sequence to be applied to Idle qubits.

        """

        self.num_qubits: int = num_qubits
        self.J_coupling: float = J_coupling

        if num_qubits > 1:
            coupling_map = [(i, i + 1) for i in range(num_qubits - 1)]
        else:
            coupling_map = None
        if num_qubits > 1:
            basis_gates = ["rx", "ry", "rz", "rzz"]
        else:
            basis_gates = ["rx", "ry", "rz"]
        backend: GenericBackendV2 = GenericBackendV2(
            num_qubits=num_qubits, coupling_map=coupling_map, basis_gates=basis_gates
        )

        assert B_field > 10 ** (-3), (
            f"B_field too low, must be greater than 10^{-3}, here B_field={B_field}"
        )
        assert delta > 10 ** (-3), (
            f"delta too low, must be greater than 10^{-3}, here delta={delta}"
        )
        assert J_coupling > 10 ** (-3), (
            f"J_coupling too low, must be greater than 10^{-3}, here J_coupling={J_coupling}"
        )
        fields = {"x": B_field, "y": B_field, "Heisenberg": J_coupling, "z": delta}
        self.fields: dict[str, float] = fields

        self.rotation_shape: Shape = rotation_shape
        match self.rotation_shape:
            case Shape.GAUSSIAN:
                self.rotation_generator = GaussianRotationInstruction
                self.coeff_duration = coeff_duration
            case Shape.SQUARE:
                self.rotation_generator = SquareRotationInstruction
            case _:
                raise ValueError(f"{rotation_shape} not currently available")

        self.ramp_duration: int = ramp_duration

        self.first_pass = generate_preset_pass_manager(
            target=backend.target, optimization_level=optim
        )
        self.second_pass = PassManager(
            [RZZEchoPass(), Optimize1qGatesDecomposition(target=backend.target)]
        )

        self.dynamical_decoupling = dynamical_decoupling

    def gate_transpile(self, circ: QuantumCircuit) -> QuantumCircuit:
        """Transpile a quantum circuit into an ISA circuit using hardware specifications.

        Parameters:
            - circ (qiskit.QuantumCircuit): The quantum circuit to be converted.

        Returns:
            qiskit.QuantumCircuit: The ISA quantum circuit composed of spin qubit native gates.

        """
        both_passes = PassManager(
            [
                self.first_pass.to_flow_controller(),
                self.second_pass.to_flow_controller(),
            ]
        )
        return both_passes.run(circ)

    def __str__(self):
        """
        Return a string representation of the HardwareSpecs instance.

        Includes:
            - Number of qubits.
            - B_field, delta and J_coupling values.
            - Shape of manipulation pulses.
            - Pulse ramp duration for square pulse.
            - Duration coefficient for Gaussian pulses if the pulses are Gaussian, otherwise N/A.
            - Dynamical decoupling sequence chosen. None if no dynamical decoupling.
        """
        summary = [
            "HardwareSpec:",
            f"num_qubits: {self.num_qubits}",
            f"B_field: {self.fields['x']}",
            f"delta: {self.fields['z']}",
            f"J_coupling: {self.fields['Heisenberg']}",
            f"rotation_shape: {self.rotation_shape}",
            f"ramp_duration: {self.ramp_duration}",
            f"coeff_duration: {getattr(self, 'coeff_duration', 'N/A')}",
            f"dynamical_decoupling: {self.dynamical_decoupling}",
        ]

        return "\n".join(summary)
