
spin_pulse.transpilation.instructions.pulse_instruction
=======================================================

.. py:module:: spin_pulse.transpilation.instructions.pulse_instruction

.. autoapi-nested-parse::

   Instruction representation used in pulse level description of a circuit.




Classes
-------

.. autoapisummary::

   spin_pulse.transpilation.instructions.pulse_instruction.PulseInstruction


Module Contents
---------------


.. py:class:: PulseInstruction(qubits, duration=1)

   Base class representing a pulse-level instruction applied to qubits.

   This class defines the common interface for all pulse instructions,
   including rotation pulses and idle periods. Each instruction targets
   one or more qubits and spans a given discrete duration. Subclasses
   extend this class to implement specific pulse behaviors.

   .. attribute:: - name

      Name identifying the type of pulse instruction.

      :type: str

   .. attribute:: - qubits

      List of qubits on which the instruction acts.

      :type: list[qiskit.circuit.Qubit]

   .. attribute:: - num_qubits

      Number of qubits targeted by the instruction.

      :type: int

   .. attribute:: - duration

      Duration of the instruction in time steps.

      :type: int

   Initialize a pulse instruction acting on the given qubits.

   :param qubits: List of qubits on which the instruction is applied.
   :type qubits: list[qiskit.circuit.Qubit]
   :param duration: Duration of the instruction in time steps.
                    Default is 1.
   :type duration: int

   :returns: The configured instruction is stored in the created object.
   :rtype: None


   .. py:attribute:: name
      :value: '_name'



   .. py:attribute:: qubits


   .. py:attribute:: num_qubits


   .. py:attribute:: duration
      :value: 1
