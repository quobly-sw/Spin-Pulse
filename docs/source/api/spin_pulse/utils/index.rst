spin_pulse.utils
================

.. py:module:: spin_pulse.utils

.. autoapi-nested-parse::

   Utility functions to interact with circuits.




Functions
---------

.. autoapisummary::

   spin_pulse.utils.compare
   spin_pulse.utils.gate_to_pulse_sequences


Module Contents
---------------

.. py:function:: compare(circ1, circ2, ignore1 = True, ignore2 = True)

   Compare two quantum circuits by plotting the matrix elements of their
   corresponding unitary operators.

   This function converts both circuits into unitary matrices using
   ``qiskit.quantum_info.Operator`` and optionally ignores their layout.
   The global phase is removed before comparison. Three scatter plots are
   generated: real parts, imaginary parts, and absolute values of the matrix
   elements. A diagonal reference line is shown, and the squared distance
   between the two matrices is displayed.

   :param circ1: First circuit to compare.
   :type circ1: QuantumCircuit
   :param circ2: Second circuit to compare.
   :type circ2: QuantumCircuit
   :param ignore1: If True, ignore the layout when converting ``circ1``.
   :type ignore1: bool
   :param ignore2: If True, ignore the layout when converting ``circ2``.
   :type ignore2: bool

   .. rubric:: Notes

   The global phase is aligned using the matrix element with maximum magnitude.
   This function is useful to visually validate the equivalence of two circuits
   after transformations such as transpilation or pulse compilation.


.. py:function:: gate_to_pulse_sequences(gate, hardware_specs)

   Translate a Qiskit gate (RX, RY, RZ, or RZZ) into hardware-compatible
   pulse sequences.

   This function maps high-level Qiskit rotation gates into low-level pulse
   instructions that follow the hardware specifications. Single-qubit rotations
   generate a single PulseSequence. While the ``rzz`` interaction generate two
   qubit sequence, followed by a single qubit sequence one each qubits.

   :param gate: The Qiskit instruction to translate.
                Supported operations are ``rx``, ``ry``, ``rz``, ``rzz`` and ``delay``.
   :type gate: CircuitInstruction
   :param hardware_specs: Hardware configuration including available
                          fields, ramp durations, and rotation generation routines.
   :type hardware_specs: HardwareSpecs

   :returns:     A pair of lists:
                 * one-qubit pulse sequences generated from the gate,
                 * two-qubit pulse sequences (only for ``rzz``).
   :rtype: tuple[list[PulseSequence], list[PulseSequence]]

   :raises ValueError: If the gate type is not supported.

   .. rubric:: Notes

   For ``rzz`` gates:
       * A central Heisenberg pulse is generated.
       * Pre/post idle ramps are added to ensure smooth pulse shaping.
       * Each qubit receives a compensating detuned Z rotation of equal duration.

   For ``delay`` gates:
       A single IdleInstruction is wrapped in a PulseSequence.

   For single-qubit rotations:
       The corresponding rotation generator in ``hardware_specs`` is invoked.
