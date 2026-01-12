
spin_pulse.transpilation.instructions
=====================================

.. py:module:: spin_pulse.transpilation.instructions

.. autoapi-nested-parse::

   Instruction representation used in pulse level description of a circuit.




Re-exported objects
-------------------

The following objects can be directly imported from spin_pulse.transpilation.instructions even if they
are implemented in submodules.

.. list-table::
   :widths: 30 70

   * - :py:class:`~spin_pulse.transpilation.instructions.rotations.GaussianRotationInstruction`
     - Gaussian-shaped rotation pulse instruction.
   * - :py:class:`~spin_pulse.transpilation.instructions.idle.IdleInstruction`
     - Represent an idle (delay) operation applied to one or more qubits.
   * - :py:class:`~spin_pulse.transpilation.instructions.pulse_instruction.PulseInstruction`
     - Base class representing a pulse-level instruction applied to qubits.
   * - :py:class:`~spin_pulse.transpilation.instructions.rotations.RotationInstruction`
     - Base class for single- and two-qubit rotation pulse instructions.
   * - :py:class:`~spin_pulse.transpilation.instructions.rotations.SquareRotationInstruction`
     - Square-shaped rotation pulse with optional linear ramps.


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/spin_pulse/transpilation/instructions/idle/index
   /autoapi/spin_pulse/transpilation/instructions/pulse_instruction/index
   /autoapi/spin_pulse/transpilation/instructions/rotations/index


Classes
-------

.. autoapisummary::

   spin_pulse.transpilation.instructions.IdleInstruction
   spin_pulse.transpilation.instructions.PulseInstruction
   spin_pulse.transpilation.instructions.GaussianRotationInstruction
   spin_pulse.transpilation.instructions.RotationInstruction
   spin_pulse.transpilation.instructions.SquareRotationInstruction


Package Contents
----------------


.. py:class:: IdleInstruction(qubits, duration = 1)

   Bases: :py:obj:`spin_pulse.transpilation.instructions.pulse_instruction.PulseInstruction`


   Represent an idle (delay) operation applied to one or more qubits.

   This instruction models the absence of active control during a time
   interval. It is used both for explicit delays in pulse scheduling and
   as a building block for dynamical decoupling sequences. The duration
   is expressed in time steps.

   .. attribute:: - name

      Name of the instruction ("delay").

      :type: str

   .. attribute:: - qubits

      List of qubits on which the idle operation acts.

      :type: list[qiskit.circuit.Qubit]

   .. attribute:: - duration

      Duration of the idle period in time steps.

      :type: int

   Initialize an idle instruction on the specified qubits.

   :param qubits: List of qubits where the idle operation is applied.
   :type qubits: list[qiskit.circuit.Qubit]
   :param duration: Duration of the idle period. Default is 1.
   :type duration: int

   :returns: The idle instruction is stored in the created object.
   :rtype: None


   .. py:attribute:: name
      :value: 'delay'



   .. py:method:: adjust_duration(duration)


   .. py:method:: plot(ax=None, t_start=0, label_gates=True)

      Plot the idle instruction as a flat line segment.

      :param ax: Axis on which the idle segment
                 is drawn. If None, the current axis is used.
      :type ax: matplotlib axis, optional
      :param t_start: Starting time of the idle segment. Default is 0.
      :type t_start: int
      :param label_gates: Unused parameter kept for API compatibility.
                          Default is True.
      :type label_gates: bool

      :returns: The idle segment is drawn on the provided axis.
      :rtype: None



   .. py:method:: to_hamiltonian()

      Convert the idle operation to its Hamiltonian representation.

      The idle period corresponds to zero Hamiltonian evolution, resulting
      in no phase accumulation. This method returns a zero Hamiltonian and
      a zero frequency array compatible with the simulation interface.

      :returns: Array of zeros of length ``duration``.
      :rtype: ndarray



   .. py:method:: to_dynamical_decoupling(hardware_specs, mode = None)

      Expand the idle instruction into a dynamical decoupling sequence.

      Depending on the hardware_specs dynamical decoupling mode, this
      method replaces the idle period with a sequence of rotations and
      shorter idle segments. Supported dynamical decoupling modes
      include:

      - SPIN_ECHO: Inserts two :math:`\pi` rotations with symmetric idle periods.
      - FULL_DRIVE: Applies repeated :math:`2\pi` rotations to average out noise.
      - None: Returns the idle instruction unchanged.

      :param hardware_specs: Hardware configuration specifying
                             the dynamical decoupling mode and available pulse shapes.
      :type hardware_specs: HardwareSpecs

      :returns: List of PulseInstruction objects implementing the chosen dynamical decoupling sequence.
      :rtype: list[PulseInstruction]



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



.. py:class:: GaussianRotationInstruction(name, qubits, amplitude, sign, coeff_duration, duration)

   Bases: :py:obj:`RotationInstruction`


   Gaussian-shaped rotation pulse instruction.

   This instruction implements a Gaussian pulse envelope centered in time,
   with width controlled by ``coeff_duration`` and amplitude chosen to
   generate a target rotation angle. The sign parameter controls the
   direction of the rotation.

   .. attribute:: - name

      Name of the generating operator, for example
      "x", "y", "z", or "Heisenberg".

      :type: str

   .. attribute:: - qubits

      List of qubits on which the rotation is applied.

      :type: list[qiskit.circuit.Qubit]

   .. attribute:: - num_qubits

      Number of qubits targeted by the instruction.

      :type: int

   .. attribute:: - duration

      Total duration of the pulse in time steps.

      :type: int

   .. attribute:: - amplitude

      Peak amplitude of the Gaussian pulse.

      :type: float

   .. attribute:: - coeff_duration

      Factor relating pulse duration to the
      Gaussian standard deviation.

      :type: float

   .. attribute:: - sign

      Sign of the rotation, typically +1 or -1.

      :type: float

   Initialize a Gaussian rotation pulse with given parameters.

   The pulse is modeled as a Gaussian envelope with a peak amplitude
   given by ``amplitude``, centered in the middle of the time window,
   and with a standard deviation derived from ``duration`` and
   ``coeff_duration``.

   :param name: Name of the generating operator, for example
                "x", "y", "z", or "Heisenberg".
   :type name: str
   :param qubits: List of qubits on which the rotation is applied.
   :type qubits: list[qiskit.circuit.Qubit]
   :param amplitude: Peak amplitude of the Gaussian pulse.
   :type amplitude: float
   :param sign: Sign of the rotation, typically +1 or -1.
   :type sign: float
   :param coeff_duration: Factor used to set the Gaussian width
                          ``sigma = duration / coeff_duration``.
   :type coeff_duration: float
   :param duration: Total duration of the pulse in time steps.
   :type duration: int

   :returns: The Gaussian rotation instruction is stored in the created object.
   :rtype: None


   .. py:attribute:: amplitude


   .. py:attribute:: coeff_duration


   .. py:attribute:: sign


   .. py:method:: from_angle(name, qubits, angle, hardware_specs)
      :classmethod:


      Build a Gaussian pulse that performs a target rotation angle.

      A search over pulse duration is performed to find a configuration
      where the peak amplitude remains below the hardware field limit and
      the total integrated area matches the requested angle. The Gaussian
      width is controlled by ``hardware_specs.coeff_duration``.

      :param name: Name of the generating operator, for example
                   "x", "y", "z", or "Heisenberg".
      :type name: str
      :param qubits: List of qubits on which the rotation is applied.
      :type qubits: list[qiskit.circuit.Qubit]
      :param angle: Target rotation angle in radians.
      :type angle: float
      :param hardware_specs: Hardware configuration providing
                             maximum allowed field strengths and the duration coefficient.
      :type hardware_specs: HardwareSpecs

      :returns: A Gaussian pulse instruction that performs the requested angle within the hardware limits.
      :rtype: GaussianRotationInstruction



   .. py:method:: eval(t)

      Evaluate the Gaussian pulse envelope at the given time indices.

      The envelope is defined as ``amplitude * sign * exp( - (t - t0)^2 / (2 * sigma^2) )``.

      where ``t0`` is the center of the pulse window and ``sigma`` is given by
      ``duration/coeff_duration``.

      :param t: Discrete time indices at which
                the pulse envelope is evaluated.
      :type t: ndarray or array-like

      :returns: Pulse amplitudes at the specified time indices.
      :rtype: ndarray



.. py:class:: RotationInstruction(name, qubits, duration)

   Bases: :py:obj:`spin_pulse.transpilation.instructions.pulse_instruction.PulseInstruction`


   Base class for single- and two-qubit rotation pulse instructions.

   A rotation instruction represents a shaped control pulse that generates
   a rotation around a given axis or interaction, such as x, y, z, or
   Heisenberg. Subclasses define the time-dependent envelope via the
   ``eval`` method and provide constructors from a target rotation angle.

   .. attribute:: - name

      Label of the generating operator, for example
      "x", "y", "z", or "Heisenberg".

      :type: str

   .. attribute:: - qubits

      List of qubits on which the rotation acts.

      :type: list[qiskit.circuit.Qubit]

   .. attribute:: - num_qubits

      Number of qubits targeted by the instruction.

      :type: int

   .. attribute:: - duration

      Duration of the pulse in time steps.

      :type: int

   .. attribute:: - amplitude

      Optional amplitude parameter used to rescale
      the pulse envelope when adjusting the duration.

      :type: float

   Initialize a rotation instruction with a given name and duration.

   :param name: Name of the generating operator, for example
                "x", "y", "z", or "Heisenberg".
   :type name: str
   :param qubits: List of qubits on which the rotation is applied.
   :type qubits: list[qiskit.circuit.Qubit]
   :param duration: Duration of the pulse in time steps.
   :type duration: int

   :returns: The rotation instruction is stored in the created object.
   :rtype: None


   .. py:attribute:: name


   .. py:method:: from_angle(name, qubits, angle, hardware_specs)
      :classmethod:

      :abstractmethod:


      Construct a rotation instruction from a target angle.

      This class method must be implemented by subclasses to map a target
      rotation angle to a concrete pulse shape and duration, using the
      hardware specifications.

      :param name: Name of the generating operator, for example
                   "x", "y", "z", or "Heisenberg".
      :type name: str
      :param qubits: List of qubits on which the rotation is applied.
      :type qubits: list[qiskit.circuit.Qubit]
      :param angle: Target rotation angle in radians.
      :type angle: float
      :param hardware_specs: Hardware configuration used
                             to determine pulse shape and duration.
      :type hardware_specs: HardwareSpecs

      :returns: Instance of the subclass implementing the requested rotation.
      :rtype: RotationInstruction

      :raises NotImplementedError: If the method is not implemented in
          the subclass.



   .. py:method:: eval(t)
      :abstractmethod:


      Evaluate the pulse envelope at the given time indices.

      Subclasses must implement this method to return the pulse amplitude
      at each time step contained in the input array.

      :param t: Discrete time indices at which
                the pulse envelope is evaluated.
      :type t: ndarray or array-like

      :returns: Pulse amplitudes at the specified time indices.
      :rtype: ndarray

      :raises NotImplementedError: If the method is not implemented in
          the subclass.



   .. py:method:: to_pulse()

      Return the full pulse envelope over the instruction duration.

      The envelope is evaluated on the interval from 0 to duration-1.
      If the instruction has an attribute ``distort_factor``, the pulse
      is corrected by an additional multiplicative factor.

      :returns: Pulse amplitudes over the full duration.
      :rtype: ndarray



   .. py:method:: to_angle()

      Compute the effective rotation angle generated by the pulse.

      The effective angle is taken as the sum of all pulse amplitudes
      over the duration of the instruction.

      :returns: Total rotation angle in radians.
      :rtype: float



   .. py:method:: to_hamiltonian()

      Build the generator Hamiltonian associated with this rotation.

      The method returns the static Hamiltonian matrix corresponding to
      the chosen generating operator, together with the time-dependent
      scalar coefficients given by the pulse envelope.

      For example:

      - "x" uses the Pauli :math:`X` operator.
      - "y" uses the Pauli :math:`Y` operator.
      - "z" uses the Pauli :math:`Z` operator.
      - "Heisenberg" uses the sum of :math:`XX`, :math:`YY`, and :math:`ZZ` interactions.

      :returns: Tuple containing the Hamiltonian matrix of size :math:`2^n` by :math:`2^n`, where :math:`n` is the number of qubits, and
                the time-dependent coefficients defined by the pulse envelope.
      :rtype: - tuple(ndarray,ndarray)



   .. py:method:: adjust_duration(duration)

      Rescale the pulse amplitude to match a new duration.

      The total rotation angle is preserved by adjusting the pulse
      amplitude after changing the duration. The method computes the
      original angle, sets a new duration, evaluates the new angle, and
      rescales the amplitude so that the final effective angle remains
      unchanged.

      :param duration: New duration of the pulse in time steps.
      :type duration: int

      :returns: The internal duration and amplitude are updated in place.
      :rtype: None



   .. py:method:: plot(ax=None, t_start=0, label_gates=True)

      Plot the pulse envelope as a filled region.

      The pulse is drawn over the interval from ``t_start`` to
      ``t_start + duration`` using a color that depends on the
      generating operator name. Optionally, a label containing the gate
      name and rotation angle is appended to the axis title.

      :param ax: Axis on which to draw the pulse.
                 If None, the current axis is used.
      :type ax: matplotlib axis, optional
      :param t_start: Starting time index of the pulse on the plot.
                      Default is 0.
      :type t_start: int
      :param label_gates: If True, appends a textual label with the
                          gate name and rotation angle to the axis title. Default is True.
      :type label_gates: bool

      :returns: The pulse envelope is drawn on the provided axis.
      :rtype: None



.. py:class:: SquareRotationInstruction(name, qubits, amplitude, sign, ramp_duration, duration)

   Bases: :py:obj:`RotationInstruction`


   Square-shaped rotation pulse with optional linear ramps.

   This instruction implements a piecewise-linear pulse envelope composed of
   a rising ramp, a constant plateau, and a falling ramp. The total duration
   and amplitude determine the effective rotation angle. The sign parameter
   controls the direction of the rotation.

   .. attribute:: - name

      Name of the generating operator, for example
      "x", "y", "z", or "Heisenberg".

      :type: str

   .. attribute:: - qubits

      List of qubits on which the rotation is applied.

      :type: list[qiskit.circuit.Qubit]

   .. attribute:: - num_qubits

      Number of qubits targeted by the instruction.

      :type: int

   .. attribute:: - duration

      Total duration of the pulse in time steps.

      :type: int

   .. attribute:: - amplitude

      Pulse amplitude during the plateau.

      :type: float

   .. attribute:: - sign

      Sign of the rotation, typically +1 or -1.

      :type: float

   .. attribute:: - ramp_duration

      Duration of each ramp region at the beginning
      and end of the pulse.

      :type: int

   Initialize a square rotation pulse with ramps and plateau.

   The pulse is defined by a linear ramp up, a constant-amplitude plateau,
   and a linear ramp down. The plateau duration is given by
   ``duration - 2 * ramp_duration`` and must be non-negative.

   :param name: Name of the generating operator, for example
                "x", "y", "z", or "Heisenberg".
   :type name: str
   :param qubits: List of qubits on which the rotation is applied.
   :type qubits: list[qiskit.circuit.Qubit]
   :param amplitude: Amplitude of the square plateau.
   :type amplitude: float
   :param sign: Sign of the rotation, typically +1 or -1.
   :type sign: float
   :param ramp_duration: Duration of each linear ramp region.
   :type ramp_duration: int
   :param duration: Total duration of the pulse in time steps.
   :type duration: int

   :returns: The square rotation instruction is stored in the created object.
   :rtype: None

   :raises ValueError: If the plateau duration is negative, i.e.,
       ``duration < 2 * ramp_duration``.


   .. py:attribute:: amplitude


   .. py:attribute:: sign


   .. py:attribute:: ramp_duration


   .. py:attribute:: duration


   .. py:method:: from_angle(name, qubits, angle, hardware_specs)
      :classmethod:


      Build a square pulse that performs a rotation of the target angle.

      A binary search is used over the pulse duration to find a combination
      of duration and amplitude that matches the requested angle while
      respecting the hardware field limits specified in ``hardware_specs``.
      The procedure starts from the minimal duration compatible with the
      ramp time and iteratively refines the duration.

      :param name: Name of the generating operator, for example
                   "x", "y", "z", or "Heisenberg".
      :type name: str
      :param qubits: List of qubits on which the rotation is applied.
      :type qubits: list[qiskit.circuit.Qubit]
      :param angle: Target rotation angle in radians.
      :type angle: float
      :param hardware_specs: Hardware configuration providing
                             ramp duration and maximum allowed field strengths.
      :type hardware_specs: HardwareSpecs

      :returns: A square pulse instruction that performs the requested rotation with the target angle within the hardware limits.
      :rtype: SquareRotationInstruction



   .. py:method:: eval(t)

      Evaluate the square pulse envelope at the given time indices.

      The envelope is composed of:

      - a linear rise from 0 to the target amplitude during the first ramp,
      - a constant plateau with full amplitude,
      - a symmetric linear fall back to 0 during the final ramp.

      If ``ramp_duration`` is zero, a pure square pulse with constant height
      is returned over the whole duration.

      :param t: Discrete time indices at which
                the pulse envelope is evaluated.
      :type t: ndarray or array-like

      :returns: Pulse amplitudes at the specified time indices.
      :rtype: ndarray
