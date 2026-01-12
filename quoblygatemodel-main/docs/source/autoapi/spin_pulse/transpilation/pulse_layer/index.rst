
spin_pulse.transpilation.pulse_layer
====================================

.. py:module:: spin_pulse.transpilation.pulse_layer

.. autoapi-nested-parse::

   Layer of pulses applied to the target qubits simultaneously.




Classes
-------

.. autoapisummary::

   spin_pulse.transpilation.pulse_layer.PulseLayer


Module Contents
---------------


.. py:class:: PulseLayer(qubits, oneq_pulse_sequences, twoq_pulse_sequences)

   Layer of one- and two-qubit gate pulse sequences.

   A PulseLayer groups single-qubit and two-qubit PulseSequence objects that
   act over a common time interval. Pulse sequences in the layer are eventually
   padded with idle instructions such that all of them share the same duration. The
   layer keeps track of which qubits are driven by one-qubit or two-qubit
   pulses and which qubits remain idle.

   .. attribute:: - duration

      Duration of the layer, which is the maximal duration
      of the pulse sequences given.

      :type: int

   .. attribute:: - qubits

      Ordered list of qubits included in the layer.

      :type: list[qiskit.circuit.Qubit]

   .. attribute:: - num_qubits

      Number of qubits in the layer.

      :type: int

   .. attribute:: - oneq_pulse_sequences

      One-qubit pulse sequence
      assigned to each qubit. For qubits without an explicit drive,
      an idle-only PulseSequence of length duration is created.

      :type: list[PulseSequence]

   .. attribute:: - twoq_pulse_sequences

      Two-qubit pulse sequences
      acting on pair of qubits in the layer.

      :type: list[PulseSequence]

   .. attribute:: - pulse_sequences

      Concatenation of all one- and
      two-qubit pulse sequences in the layer.

      :type: list[PulseSequence]

   .. attribute:: - n_pulses

      Total number of pulse sequences in the layer.

      :type: int

   .. attribute:: - qubits_oneq_active

      Qubits that are manipulated during the layer
      through single-qubit gate.

      :type: list[qiskit.circuit.Qubit]

   .. attribute:: - qubits_twoq_active

      Qubits that are manipulated during the layer
      through two-qubit gate.

      :type: list[qiskit.circuit.Qubit]

   .. attribute:: - qubits_idle

      Qubits that are idle during this layer.

      :type: list[qiskit.circuit.Qubit]

   Initialize the PulseLayer from lists of pulse sequences and qubits.

   :param qubits: Ordered list of qubits included in the layer.
   :type qubits: list[qiskit.circuit.Qubit]
   :param oneq_pulse_sequences: One-qubit pulse sequences
                                to be applied in the layer.
   :type oneq_pulse_sequences: list[PulseSequence]
   :param twoq_pulse_sequences: Two-qubit pulse sequences
                                to be applied in the layer.
   :type twoq_pulse_sequences: list[PulseSequence]


   .. py:attribute:: duration


   .. py:attribute:: oneq_pulse_sequences


   .. py:attribute:: twoq_pulse_sequences


   .. py:attribute:: pulse_sequences


   .. py:attribute:: qubits


   .. py:attribute:: n_pulses
      :type:  int


   .. py:attribute:: num_qubits
      :type:  int


   .. py:attribute:: qubits_oneq_active
      :value: []



   .. py:attribute:: qubits_twoq_active
      :value: []



   .. py:attribute:: qubits_idle
      :value: []



   .. py:method:: from_circuit_layer(qubits, circuit_layer, hardware_specs)
      :classmethod:


      Construct a PulseLayer from a circuit layer.

      This method converts each gate in a circuit layer into a
      PulseSequence object according to the hardware specifications. Single-
      and two-qubit gates are translated separately, and the resulting pulse
      sequences are grouped into a PulseLayer.

      :param qubits: Ordered list of qubits included in the layer.
      :type qubits: list[qiskit.circuit.Qubit]
      :param circuit_layer: QuantumCircuit instance representing one layer of a bigger circuit. Its instructions are passed to
                            ``gate_to_pulse_sequences`` to be converted into pulses.
      :type circuit_layer: QuantumCircuit
      :param hardware_specs: HardwareSpecs class instance that defines
                             the hardware specifications.
      :type hardware_specs: HardwareSpecs

      :returns: A PulseLayer containing the pulse sequences that corresponds to the circuit_layer.
      :rtype: PulseLayer



   .. py:method:: plot(axs=None, label_gates = True)

      Plot all single-qubit and two-qubit pulse sequences in the layer.

      For each qubit, the corresponding one-qubit PulseSequence is displayed on
      its own axis. Two-qubit PulseSequences are plotted on intermediate axes
      between the qubits they act on. If no axis array is provided, a new
      matplotlib figure is created.

      :param axs: Array of axes on which to draw the sequences.
                  If None, a new figure and axis array is created.
      :type axs: list[Axes] | None
      :param label_gates: Controls gate labelling. If True, each pulse
                          is annotated with a default gate label. If a string, the value is
                          forwarded to the underlying ``PulseSequence.plot`` methods to
                          customize labelling.
      :type label_gates: bool | str



   .. py:method:: to_circuit()

      Convert the pulse layer into an equivalent qiskit.QuantumCircuit.

      Each PulseSequence is translated into a unitary matrix by propagating the
      corresponding Hamiltonian terms over the layer duration. Two-qubit
      sequences generate 4x4 unitaries, while single-qubit sequences generate
      2x2 unitaries. The resulting unitaries are appended to a new qiskit.QuantumCircuit
      in an order consistent with the layer structure.

      :returns:

                A circuit representation of the pulse layer, where UnitaryGate
                    corresponds to a pulse sequence.
      :rtype: qiskit.QuantumCircuit



   .. py:method:: attach_dynamical_decoupling(hardware_specs)

      Apply a dynamical decoupling sequence to all one-qubit pulse sequences
      if possible.

      If a dynamical decoupling mode is specified in the hardware
      specifications, this method transforms each one-qubit PulseSequence
      in the layer with a new sequence obtained by applying a dynamical decoupling
      transformation according to the specified hardware parameters. Two-qubit
      sequences are left unchanged.

      :param hardware_specs: Hardware configuration specifying
                             the dynamical decoupling mode and available pulse shapes.
      :type hardware_specs: HardwareSpecs
