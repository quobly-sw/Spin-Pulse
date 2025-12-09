spin_pulse.instructions.rotations
=================================

.. py:module:: spin_pulse.instructions.rotations

.. autoapi-nested-parse::

   Description of rotations at the pulse level.




Classes
-------

.. autoapisummary::

   spin_pulse.instructions.rotations.RotationInstruction
   spin_pulse.instructions.rotations.SquareRotationInstruction
   spin_pulse.instructions.rotations.GaussianRotationInstruction


Module Contents
---------------

.. py:class:: RotationInstruction(name, qubits, duration)

   Bases: :py:obj:`spin_pulse.instructions.pulse_instruction.PulseInstruction`



   Initialize a RotatingInstruction with GeneratingOperator name, number of pulses n_pulses of angle angle

   Parameters:
   - ..: ..



.. py:class:: SquareRotationInstruction(name, qubits, amplitude, sign, ramp_duration, duration)

   Bases: :py:obj:`RotationInstruction`



   Initialize a Square RotatingInstruction with GeneratingOperator: name, and total angle: angle, and n pulses
   Parameters:
   - ..: ..


   .. py:method:: __str__()

      Provide a string representation of the PulseDuration object.

      Returns:
      - str: A formatted string describing the PulseDuration object.




.. py:class:: GaussianRotationInstruction(name, qubits, amplitude, sign, coeff_duration, duration)

   Bases: :py:obj:`RotationInstruction`



   Initialize a Gaussian RotatingInstruction with GeneratingOperator name, and total angle angle, and n pulses
   Parameters:
   - ..: ..


   .. py:method:: __str__()

      Provide a string representation of the PulseDuration object.

      Returns:
      - str: A formatted string describing the PulseDuration object.
