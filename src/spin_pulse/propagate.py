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
"""Tools to compute unitary time evolution."""

import numpy as np
from scipy.linalg import expm


def propagate(H: list[np.ndarray], coeff: list[list[float]]):  # TODO return typing
    """
    Compute the total unitary evolution operator for a quantum system governed by
    a time-dependent Hamiltonian, expressed as a linear combination of basis Hamiltonians.

    Parameters:
        - H (List[np.ndarray]): List of Hamiltonian matrices [H1, H2, ..., Hn], each of shape (d, d).
        - coeff (List[List[float]]): List of time-dependent coefficients for each Hamiltonian. coeff[j][i] is the coefficient for Hamiltonian H[j] at time step i.

    Returns:
        np.ndarray: The final unitary matrix U of shape (d, d) representing the total time evolution.

    Raises:
        ValueError: If the number of Hamiltonians does not coincide with the number of time-dependent coefficient lists given or if
          the number of coefficients per Hamiltonian is not always the same.

    """
    num_ham: int = len(H)
    num_times: int = len(coeff[0])

    if num_ham != len(coeff):
        raise ValueError(
            f"The number of Hamiltonians ({num_ham}) does not coincide with the number of time-dependent coefficient collections ({len(coeff)}) given."
        )
    for k in range(len(coeff) - 1):
        if len(coeff[k]) != len(coeff[k + 1]):
            raise ValueError(
                f"The number of coefficients given for the {k}-th and {k + 1}-th Hamiltonians is not the same ({len(coeff[k])} against {len(coeff[k + 1])}). Might be due to pulse sequences with diffferent durations in the same pulse layer."
            )

    nh = H[0].shape[0]
    u = np.eye(nh, dtype=complex)
    for i in range(num_times):
        H_tot = sum(coeff[j][i] * H[j] for j in range(num_ham))
        u_i = expm(-1j * H_tot)  # type: ignore
        u = u_i @ u
    return u
