
spin_pulse.characterization.ramsey
==================================

.. py:module:: spin_pulse.characterization.ramsey

.. autoapi-nested-parse::

   Helper functions to carry out Ramsey experiments.




Functions
---------

.. autoapisummary::

   spin_pulse.characterization.ramsey.get_ramsey_circuit
   spin_pulse.characterization.ramsey.get_contrast
   spin_pulse.characterization.ramsey.get_average_ramsey_contrast


Module Contents
---------------


.. py:function:: get_ramsey_circuit(duration, hardware_specs, exp_env = None)

   Construct a pulse-level Ramsey experiment.

   This function builds a single-qubit Ramsey sequence consisting of a
   Hadamard gate, an idle period of a specified duration, and a second
   Hadamard gate. The circuit is transpiled into the hardware native gate
   set and converted into a PulseCircuit. If an experimental environment is
   provided, noise time traces are attached to the resulting pulse-level
   circuit.

   :param duration: Duration of the free-evolution period (in the discrete
                    time unit used by the hardware model).
   :type duration: int
   :param hardware_specs: Hardware configuration used to
                          transpile the logical Ramsey sequence into native instructions, and
                          to generate the pulse sequences of the PulseCircuit.
   :type hardware_specs: HardwareSpecs
   :param exp_env: Optional noise environment
                   from which time traces are created and attached to the PulseCircuit.
   :type exp_env: ExperimentalEnvironment | None

   :returns: Pulse-level representation of the Ramsey experiment,
             optionally including noise time traces.
   :rtype: PulseCircuit


.. py:function:: get_contrast(pulse_circuit)

   Compute the population contrast of a Ramsey experiment.

   The pulse-level circuit is converted back to a unitary qiskit.QuantumCircuit,
   and the resulting unitary matrix is applied to the input state 0.
   The contrast is defined as the population difference between state 0
   and state 1, that is: C = P0 - P1

   :param pulse_circuit: Pulse-level Ramsey circuit.
   :type pulse_circuit: PulseCircuit

   :returns: Population contrast.
   :rtype: float


.. py:function:: get_average_ramsey_contrast(hardware_specs, exp_env, durations)

   Compute the average Ramsey contrast over multiple noise realizations.

   For each free-evolution duration given, a Ramsey pulse circuit is constructed
   and its population contrast is computed by averaging over multiple noise
   realizations drawn from the experimental environment. After each duration,
   the environment time traces are regenerated to ensure independence
   between samples.

   :param hardware_specs: Hardware configuration used to
                          construct pulse-level Ramsey circuits.
   :type hardware_specs: HardwareSpecs
   :param exp_env: Noise environment providing time
                   traces for each sample.
   :type exp_env: ExperimentalEnvironment
   :param durations: List of free-evolution durations for which the
                     Ramsey contrast is evaluated.
   :type durations: list[int]

   :returns:

             Array containing the average Ramsey contrast for each
                 duration in ``durations``.
   :rtype: np.ndarray
