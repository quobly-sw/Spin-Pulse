
spin_pulse.transpilation.utils
==============================

.. py:module:: spin_pulse.transpilation.utils

.. autoapi-nested-parse::

   Utility functions to interact with circuits.




Functions
---------

.. autoapisummary::

   spin_pulse.transpilation.utils.gate_to_pulse_sequences
   spin_pulse.transpilation.utils.propagate
   spin_pulse.transpilation.utils.deshuffle_qiskit
   spin_pulse.transpilation.utils.qiskit_to_quimb
   spin_pulse.transpilation.utils.my_quimb_fidelity


Module Contents
---------------


.. py:function:: gate_to_pulse_sequences(gate, hardware_specs)

   Translate a Qiskit gate (`RX`, `RY`, `RZ`, or `RZZ`) into hardware-compatible
   pulse sequences.

   This function maps high-level Qiskit rotation gates into low-level pulse
   instructions that follow the hardware specifications. Single-qubit rotations
   generate a single PulseSequence, while the ``rzz`` interaction generate two
   qubit sequence followed by a single qubit sequence on each qubit.

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


.. py:function:: propagate(H, coeff)

   Compute the total unitary evolution operator for a quantum system governed by
   a time-dependent Hamiltonian, expressed as a linear combination of basis Hamiltonians.

   :param H: array containing the Hamiltonian matrices [H1, H2, ..., Hn], each of shape (d, d).
   :type H: np.ndarray
   :param coeff: array of time-dependent coefficients for each Hamiltonian. coeff[j, i] is the coefficient for Hamiltonian H[j, :, :] at time step i.
   :type coeff: np.ndarray

   :returns: The final unitary matrix U of shape (d, d) representing the total time evolution.
   :rtype: np.ndarray

   :raises ValueError: If the number of Hamiltonians does not coincide with the number of time-dependent coefficient lists given or if
       the number of coefficients per Hamiltonian is not always the same.


.. py:function:: deshuffle_qiskit(mat)

   Reverse Qiskit's bit-ordering convention in a matrix representation.

   This function permutes the rows and columns of a square matrix by reversing
   the binary representation of their indices. It is typically used when
   converting multi-qubit operators between Qiskit and libraries that follow a
   different qubit-index (endianness) convention, such as Quimb.

   :param mat: A square matrix of shape ``(2**n, 2**n)`` representing an ``n``-qubit
               operator.

   :returns:

             A matrix of the same shape as ``mat`` with reversed bit-ordering applied
               to both row and column indices.


.. py:function:: qiskit_to_quimb(circuit)

   Convert a Qiskit quantum circuit into a Quimb MPS circuit.

   Each instruction of the input ``QuantumCircuit`` is translated into a
   constant gate applied to a ``CircuitMPS``. For multi-qubit gates, the gate
   matrix is first reordered using ``deshuffle_qiskit`` to match Quimb's qubit
   ordering convention.

   :param circuit: The input ``qiskit.QuantumCircuit`` to convert.

   :returns:

             A ``quimb.tensor.circuit.CircuitMPS`` representing the same sequence of
               operations as the input circuit.

   .. rubric:: Notes

   This function assumes that each instruction in ``circuit.data`` provides
     a matrix representation via ``ins.matrix`` and qubit operands via
     ``ins.qubits``.


.. py:function:: my_quimb_fidelity(pulse_circuit, quimb_circ_ideal)

   Compute the state fidelity against an ideal Quimb reference circuit.

   The input `pulse_circuit` is converted to a `qiskit.QuantumCircuit` via
   `pulse_circuit.to_circuit()`, then translated to a `CircuitMPS` using
   `qiskit_to_quimb`. The fidelity is computed as

   .. math::

       F = \left| \langle \psi_{\mathrm{ideal}} \mid \psi \rangle \right|^2



   :param pulse_circuit: Pulse-level circuit to evaluate.
   :param quimb_circ_ideal: Ideal reference `CircuitMPS` circuit.

   :returns: The state fidelity as a float in $[0, 1]$.
