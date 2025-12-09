spin_pulse.experimental_environment
===================================

.. py:module:: spin_pulse.experimental_environment

.. autoapi-nested-parse::

   Description of the noisy environment associated to a hardware.




Classes
-------

.. autoapisummary::

   spin_pulse.experimental_environment.ExperimentalEnvironment


Module Contents
---------------

.. py:class:: ExperimentalEnvironment(hardware_specs, noise_type = 'pink', T2 = 100.0, TJ = None, duration = 2**10, only_idle = False, segment_duration = 2**10, seed = None)

   Simulates a quantum experimental environment with configurable noise models.

   .. attribute:: hardware_specs

      HardwareSpecs class, that defines the hardware settings.

      :type: class

   .. attribute:: noise_type

      Type of noise to simulate ("pink", "white", or "coherent").

      :type: str

   .. attribute:: T2

      Characteristic time of individual qubits.

      :type: float

   .. attribute:: TJ

      Characteristic time of coupled two-qubit system at maximal J coupling with no noise on Larmor frequency.

      :type: float or None

   .. attribute:: duration

      Total duration of the simulation.

      :type: int

   .. attribute:: segment_duration

      Duration of each noise segment.

      :type: int

   .. attribute:: only_idle

      Flag to simulate only idle qubits.

      :type: bool

   .. attribute:: time_traces

      List of time traces for each qubit.

      :type: list

   .. attribute:: time_traces_coupling

      List of time traces for coupling noise for each pair of qubits (if TJ is set).

      :type: list

   .. attribute:: seed

      seed integer for random number generation

   Initialize the ExperimentalEnvironment with specified noise characteristics and simulation parameters.

   :param hardware_specs: HardwareSpecs class, that defines the hardware settings.
   :type hardware_specs: class
   :param noise_type: Type of noise to simulate. Must be one of "pink", "white", or "coherent".
   :type noise_type: Literal
   :param T2: Characteristic time of individual qubits.
   :type T2: float
   :param TJ: Characteristic time of coupled two-qubit system at maximal J coupling with no noise on Lamror frequency.
   :type TJ: float or None
   :param duration: Total duration of the simulation.
   :type duration: int
   :param only_idle: Flag to simulate only idle qubits.
   :type only_idle: bool
   :param segment_duration: Duration of each noise segment; used to partition the time trace.
   :type segment_duration: int
   :param seed: seed integer for random number generation

   :raises AssertionError: If an invalid noise_type is provided.


   .. py:method:: assign_time_traces()

      Generate and assign noise time traces to each qubit's Larmor frequency and J coupling to each pair of qubits.

      Behavior:
          - For each qubit, instantiate a noise generator using the selected noise_type.
          - The generator uses T2, duration, and segment_duration to produce a time trace.
          - If TJ is provided, generate additional time traces for J coupling noise for each pair of qubits.

      Effects:
          - Populates self.time_traces with one noise trace per qubit.
          - If TJ is set, populates self.time_traces_coupling with one trace per pair of qubits (n-1 traces for n qubits).



   .. py:method:: __str__()

      Returns a string representation of the ExperimentalEnvironment instance.

      Includes:
          - Number of qubits
          - Noise type
          - T2 and TJ values
          - Duration and segment duration
          - Whether only idle qubits are simulated
          - The J Coupling value set in HardwareSpecs
          - The total number of assigned time traces
