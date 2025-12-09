spin_pulse.hardware_specs
=========================

.. py:module:: spin_pulse.hardware_specs

.. autoapi-nested-parse::

   Description of the hardware to simulate circuit execution.




Classes
-------

.. autoapisummary::

   spin_pulse.hardware_specs.HardwareSpecs


Module Contents
---------------

.. py:class:: HardwareSpecs(num_qubits, B_field, delta, J_coupling, rotation_shape, ramp_duration = 1, coeff_duration = 5, dynamical_decoupling=None, optim = 0)


   Initialize the HardwareSpecs object that defines the hardware specifications

   :param - num_qubits: Number of qubits considered.
   :type - num_qubits: int
   :param - B_field: Maximal magnetic field strength.
   :type - B_field: float
   :param - delta: Maximal energy difference between two qubits.
   :type - delta: float
   :param - J_coupling: Maximal coupling strength between two qubit.
   :type - J_coupling: float
   :param - rotation_shape: Pulse shape used for qubit manipulation.
   :type - rotation_shape: Shape
   :param - ramp_duration: Duration of the pulse ramp for square pulse. Default is 1.
   :type - ramp_duration: int, optional
   :param - coeff_duration: Duration coefficient for Gaussian pulses. Default is 5.
   :type - coeff_duration: int, optional
   :param - dynamical_decoupling: If not None, defines the dynamical decoupling sequence to by applied to Idle qubits.
   :type - dynamical_decoupling: optional


   .. py:method:: gate_transpile(circ)

      Transpile a quantum circuit into an ISA circuit using hardware specifications

      :param circ: the quantum circuit to be converted
      :type circ: qiskit.QuantumCircuit

      :returns: the ISA quantum circuit composed of spin qubit native gates
      :rtype: qiskit.QuantumCircuit



   .. py:method:: __str__()

      Return a string representation of the HardwareSpecs instance.

      Includes:
          - Number of qubits.
          - B_field, delta and J_coupling values.
          - Shape of manipulation pulses.
          - The pulse ramp duration for square pulse.
          - The coefficient for Gaussian pulses.
          - The dynamical decoupling sequence chosen. None if no dynamical decoupling.
