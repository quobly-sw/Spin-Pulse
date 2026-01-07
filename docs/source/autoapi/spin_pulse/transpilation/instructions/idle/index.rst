
spin_pulse.transpilation.instructions.idle
==========================================

.. py:module:: spin_pulse.transpilation.instructions.idle

.. autoapi-nested-parse::

   Pulse description of qubit idling.




Classes
-------

.. autoapisummary::

   spin_pulse.transpilation.instructions.idle.IdleInstruction


Module Contents
---------------


.. py:class:: IdleInstruction(qubits, duration = 1)

   Bases: :py:obj:`spin_pulse.transpilation.instructions.pulse_instruction.PulseInstruction`


   Represents an idle (delay) operation applied to one or more qubits.

   This instruction models the absence of active control during a time
   interval. It is used both for explicit delays in pulse scheduling and
   as a building block for dynamical decoupling sequences. The duration
   is expressed in discrete time steps compatible with the pulse model.

   .. attribute:: - name

      Name of the instruction ("delay").

      :type: str

   .. attribute:: - qubits

      List of qubits on which the idle operation acts.

      :type: list

   .. attribute:: - duration

      Duration of the idle period in time steps.

      :type: int

   Initializes an idle instruction on the specified qubits.

   :param - qubits: List of qubits where the idle operation is applied.
   :type - qubits: list
   :param - duration: Duration of the idle period. Default is 1.
   :type - duration: int

   :returns: The idle instruction is stored in the created object.
   :rtype: - None


   .. py:attribute:: name
      :value: 'delay'



   .. py:method:: adjust_duration(duration)


   .. py:method:: plot(ax=None, t_start=0, label_gates=True)

      Plots the idle instruction as a flat line segment.

      :param - ax: Axis on which the idle segment
                   is drawn. If None, the current axis is used.
      :type - ax: matplotlib axis, optional
      :param - t_start: Starting time of the idle segment. Default is 0.
      :type - t_start: int
      :param - label_gates: Unused parameter kept for API compatibility.
                            Default is True.
      :type - label_gates: bool

      :returns: The idle segment is drawn on the provided axis.
      :rtype: - None



   .. py:method:: to_hamiltonian()

      Converts the idle operation to its Hamiltonian representation.

      The idle period corresponds to zero Hamiltonian evolution, resulting
      in no phase accumulation. This method returns a zero Hamiltonian and
      a zero frequency array compatible with the simulation interface.

      :returns: Array of zeros of length ``duration``.
      :rtype: - ndarray



   .. py:method:: to_dynamical_decoupling(hardware_specs)

      Expands the idle instruction into a dynamical decoupling sequence.

      Depending on the hardware_specs dynamical decoupling mode, this
      method replaces the idle period with a sequence of rotations and
      shorter idle segments. Supported dynamical decoupling modes
      include:
      - SPIN_ECHO: Inserts two pi rotations with symmetric idle periods.
      - FULL_DRIVE: Applies repeated 2*pi rotations to average out noise.
      - None: Returns the idle instruction unchanged.

      :param - hardware_specs: Hardware configuration specifying
                               the dynamical decoupling mode and available pulse shapes.
      :type - hardware_specs: HardwareSpecs

      :returns:

                List of PulseInstruction objects implementing the chosen
                  dynamical decoupling sequence.
      :rtype: - list
