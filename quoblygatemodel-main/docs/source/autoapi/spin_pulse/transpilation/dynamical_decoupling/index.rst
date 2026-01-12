
spin_pulse.transpilation.dynamical_decoupling
=============================================

.. py:module:: spin_pulse.transpilation.dynamical_decoupling

.. autoapi-nested-parse::

   Description of dynamical decoupling.




Classes
-------

.. autoapisummary::

   spin_pulse.transpilation.dynamical_decoupling.DynamicalDecoupling


Module Contents
---------------


.. py:class:: DynamicalDecoupling(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Enumeration of supported dynamical decoupling sequences.

   This enumeration identifies the available pulse-based methods used to
   mitigate phase noise in spin qubit experiments. The selected sequence
   determines how control pulses are applied during idle periods in order
   to reduce the effect of low-frequency noise.

   .. attribute:: - FULL_DRIVE

      Continuous driving of the qubit during the idle period.

   .. attribute:: - SPIN_ECHO

      Single refocusing pulse applied at the midpoint of the
      idle period.


   .. py:attribute:: FULL_DRIVE
      :value: 'full_drive'



   .. py:attribute:: SPIN_ECHO
      :value: 'spin_echo'
