
spin_pulse.transpilation.hardware_specs
=======================================

.. py:module:: spin_pulse.transpilation.hardware_specs

.. autoapi-nested-parse::

   Description of the hardware to simulate circuit execution.




Classes
-------

.. autoapisummary::

   spin_pulse.transpilation.hardware_specs.Shape
   spin_pulse.transpilation.hardware_specs.HardwareSpecs


Module Contents
---------------


.. py:class:: Shape(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Enumeration of pulse envelope shapes.

   This enum defines the functional form of the pulse envelope used for
   control operations in spin-qubit pulse sequences.


   .. py:attribute:: GAUSSIAN
      :value: 'gaussian'


      Gaussian-shaped pulse envelope.


   .. py:attribute:: SQUARE
      :value: 'square'


      Square (rectangular) pulse envelope.


.. py:class:: HardwareSpecs(num_qubits, B_field, delta, J_coupling, rotation_shape, ramp_duration = 1, coeff_duration = 5, dynamical_decoupling = None, optim = 0)

   Defines the hardware specifications for a spin qubit device model.

   This class stores all physical and control parameters required to build
   pulse instructions, generate rotation gates, and configure backend-level
   compilation. It also defines the available couplings, supported gate set,
   and optional dynamical decoupling strategy. The specifications in this
   object determine how qubit operations and timing constraints are modeled
   throughout the simulation workflow.

   .. attribute:: - rotation_generator

      Class used to generate rotation
      instructions based on the selected pulse shape.

      :type: RotationInstruction

   .. attribute:: - num_qubits

      Number of qubits in the device model.

      :type: int

   .. attribute:: - J_coupling

      Maximum coupling strength between adjacent qubits.

      :type: float

   .. attribute:: - fields

      Dictionary mapping interaction types ("x", "y",
      "z", "Heisenberg") to their corresponding field strengths.

      :type: dict

   .. attribute:: - rotation_shape

      Shape of the pulses used for qubit control.

      :type: Shape

   .. attribute:: - coeff_duration

      Duration coefficient for Gaussian pulses
      when applicable.

      :type: int

   .. attribute:: - ramp_duration

      Duration of the ramp used in square pulses.

      :type: int

   .. attribute:: - first_pass

      Preset first-stage Qiskit pass manager.

      :type: PassManager

   .. attribute:: - second_pass

      Additional optimization pass manager.

      :type: PassManager

   .. attribute:: - dynamical_decoupling

      Optional
      dynamical decoupling sequence applied to idle qubits.

      :type: DynamicalDecoupling | None

   Initialize the HardwareSpecs object that defines the hardware specifications.

   :param num_qubits: Number of qubits considered.
   :type num_qubits: int
   :param B_field: Maximal magnetic field strength.
   :type B_field: float
   :param delta: Maximal energy difference between two qubits.
   :type delta: float
   :param J_coupling: Maximal coupling strength between two qubit.
   :type J_coupling: float
   :param rotation_shape: Pulse shape used for qubit manipulation.
   :type rotation_shape: Shape
   :param ramp_duration: Duration of the pulse ramp for square pulse. Default is 1.
   :type ramp_duration: int, optional
   :param coeff_duration: Duration coefficient for Gaussian pulses. Default is 5.
   :type coeff_duration: int, optional
   :param dynamical_decoupling: If not None, defines the dynamical decoupling sequence to be applied to Idle qubits.
   :type dynamical_decoupling: DynamicalDecoupling, optional


   .. py:attribute:: rotation_generator
      :type:  type[spin_pulse.transpilation.instructions.RotationInstruction]


   .. py:attribute:: num_qubits
      :type:  int


   .. py:attribute:: J_coupling
      :type:  float


   .. py:attribute:: fields
      :type:  dict[str, float]


   .. py:attribute:: rotation_shape
      :type:  Shape


   .. py:attribute:: ramp_duration
      :type:  int
      :value: 1



   .. py:attribute:: first_pass


   .. py:attribute:: second_pass


   .. py:attribute:: dynamical_decoupling
      :type:  spin_pulse.transpilation.dynamical_decoupling.DynamicalDecoupling | None
      :value: None



   .. py:method:: gate_transpile(circ)

      Transpile a quantum circuit into an ISA circuit using hardware specifications.

      :param circ: The quantum circuit to be converted.
      :type circ: qiskit.QuantumCircuit

      :returns: The ISA quantum circuit composed of spin qubit native gates.
      :rtype: qiskit.QuantumCircuit
