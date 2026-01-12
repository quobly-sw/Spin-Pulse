
spin_pulse.transpilation.pulse_circuit
======================================

.. py:module:: spin_pulse.transpilation.pulse_circuit

.. autoapi-nested-parse::

   Pulse-level representation of a quantum circuit.




Classes
-------

.. autoapisummary::

   spin_pulse.transpilation.pulse_circuit.PulseCircuit


Module Contents
---------------


.. py:class:: PulseCircuit(circ, qubits, pulse_layers, hardware_specs, exp_env = None, store_samples = False)

   Pulse-level representation of a quantum circuit.

   A PulseCircuit stores a layered decomposition of a qiskit.QuantumCircuit into
   PulseLayer objects and, optionally, a stochastic noise environment. It
   provides utilities to visualize the pulse schedule, convert it back to a
   gate-level circuit, and compute fidelities or average channels under
   sampled noise realizations.

   .. attribute:: - original_circ

      Original quantum circuit from which
      the PulseCircuit was constructed.

      :type: qiskit.QuantumCircuit

   .. attribute:: - num_qubits

      Number of qubits in the circuit.

      :type: int

   .. attribute:: - qubits

      Ordered list of qubits acted on by the circuit.

      :type: list[qiskit.circuit.Qubit]

   .. attribute:: - pulse_layers

      Ordered list of pulse layers that
      implement the circuit at the pulse level.

      :type: list[PulseLayer]

   .. attribute:: - n_layers

      Number of pulse layers.

      :type: int

   .. attribute:: - duration

      Total duration of the pulse circuit, given by the sum
      of all layer durations (in the discrete time unit of the model).

      :type: int

   .. attribute:: - t_lab

      Current position in the laboratory time axis, used to
      attach successive noise time traces when averaging over samples.

      :type: int

   Initialize a PulseCircuit from pulse layers.

   The constructor records the original circuit, the list of qubits and
   the sequence of PulseLayer objects. It computes the total duration,
   assigns starting times to all layers and computes a dynamical decoupling
   sequence according to the hardware specifications. If an ExperimentalEnvironment
   is provided, noise time traces are attached to the circuit and its layers.
   Optionally, a container for storing per-sample time series can be created.

   :param circ: Original quantum circuit represented at
                the pulse level.
   :type circ: QuantumCircuit
   :param qubits: Ordered list of qubits involved in the
                  circuit.
   :type qubits: list[qiskit.circuit.Qubit]
   :param pulse_layers: Pulse layers that realize the
                        circuit in time order.
   :type pulse_layers: list[PulseLayer]
   :param hardware_specs: Hardware configuration specifying
                          fields, couplings and dynamical decoupling options.
   :type hardware_specs: HardwareSpecs
   :param exp_env: Noise environment from
                   which time traces are drawn and attached to this circuit. If
                   None, no noise trace is attached.
   :type exp_env: ExperimentalEnvironment | None
   :param store_samples: If True, allocate an internal dictionary
                         ``series_samples`` to store time-series samples of observables.
   :type store_samples: bool


   .. py:attribute:: original_circ
      :type:  qiskit.QuantumCircuit


   .. py:attribute:: qubits
      :type:  list[qiskit.circuit.Qubit]


   .. py:attribute:: num_qubits


   .. py:attribute:: pulse_layers


   .. py:attribute:: n_layers


   .. py:attribute:: duration


   .. py:attribute:: t_lab
      :value: 0



   .. py:method:: from_circuit(circ, hardware_specs, exp_env = None, store_samples = False)
      :classmethod:


      Construct a PulseCircuit from a qiskit.QuantumCircuit.

      The input is first converted to a qiskit.dagcircuit.DAGCircuit then all barrier and
      measurement gate are removed, and each DAG layer is translated
      into a PulseLayer using the hardware specifications. Empty layers
      (containing only barriers) are skipped. The resulting list of
      pulse layers is used to build a PulseCircuit.

      :param circ: Circuit to translate into pulse layers.
      :type circ: qiskit.QuantumCircuit
      :param hardware_specs: Hardware specification used to
                             map gate operations to pulse sequences.
      :type hardware_specs: HardwareSpecs
      :param exp_env: Experimental
                      environment providing noise specification and noise time traces.
                      If None, no noise is attached to the pulses.
      :type exp_env: ExperimentalEnvironment | None
      :param store_samples: If True, allocate storage for time-series
                            samples of observables.
      :type store_samples: bool

      :returns: A pulse-level representation of the input
                circuit.
      :rtype: PulseCircuit



   .. py:method:: from_dag_circuit(dag, hardware_specs, exp_env = None, store_samples = False, original_circuit = None)
      :classmethod:


      Construct a PulseCircuit from a qiskit.dagcircuit.DAGCircuit.

      The input circuit is first stripped of measurements and
      barrier, if present. Then each DAG layer is translated
      into a PulseLayer using the hardware specifications.
      Empty layers (containing only barriers) are skipped.
      The resulting list of pulse layers is used to build a PulseCircuit.

      :param dag: Circuit to translate into pulse layers.
      :type dag: qiskit.dagcircuit.DAGCircuit
      :param hardware_specs: Hardware specification used to
                             map gate operations to pulse sequences.
      :type hardware_specs: HardwareSpecs
      :param exp_env: Experimental
                      environment providing noise specification and noise time traces.
                      If None, no noise is attached to the pulses.
      :type exp_env: ExperimentalEnvironment | None
      :param store_samples: If True, allocate storage for time-series
                            samples of observables.
      :type store_samples: bool

      :returns: A pulse-level representation of the input
                circuit.
      :rtype: PulseCircuit



   .. py:method:: assign_starting_times()

      Assign a starting time to each pulse layer to synchronize the
      different layers and pulse instructions.

      The starting time ``t_start`` of each PulseLayer is computed as the
      cumulative duration of all previous layers, with the first layer
      starting at time zero. This defines a global time axis for the
      PulseCircuit.




   .. py:method:: plot(hardware_specs = None, label_gates = True)

      Plot the pulse schedule of the circuit.

      This method creates a multi-panel matplotlib figure showing, for each
      layer, the one-qubit and two-qubit pulse envelopes applied to each
      qubit and coupling. The vertical scale is chosen
      consistently with the hardware field and coupling amplitudes if given.

      :param hardware_specs: Hardware specification used
                             to set the limits of manipulation parameter amplitudes.
                             If None, default symmetric limits are used.
      :type hardware_specs: HardwareSpecs | None
      :param label_gates: If True, gate labels are shown.
      :type label_gates: bool



   .. py:method:: to_circuit(measure_all = False)

      Convert the pulse circuit back to a qiskit.QuantumCircuit.

      Each PulseLayer is converted into equivalent circuit that are
      composed into a copy of the original circuit structure.
      Optionally, a final measurement on all qubits is added.

      :param measure_all: If True, all qubits are measured
                          at the end of the reconstructed circuit.
      :type measure_all: bool

      :returns: A circuit implementing the same unitary evolution
                as the PulseCircuit (up to numerical approximations).
      :rtype: qiskit.QuantumCircuit



   .. py:method:: circuit_samples(exp_env = None)

      Compute the number of noisy circuit samples that can be obtained with the given environment.

      The number of circuit samples is given by the integer ratio between
      the environment duration and the pulse-circuit duration. If no
      environment is provided, a single sample is assumed.

      :param exp_env: Experimental environment
                      providing the total duration.
      :type exp_env: ExperimentalEnvironment | None

      :returns: Number of non-overlapping samples that can be drawn from the
                duration of the experiment.
      :rtype: int



   .. py:method:: get_logical_bitstring(physical_bistring)

      Restore the original logical qubit layout before transpilation.
      During Qiskit transpilation process, the qubit register may be
      reordered to produce an optimized physical layout that minimizes gate
      costs. To recover the logical bitstring and interpret measurement
      outcomes correctly, it is necessary to invert this remapping and reconstruct
      the initial logical ordering of the qubits.

      The mapping is derived from the layout associated with the original
      circuit used to build the PulseCircuit. If a TranspileLayout is
      present, the final index layout is used. If only a Layout is
      available, its permutation is used and a warning is emitted, as this
      typically indicates that the circuit was not transpiled. If no layout
      information is present, the physical and logical orders are assumed
      to coincide and a warning is emitted.

      :param physical_bistring: Bitstring obtained from a measurement in
                                the physical qubit ordering.
      :type physical_bistring: str

      :returns: Bitstring reordered into the logical qubit basis.
      :rtype: str



   .. py:method:: averaging_over_samples(f, exp_env = None, *args)

      Estimate the average value over as many noisy samples as the experimental environment
      allows it, of a user-provided function using the pulse circuit.


      This method repeatedly attaches new pieces of the noise time traces from the
      experimental environment to the PulseCircuit and evaluates a
      user-provided function ``f(self, *args)`` for each realization. The
      results are averaged over all samples, effectively performing a
      Monte Carlo average over noise trajectories.

      :param f: Function that takes the PulseCircuit as first
                argument and returns a numerical quantity to be averaged.
      :type f: Callable
      :param exp_env: Noise environment from
                      which time traces are drawn. If None, a single deterministic
                      evaluation is performed.
      :type exp_env: ExperimentalEnvironment | None
      :param \*Parameters: Additional positional arguments forwarded to ``f``.

      :returns: The sample-averaged value of ``f(self, *args)``.
      :rtype: Any



   .. py:method:: run_experiment(exp_env, simulator=AerSimulator())

      Simulate single-shot measurement on noisy instances of the circuit.

      This method repeatedly attaches new pieces of the noise time traces from the
      experimental environment to the PulseCircuit and simulates with MPS method a single-shot measurement thanks to Qiskit Aer. The
      results are stored in a dictionary that gather the counts obtained for all possible bitstrings.


      :param exp_env: Noise environment from
                      which time traces are drawn. If None, a single deterministic
                      evaluation is performed.
      :type exp_env: ExperimentalEnvironment | None
      :param - simulator: an instance of qiksit's AerSimulator.

      :returns: A dictionary which keys are the obtained bitstrings and their respective number of occurences.
      :rtype: dict



   .. py:method:: fidelity(circ_ref = None)

      Compute the average gate fidelity with respect to a reference circuit.

      The PulseCircuit is converted to a qiskit.QuantumCircuit, and the average
      gate fidelity between its unitary and that of the reference circuit
      is computed using the qiskit.quantum_info.Operator representation.

      :param circ_ref: Reference circuit used to define the
                       target unitary. Default is self.original_circ
      :type circ_ref: qiskit.QuantumCircuit

      :returns: Average gate fidelity between the PulseCircuit unitary and
                the reference circuit unitary.
      :rtype: float



   .. py:method:: mean_fidelity(exp_env, circ_ref = None)

      Estimate the mean fidelity under a stochastic noise environment.

      The average gate fidelity with respect to a reference circuit is
      computed for multiple noise realizations drawn from the experimental
      environment, and the results are averaged using
      ``averaging_over_samples``.

      :param circ_ref: Reference circuit used to define the
                       target unitary.
      :type circ_ref: qiskit.QuantumCircuit
      :param exp_env: Noise environment from
                      which time traces are drawn.
      :type exp_env: ExperimentalEnvironment | None

      :returns: Sample-averaged gate fidelity under the specified noise
                model.
      :rtype: float



   .. py:method:: mean_channel(exp_env = None)

      Estimate the mean quantum channel generated by the pulse circuit.

      For each noise realization, the PulseCircuit is converted to a
      qiskit.QuantumCircuit and then to a SuperOp representing the corresponding
      quantum channel. The channels are averaged over samples using
      ``averaging_over_samples``.

      :param exp_env: Noise environment from
                      which time traces are drawn.
      :type exp_env: ExperimentalEnvironment | None

      :returns: Sample-averaged quantum channel acting on the qubit
                register.
      :rtype: qiskit.quantum_info.SuperOp



   .. py:method:: attach_time_traces(exp_env = None)

      Attach noise time traces from the experimental environment
      to the pulse circuit.

      If an experimental environment is provided, this method extracts
      segments of the environment time traces that match the total circuit
      duration and assigns them to the PulseCircuit and each PulseLayer.
      For one-qubit pulse sequences, the corresponding single-qubit time
      traces are attached (qubit's frequency deviation).
      For two-qubit sequences, coupling time traces are attached if
      available (i.e. J coupling noise) and used to set the J noise deviation
      during two-qubit gates.

      The internal laboratory time pointer ``t_lab`` is incremented by the
      circuit duration after attaching the time traces, so that subsequent
      calls use the next segment of the noise time trace.

      :param exp_env: Experimental
                      environment providing qubit's frequency deviation time trace
                      and, optionally, J coupling deviation time traces.
                      If None, no trace is attached.
      :type exp_env: ExperimentalEnvironment | None



   .. py:method:: attach_dynamical_decoupling(hardware_specs)

      Insert dynamical decoupling sequences into all pulse layers,
      when possible (i.e. Idle time sufficiently long).

      If a dynamical decoupling mode is specified in the hardware
      specifications, each PulseLayer in the circuit is updated by calling
      its ``attach_dynamical_decoupling`` method with the chosen mode. If
      no dynamical decoupling is configured, the circuit is left unchanged.

      :param hardware_specs: Hardware configuration specifying
                             the dynamical decoupling mode and available pulse shapes.
      :type hardware_specs: HardwareSpecs
