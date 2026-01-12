
spin_pulse.transpilation.pulse_sequence
=======================================

.. py:module:: spin_pulse.transpilation.pulse_sequence

.. autoapi-nested-parse::

   Low-level representation of pulses applied to qubits.




Classes
-------

.. autoapisummary::

   spin_pulse.transpilation.pulse_sequence.PulseSequence


Module Contents
---------------


.. py:class:: PulseSequence(pulse_instructions)

   Sequence of pulse instructions acting on one or several qubits.

   A PulseSequence is an ordered list of PulseInstruction objects consecutive in time. The class computes the total duration of the
   sequence, the starting time of each constituent instruction, and provides
   utilities for plotting. It allows to reconstruct Hamiltonians,
   attach time traces from a noise environment, and apply dynamical
   decoupling on idle segments.

   .. attribute:: - qubits

      Ordered list of qubits included in the layer.

      :type: list[qiskit.circuit.Qubit]

   .. attribute:: - num_qubits

      Number of qubits in the sequence.

      :type: int

   .. attribute:: - pulse_instructions

      Ordered list of pulse
      instructions that form the sequence.

      :type: list[PulseInstruction]

   .. attribute:: - n_pulses

      Number of instructions in the sequence.

      :type: int

   .. attribute:: - duration

      Total duration of the sequence (sum of individual
      instruction durations).

      :type: int

   .. attribute:: - t_start_relative

      Starting time of each pulse instruction
      relative to the beginning of the sequence.

      :type: list[int]

   .. attribute:: - name

      Concatenated name describing the sequence, formed from
      instruction names and durations.

      :type: str

   Initialize a PulseSequence from a list of PulseInstruction objects.

   The constructor computes the total duration, the relative starting
   times of each instruction, and assigns a compact sequence name for
   identification or debugging.

   :param pulse_instructions: Ordered list of pulse
                              instructions to concatenate into a sequence. All instructions
                              must act on the same qubit subset.
   :type pulse_instructions: list[PulseInstruction]


   .. py:attribute:: qubits


   .. py:attribute:: num_qubits


   .. py:attribute:: n_pulses


   .. py:attribute:: duration


   .. py:attribute:: t_start_relative
      :value: [0]



   .. py:attribute:: pulse_instructions


   .. py:attribute:: name
      :value: ''



   .. py:method:: plot(ax=None, label_gates = True)

      Plot the pulse sequence on a matplotlib axis.

      Each instruction is rendered at its relative starting time using the
      ``PulseInstruction.plot`` method. If a time trace has been attached,
      the corresponding stochastic noise signal is plotted on top of the
      sequence.

      :param ax: Axis on which to draw the
                 sequence. If None, the current axis is used.
      :type ax: matplotlib.axes.Axes | None
      :param label_gates: Whether to annotate pulse instructions with
                          gate labels.
      :type label_gates: bool



   .. py:method:: to_hamiltonian()

      Construct the Hamiltonian representation of the sequence.

      For each pulse instruction, this method extracts the local Hamiltonian
      generator and its time-dependent coefficient. The coefficients are
      embedded into a global array spanning the full sequence duration,
      resulting in a list of Hamiltonians and a list of time-dependent
      coefficient vectors for each qubit.

      If a noise time trace was previously attached (e.g., from a noise
      model), an additional Z-type Hamiltonian is appended for one-qubit
      sequences (for deviations of the qubit's frequency).

      :returns:     H: ndarray of Hamiltonian matrices.
                    coeff: ndarray of time-dependent coefficient.
      :rtype: tuple[np.ndarray, np.ndarray]



   .. py:method:: adjust_duration(duration)

      Extend individual qubit pulse sequence to match a target duration
      (i.e. usually the maximal duration of a pulse sequence in a pulse layer).

      If the target duration is larger than the current sequence duration,
      an IdleInstruction is appended to pad the sequence. This is used, for
      example, to align pulse durations across a PulseLayer. Otherwise, a warning is
      issued to let know the user that the duration in input was too short.

      :param duration: Targeted total duration for the sequence.
      :type duration: int



   .. py:method:: attach_time_trace(time_trace, only_idle)

      Attach a noise time trace to the sequence.

      The method maps a provided noise signal (typically from a noise
      model) onto the time domain of the sequence. If ``only_idle`` is True,
      the trace is only applied to idle ("delay") instructions; otherwise,
      it is applied to all instructions.

      :param time_trace: Array of classical values sampled over
                         the full duration of the parent PulseLayer.
      :type time_trace: np.ndarray
      :param only_idle: If True, attach the trace only on idle
                        instructions; all active pulses receive no time trace.
      :type only_idle: bool



   .. py:method:: to_dynamical_decoupling(hardware_specs)

      Insert dynamical decoupling sequence into the Idle instruction.

      The method scans the pulse list and replaces idle ("delay")
      instructions by a list of pulses generated according to the selected
      dynamical decoupling mode defined in the hardware specifications.
      Non-idle instructions are left unchanged. Only single-qubit sequences
      can be dynamically decoupled.

      :param hardware_specs: Hardware configuration specifying
                             the dynamical decoupling mode and available pulse shapes.
      :type hardware_specs: HardwareSpecs

      :returns: A new sequence with dynamical decoupling applied.
      :rtype: PulseSequence

      :raises AssertionError: If the sequence acts on more than one qubit.



   .. py:method:: append(pulse_instruction)

      Append a pulse instruction at the end of the sequence.

      The starting times and sequence metadata (duration, name, pulse count)
      are updated accordingly.

      :param pulse_instruction: Instruction to append.
      :type pulse_instruction: PulseInstruction



   .. py:method:: insert(pos, pulse_instruction)

      Insert a pulse instruction at a specified position.

      The method inserts the instruction at index ``pos`` (negative indices
      are accepted and interpreted in Python style). The relative start times
      and total duration are recomputed after insertion.

      :param pos: Insertion index; negative values count from the end.
      :type pos: int
      :param pulse_instruction: Instruction to insert.
      :type pulse_instruction: PulseInstruction



   .. py:method:: generate_relative_time_sequence()

      Generate the list of starting times for each pulse instruction.

      :returns: Relative starting times of each instruction, with
                the first entry equal to 0 and each subsequent entry equal to
                the cumulative duration of the preceding pulses.
      :rtype: list[int]
