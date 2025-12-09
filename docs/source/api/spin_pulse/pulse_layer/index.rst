spin_pulse.pulse_layer
======================

.. py:module:: spin_pulse.pulse_layer

.. autoapi-nested-parse::

   Pulse layer applied to all target qubits simultaneously.




Classes
-------

.. autoapisummary::

   spin_pulse.pulse_layer.PulseLayer


Module Contents
---------------

.. py:class:: PulseLayer(qubits, oneq_pulse_sequences, twoq_pulse_sequences)


   Layer of one- and two-qubit gate pulse sequences.

   A PulseLayer groups single-qubit and two-qubit PulseCircuit objects that
   act over a common time interval (time step). All pulse sequences in the layer are
   padded with idle instructions so that they share the same duration. The
   layer keeps track of which qubits are driven by one-qubit or two-qubit
   pulses and which qubits remain idle.

   :param qubits: Ordered list of qubits included in the layer.
   :type qubits: list
   :param oneq_pulse_sequences: One-qubit pulse sequences
                                to be applied in the layer.
   :type oneq_pulse_sequences: list[PulseCircuit]
   :param twoq_pulse_sequences: Two-qubit pulse sequences
                                to be applied in the layer.
   :type twoq_pulse_sequences: list[PulseCircuit]

   .. attribute:: duration

      Common duration of the layer, which is the maximal duration
      of the pulse sequences given

      :type: int

   .. attribute:: qubits

      Ordered list of qubits included in the layer.

      :type: list

   .. attribute:: num_qubits

      Number of qubits in the layer.

      :type: int

   .. attribute:: oneq_pulse_sequences

      One-qubit pulse sequence
      assigned to each qubit. For qubits without an explicit drive,
      an idle-only PulseSequence of length duration is created.

      :type: list[PulseCircuit]

   .. attribute:: twoq_pulse_sequences

      Two-qubit pulse sequences
      acting on pair of qubits in the layer.

      :type: list[PulseCircuit]

   .. attribute:: pulse_sequences

      Concatenation of all one- and
      two-qubit pulse sequences in the layer.

      :type: list[PulseCircuit]

   .. attribute:: n_pulses

      Total number of pulse sequences in the layer.

      :type: int

   .. attribute:: qubits_oneq_active

      Qubits that are manipulated during the layer
      through single-qubit gate.

      :type: list

   .. attribute:: qubits_twoq_active

      Qubits that are manipulated during the layer
      through two-qubit gate.

      :type: list

   .. attribute:: qubits_idle

      Qubits that are idle in this layer.

      :type: list


   .. py:method:: from_circuit_layer(qubits, circuit_layer, hardware_specs)
      :classmethod:


      Construct a PulseLayer from a circuit layer.

      This method converts each gate in a circuit layer into one
      PulseCircuit objects according to the hardware specifications. Single-
      and two-qubit gates are translated separately, and the resulting pulse
      sequences are grouped into a PulseLayer.

      :param qubits: Ordered list of qubits included in the layer.
      :type qubits: list
      :param circuit_layer: Circuit layer or list of
                            gate data objects whose entries are passed to.
                            ``gate_to_pulse_sequences`` to be converted into pulses.
      :type circuit_layer: list[QuantumCircuit]
      :param hardware_specs: HardwareSpecs class that defines
                             the hardware specifications.
      :type hardware_specs: HardwareSpecs

      :returns: A new layer containing the translated one- and two-qubit
                pulse sequences.
      :rtype: PulseLayer



   .. py:method:: __str__()

      Return a string representation of the pulse layer.

      Includes:
          - duration: the duration of the layer.




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

      Convert the pulse layer into an equivalent QuantumCircuit.

      Each PulseSequence is translated into a unitary matrix by propagating the
      corresponding Hamiltonian terms over the layer duration. Two-qubit
      sequences generate 4x4 unitaries, while single-qubit sequences generate
      2x2 unitaries. The resulting unitaries are appended to a new QuantumCircuit
      in an order consistent with the layer structure.

      :returns: A circuit representation of the pulse layer, where
                each pulse sequence is replaced by a UnitaryGate.
      :rtype: QuantumCircuit
