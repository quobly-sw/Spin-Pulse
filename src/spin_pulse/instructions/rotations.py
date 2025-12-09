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
"""Description of rotations at the pulse level."""

import matplotlib.pyplot as plt
import numpy as np
from qiskit.quantum_info import Pauli

from .pulse_instruction import PulseInstruction

MAX_DURATION = 5e4
MAX_ITER = 1e5


class RotationInstruction(PulseInstruction):
    def __init__(self, name, qubits, duration):
        """
        Initialize a RotatingInstruction with GeneratingOperator name, number of pulses n_pulses of angle angle

        Parameters:
        - ..: ..

        """
        super().__init__(qubits, duration)
        self.name = name

    @classmethod
    def from_angle(cls, name, qubits, angle, hardware_specs):
        raise NotImplementedError

    def eval(self, t):
        raise NotImplementedError

    def to_pulse(self):
        t_rel = np.arange(self.duration)
        pulse = self.eval(t_rel)
        if hasattr(self, "distort_factor"):
            pulse += pulse * self.distort_factor
        return pulse

    def to_angle(self):
        return sum(self.to_pulse())

    def to_hamiltonian(self):
        coeff = self.to_pulse()
        name = self.name
        if name == "x":
            H = 0.5 * Pauli("X").to_matrix()
        elif name == "y":
            H = 0.5 * Pauli("Y").to_matrix()
        elif name == "z":
            H = 0.5 * Pauli("Z").to_matrix()
        elif name == "Heisenberg":
            H = 0.5 * (
                Pauli("XX").to_matrix()
                + Pauli("YY").to_matrix()
                + Pauli("ZZ").to_matrix()
            )

        return H, coeff

    def adjust_duration(self, duration):
        angle = self.to_angle()
        self.duration = duration
        self.amplitude = 1
        angle_1 = self.to_angle()

        self.amplitude = np.abs(angle) / np.abs(angle_1)

    def plot(self, ax=None, t_start=0, label_gates=True):
        if ax is None:
            ax = plt.gca()

        name = self.name
        color_dict = {
            "x": "brown",
            "y": "brown",
            "z": "deepskyblue",
            "Heisenberg": "deepskyblue",
        }

        a = self.to_angle() / np.pi
        if np.abs(a - 1) < 1e-10:
            latex_str = r" $\pi$"
        elif np.abs(a + 1) < 1e-10:
            latex_str = r" $-\pi$"
        elif np.abs(1 / a - round(1 / a)) < 1e-10:
            if a > 0:
                latex_str = rf" $\frac{{\pi}}{{{abs(round(1 / a))}}}$"
            else:
                latex_str = rf" $-\frac{{\pi}}{{{abs(round(1 / a))}}}$"
        else:
            latex_str = " {:.1f}".format(a) + r"$\pi$"

        ax.fill_between(
            range(t_start, t_start + self.duration),
            self.to_pulse(),
            0,
            color=color_dict[name],
            alpha=0.5,
            lw=2,
        )
        if label_gates:
            ax.set_title(ax.get_title() + " " + name + latex_str, color="#24185E")


class SquareRotationInstruction(RotationInstruction):
    def __init__(self, name, qubits, amplitude, sign, ramp_duration, duration):
        """
        Initialize a Square RotatingInstruction with GeneratingOperator: name, and total angle: angle, and n pulses
        Parameters:
        - ..: ..
        """
        super().__init__(name, qubits, duration)
        self.amplitude = amplitude
        self.sign = sign
        self.ramp_duration = ramp_duration
        self.duration = int(duration)
        plateau_duration = duration - 2 * ramp_duration
        if plateau_duration < 0:
            print("error negative plateau duration")

    @classmethod
    def from_angle(cls, name, qubits, angle, hardware_specs):
        sign = np.sign(angle)
        ramp_duration = hardware_specs.ramp_duration

        # Evaluating the smallest pulse_duration available
        # duration = 2 * ramp_duration + 1
        low_duration = 2 * ramp_duration + 1
        high_duration = MAX_DURATION
        cpt = 0
        while cpt < MAX_ITER and low_duration <= high_duration:
            duration = low_duration + (high_duration - low_duration) // 2
            amplitude_1 = 1
            instruction = cls(name, qubits, amplitude_1, sign, ramp_duration, duration)
            angle_1 = instruction.to_angle()
            if np.abs(angle_1) > 1e-15:
                amplitude = np.abs(angle) / np.abs(angle_1)
            else:
                amplitude = 1
            if amplitude < hardware_specs.fields[name] + 1e-10:
                high_duration = duration - 1
            else:
                low_duration = duration + 1
            cpt += 1
        err = np.abs(amplitude - hardware_specs.fields[name])

        # checking the actual best case
        next_duration = duration + 1
        next_instruction = cls(
            name, qubits, amplitude_1, sign, ramp_duration, next_duration
        )
        angle_1 = next_instruction.to_angle()
        if np.abs(angle_1) > 1e-15:
            next_amplitude = np.abs(angle) / np.abs(angle_1)
        else:
            next_amplitude = 1
        next_err = np.abs(next_amplitude - hardware_specs.fields[name])

        previous_duration = duration - 1
        previous_instruction = cls(
            name, qubits, amplitude_1, sign, ramp_duration, previous_duration
        )
        angle_1 = previous_instruction.to_angle()
        if np.abs(angle_1) > 1e-15:
            previous_amplitude = np.abs(angle) / np.abs(angle_1)
        else:
            previous_amplitude = 1
        previous_err = np.abs(previous_amplitude - hardware_specs.fields[name])

        if next_err < err and next_err < previous_err:
            duration = next_duration
            amplitude = next_amplitude
        elif previous_err < next_err and previous_err < err:
            duration = previous_duration
            amplitude = previous_amplitude

        instruction = cls(name, qubits, amplitude, sign, ramp_duration, duration)

        return instruction

    def eval(self, t):
        height = self.sign * self.amplitude
        plateau_duration = self.duration - 2 * self.ramp_duration
        if not self.ramp_duration:  # "pure" square?
            return height * (t < self.duration)
        else:
            t1 = 0
            t2 = t1 + self.ramp_duration
            t3 = t2 + plateau_duration
            t4 = t3 + self.ramp_duration
            y_rise = height * (t / t2) * (t < t2)
            y_constant = height * (t >= t2) * (t < t3)
            y_fall = height * (1 + ((t3 - t - 1) / t2)) * (t >= t3) * (t < t4)
            return y_rise + y_constant + y_fall

    def __str__(self):
        """
        Provide a string representation of the PulseDuration object.

        Returns:
        - str: A formatted string describing the PulseDuration object.

        """
        return f"SquarePulse for {self.name}, amplitude={self.amplitude}, duration={self.duration} "


class GaussianRotationInstruction(RotationInstruction):
    def __init__(self, name, qubits, amplitude, sign, coeff_duration, duration):
        """
        Initialize a Gaussian RotatingInstruction with GeneratingOperator name, and total angle angle, and n pulses
        Parameters:
        - ..: ..
        """
        super().__init__(name, qubits, duration=int(duration))
        self.amplitude = amplitude
        self.coeff_duration = coeff_duration
        self.sign = sign

    @classmethod
    def from_angle(cls, name, qubits, angle, hardware_specs):
        sign = np.sign(angle)

        # Evaluating the smallest pulse_duration available
        prev_duration = -1
        prev_low = -1
        prev_high = -1
        low_duration = 1
        high_duration = MAX_DURATION
        cpt = 0

        assert hardware_specs.fields[name] > 10 ** (-3), (
            f"Hardware specs for pulse amplitude to low: amplitude={hardware_specs.fields[name]}"
        )

        while cpt < MAX_ITER and low_duration <= high_duration:
            duration = low_duration + (high_duration - low_duration) // 2

            if (
                duration == prev_duration
                and low_duration == prev_low
                and high_duration == prev_high
            ):
                break

            prev_duration = duration
            prev_low = low_duration
            prev_high = high_duration

            amplitude_1 = 1
            instruction = cls(
                name, qubits, amplitude_1, sign, hardware_specs.coeff_duration, duration
            )
            angle_1 = instruction.to_angle()
            if np.abs(angle_1) > 1e-15:
                amplitude = np.abs(angle) / np.abs(angle_1)
            else:
                amplitude = high_duration
            if amplitude < hardware_specs.fields[name] + 1e-10:
                high_duration = duration - 1
            else:
                low_duration = duration + 1
            cpt += 1

        if cpt >= MAX_ITER:
            print(
                f"Warning: maximum of iterations reached for angle={angle}, duration={duration}"
            )

        instruction = cls(
            name, qubits, amplitude, sign, hardware_specs.coeff_duration, duration
        )

        return instruction

    def eval(self, t):
        sigma = self.duration / self.coeff_duration
        t0 = self.duration / 2
        return self.sign * self.amplitude * np.exp(-((t - t0) ** 2) / (2 * sigma**2))

    def __str__(self):
        """
        Provide a string representation of the PulseDuration object.

        Returns:
        - str: A formatted string describing the PulseDuration object.

        """
        return f"GaussianPulse for {self.name}, amplitude={self.amplitude}, duration={self.duration} "
