
spin_pulse.environment.noise.quasistatic
========================================

.. py:module:: spin_pulse.environment.noise.quasistatic



Classes
-------

.. autoapisummary::

   spin_pulse.environment.noise.quasistatic.QuasistaticNoiseTimeTrace


Module Contents
---------------


.. py:class:: QuasistaticNoiseTimeTrace(T2S, duration, segment_duration, seed = None)

   Bases: :py:obj:`spin_pulse.environment.noise.noise_time_trace.NoiseTimeTrace`


   Generate a quasi-static noise time trace for spin-qubit simulations.

   This noise type produces a sequence of piecewise-constant Gaussian
   noise segments. Each segment has duration ``segment_duration``, and all
   samples within a segment share the same random value. The resulting
   noise corresponds to a quasi-static fluctuation with standard deviation
   determined by the coherence time ``T2S``.

   .. attribute:: - segment_duration

      Duration of each constant-noise segment.

      :type: int

   .. attribute:: - sigma

      Standard deviation of the quasistatic noise,
      computed as :math:`\sqrt{2}/T_2^*`.

      :type: float

   .. attribute:: - T2S

      Coherence time parameter used to scale the noise.

      :type: float

   .. attribute:: - values

      Array of noise values of length ``duration``.

      :type: ndarray

   Initialize a quasi-static Gaussian noise trace.

   The noise trace is constructed from repeated Gaussian segments of
   length ``segment_duration``. Each segment takes a single Gaussian
   random value with zero mean and standard deviation :math:`\sqrt{2}/T_2^*`.
   The total duration must be an integer multiple of the segment length.

   :param T2S: Coherence time parameter defining the noise intensity.
   :type T2S: float
   :param duration: Total number of time steps in the noise trace.
   :type duration: int
   :param segment_duration: Length of each piecewise-constant segment.
   :type segment_duration: int
   :param seed: Optional seed for reproducible random generation.
   :type seed: int | None

   :raises ValueError: If ``duration`` is not divisible by ``segment_duration``.


   .. py:attribute:: segment_duration


   .. py:attribute:: sigma


   .. py:attribute:: T2S


   .. py:attribute:: values


   .. py:method:: plot_ramsey_contrast(ramsey_duration)

      Plot the analytical and simulated Ramsey contrast.

      The analytical contrast :math:`\exp(-t^2 / T_2^{*2})` is plotted together
      with the contrast returned by the parent ``NoiseTimeTrace`` class.

      :param ramsey_duration: Duration over which the Ramsey signal
                              is evaluated.
      :type ramsey_duration: int
