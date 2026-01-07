
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


   Echoes RZZ gates with X pulses to mitigate Stark shifts.

   This transpiler pass replaces each two-qubit RZZ gate by an echoed
   sequence consisting of interleaved pi rotations around the X axis and
   RZZ gates with half the original angle. The echo sequence is applied
   locally on each occurrence of an RZZ gate in the input DAG circuit.


   .. py:method:: run(dag)

      Applies the RZZ echo transformation to all RZZ gates in the DAG.

      Each RZZ(theta) operation is replaced by the following pattern
      on the two involved qubits:
      - RX(pi) on both qubits
      - RZZ(theta / 2)
      - RX(pi) on both qubits
      - RZZ(theta / 2)

      All other operations are left unchanged.

      :param - dag: Input circuit represented as a DAG on which
                    the transformation is applied.
      :type - dag: DAGCircuit

      :returns:

                New DAG circuit where each RZZ gate has been
                  replaced by the echoed RZZ sequence.
      :rtype: - DAGCircuit
