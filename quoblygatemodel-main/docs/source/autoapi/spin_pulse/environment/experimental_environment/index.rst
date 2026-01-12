
spin_pulse.environment.experimental_environment
===============================================

.. py:module:: spin_pulse.environment.experimental_environment

.. autoapi-nested-parse::

   Description of the noisy environment associated to a hardware.




Classes
-------

.. autoapisummary::

   spin_pulse.environment.experimental_environment.ExperimentalEnvironment


Module Contents
---------------


.. py:class:: ExperimentalEnvironment(hardware_specs, noise_type = NoiseType.PINK, T2S = 100.0, TJS = None, duration = 2**10, only_idle = False, segment_duration = 2**10, seed = None)

   Contain a quantum experimental environment with configurable noise models.

   .. attribute:: - hardware_specs

      HardwareSpecs class, that defines the hardware settings.

      :type: class

   .. attribute:: - noise_type

      Type of noise to simulate. Must be "pink", "white", or "quasistatic".

      :type: NoiseType

   .. attribute:: - T2S

      Characteristic time of individual qubits.

      :type: float

   .. attribute:: - TJS

      Characteristic time of coupled two-qubit system at maximal J coupling without noise on the qubit's frequency.

      :type: float or None

   .. attribute:: - duration

      Total duration of the simulation.

      :type: int

   .. attribute:: - segment_duration

      Duration of each noise segment; used to partition the time trace.

      :type: int

   .. attribute:: - only_idle

      Flag to apply noise only to idle qubits.

      :type: bool

   .. attribute:: - time_traces

      List of time traces for each qubit.

      :type: list[float]

   .. attribute:: - time_traces_coupling

      List of time traces for coupling noise for each pair of qubits (if TJS is set).

      :type: list[float]

   .. attribute:: - seed

      seed integer for random number generation. If not specified, no seed used.

      :type: int or None

   Initialize the ExperimentalEnvironment with specified noise characteristics and simulation parameters.

   :param hardware_specs: HardwareSpecs class, that defines the hardware settings.
   :type hardware_specs: class
   :param noise_type: Type of noise to simulate. Must be "pink", "white", or "quasistatic".
   :type noise_type: NoiseType
   :param T2S: Characteristic time of individual qubits.
   :type T2S: float
   :param TJS: Characteristic time of coupled two-qubit system at maximal J coupling with no noise on the qubit's frequency.
   :type TJS: float or None
   :param duration: Total duration of the simulation.
   :type duration: int
   :param only_idle: Flag to apply noise only to idle qubits.
   :type only_idle: bool
   :param segment_duration: Duration of each noise segment; used to partition the time trace.
   :type segment_duration: int
   :param seed: seed integer for random number generation. If not specified, no seed used.
   :type seed: int or None

   :raises ValueError: If an invalid noise_type is provided.


   .. py:attribute:: noise_generator
      :type:  type[spin_pulse.environment.noise.WhiteNoiseTimeTrace] | type[spin_pulse.environment.noise.QuasistaticNoiseTimeTrace] | type[spin_pulse.environment.noise.PinkNoiseTimeTrace]


   .. py:attribute:: hardware_specs
      :type:  spin_pulse.transpilation.hardware_specs.HardwareSpecs


   .. py:attribute:: noise_type
      :type:  spin_pulse.environment.noise.NoiseType


   .. py:attribute:: T2S
      :type:  float
      :value: 100.0



   .. py:attribute:: TJS
      :type:  float | None
      :value: None



   .. py:attribute:: duration
      :type:  int
      :value: 1024



   .. py:attribute:: segment_duration
      :type:  int
      :value: 1024



   .. py:attribute:: seed
      :type:  int | None
      :value: None



   .. py:attribute:: only_idle
      :value: False



   .. py:method:: generate_time_traces()

      Generate noise time traces for each qubit's frequency and J coupling to each pair of qubits if TJS is defined.

      Behavior:
          For each qubit, instantiate a noise generator using the selected noise_type.
          The generator uses T2S, duration, and segment_duration to produce a time trace.
          If TJS is provided, generate additional time traces for J coupling noise for each pair of qubits.

      Effects:
          Populate self.time_traces with one noise trace per qubit.
          If TJS is set, populate self.time_traces_coupling with one trace per pair of qubits (n-1 traces for n qubits).
