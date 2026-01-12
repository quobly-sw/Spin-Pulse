
spin_pulse.transpilation.passes.rzz_echo
========================================

.. py:module:: spin_pulse.transpilation.passes.rzz_echo



Classes
-------

.. autoapisummary::

   spin_pulse.transpilation.passes.rzz_echo.RZZEchoPass


Module Contents
---------------


.. py:class:: RZZEchoPass

   Bases: :py:obj:`qiskit.transpiler.basepasses.TransformationPass`


   Echo :math:`R_{ZZ}` gates with :math:`X` pulses to mitigate Stark shifts.

   This transpiler pass replaces each two-qubit :math:`R_{ZZ}` gate by an echoed
   sequence consisting of interleaved :math:`\pi` rotations around the :math:`x` axis and
   :math:`R_{ZZ}` gates with half the original angle. The echo sequence is applied
   locally on each occurrence of an RZZ gate in the input DAG circuit.


   .. py:method:: run(dag)

      Apply the :math:`R_{ZZ}` echo transformation to all :math:`R_{ZZ}` gates in the DAG.

      Each :math:`R_{ZZ}(\theta)` operation is replaced by the following pattern
      on the two involved qubits:

      - :math:`R_X(\pi)` on both qubits
      - :math:`R_{ZZ}(\theta / 2)`
      - :math:`R_X(\pi)` on both qubits
      - :math:`R_{ZZ}(\theta / 2)`

      All other operations are left unchanged.

      :param dag: Input circuit represented as a DAG on which
                  the transformation is applied.
      :type dag: DAGCircuit

      :returns: New DAG circuit where each :math:`R_{ZZ}` gate has been replaced by the echoed :math:`R_{ZZ}` sequence.
      :rtype: DAGCircuit
