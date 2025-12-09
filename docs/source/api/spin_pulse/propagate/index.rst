spin_pulse.propagate
====================

.. py:module:: spin_pulse.propagate

.. autoapi-nested-parse::

   Tools to compute unitary time evolution.




Functions
---------

.. autoapisummary::

   spin_pulse.propagate.propagate


Module Contents
---------------

.. py:function:: propagate(H, coeff)

   Computes the total unitary evolution operator for a quantum system governed by
   a time-dependent Hamiltonian expressed as a linear combination of basis Hamiltonians.

   :param H: List of Hamiltonian matrices [H1, H2, ..., Hn], each of shape (d, d).
   :type H: List[np.ndarray]
   :param coeff: List of time-dependent coefficients for each Hamiltonian.
   :type coeff: List[List[float]]
   :param coeff[j][i] is the coefficient for Hamiltonian H[j] at time step i.:

   :returns: The final unitary matrix U representing the time evolution over all time steps.
   :rtype: np.ndarray
