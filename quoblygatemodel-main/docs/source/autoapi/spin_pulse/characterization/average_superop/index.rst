
spin_pulse.characterization.average_superop
===========================================

.. py:module:: spin_pulse.characterization.average_superop

.. autoapi-nested-parse::

   Utilities to analyze and visualize quantum super-Operators.




Functions
---------

.. autoapisummary::

   spin_pulse.characterization.average_superop.compare_circuits
   spin_pulse.characterization.average_superop.plot_chi_matrix
   spin_pulse.characterization.average_superop.get_superop_from_paulidict


Module Contents
---------------


.. py:function:: compare_circuits(circ1, circ2)

   Compare two quantum circuits by plotting the matrix elements of their
   corresponding unitary operators.

   This function converts both circuits into unitary matrices using
   qiskit.quantum_info.Operator.
   The global phase is removed before comparison. Three scatter plots are
   generated: real parts, imaginary parts, and absolute values of the matrix
   elements. A diagonal reference line is shown, and the squared distance
   between the two matrices is displayed.

   :param circ1: First circuit to compare.
   :type circ1: qiskit.QuantumCircuit
   :param circ2: Second circuit to compare.
   :type circ2: qiskit.QuantumCircuit

   .. rubric:: Notes

   The global phase is aligned using the matrix element with maximum magnitude.
   This function is useful to visually validate the equivalence of two circuits
   after transformations such as transpilation or pulse compilation.


.. py:function:: plot_chi_matrix(superop, threshold=None)

   Plot the chi-matrix elements for one or multiple quantum superop.

   The chi-matrix is computed for each channel and plotted as bar plots
   (real and imaginary parts). If a threshold is provided, only elements
   with absolute value greater than the threshold (from the first channel)
   are shown.

   Channels whose key contains the substring ``"analytical"`` are plotted
   with transparent bars and line styles, while the others are plotted as
   semi-transparent filled bars.

   :param superop: Dictionary mapping labels to quantum super-Operator. Each value must
                   be compatible with ``qiskit.quantum_info.Choi``/``Chi`` so that
                   ``Chi(superop[key]).data`` returns the chi-matrix.
   :type superop: dict[str, qiskit.quantum_info.SuperOp or qiskit.quantum_info.Channel]
   :param threshold: If not ``None``, only chi-matrix elements with
                     absolute value greater than ``threshold`` (as determined from the
                     first channel in ``superop``) are included in the plot.
   :type threshold: float | None

   :returns: The figure object containing the chi-matrix plot.
   :rtype: matplotlib.figure.Figure


.. py:function:: get_superop_from_paulidict(pauli_dict)

   Return the SuperOp corresponding to a Pauli decomposition given as
   a dictionary.

   The input is a mapping from tensor-product Pauli labels (e.g., "IXZ",
   "ZZ", "I") to complex coefficients. For an n-qubit system, each label
   must be a string of length n, with characters drawn from
   ``{"I", "X", "Y", "Z"}``.

   The function builds the operator

   .. math::

       O = \sum_{P} c_P P,

   where :math:`P` runs over Pauli strings and :math:`c_P` are the provided
   coefficients, and then wraps it as a ``qiskit.quantum_info.SuperOp``.

   :param pauli_dict: Dictionary mapping Pauli labels
                      (e.g., "IX", "ZZI") to complex coefficients.
   :type pauli_dict: dict[str, complex]

   :returns: The resulting quantum channel represented
             as a ``SuperOp`` acting on the corresponding Hilbert space dimension.
   :rtype: qiskit.quantum_info.SuperOp
