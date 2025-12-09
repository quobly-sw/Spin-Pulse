spin_pulse.instructions.idle
============================

.. py:module:: spin_pulse.instructions.idle

.. autoapi-nested-parse::

   Pulse description of qubit idling.




Classes
-------

.. autoapisummary::

   spin_pulse.instructions.idle.IdleInstruction


Module Contents
---------------

.. py:class:: IdleInstruction(qubits, duration = 1)

   Bases: :py:obj:`spin_pulse.instructions.pulse_instruction.PulseInstruction`


   _summary_

   :param PulseInstruction: _description_
   :type PulseInstruction: _type_

   _summary_

   :param qubits: _description_
   :type qubits: _type_
   :param duration: _description_. Defaults to 1.
   :type duration: int, optional


   .. py:method:: __str__()

      Provide a string representation of the PulseDuration object.

      Returns:
      - str: A formatted string describing the PulseDuration object.




   .. py:method:: plot(ax=None, t_start=0, label_gates=True)

      _summary_

      :param ax: _description_. Defaults to None.
      :type ax: _type_, optional
      :param t_start: _description_. Defaults to 0.
      :type t_start: int, optional
      :param label_gates: _description_. Defaults to True.
      :type label_gates: bool, optional



   .. py:method:: to_hamiltonian()

      _summary_

      :returns: _description_
      :rtype: _type_
