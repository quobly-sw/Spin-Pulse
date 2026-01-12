
spin_pulse.environment.noise.white
==================================

.. py:module:: spin_pulse.environment.noise.white



Classes
-------

.. autoapisummary::

   spin_pulse.environment.noise.white.WhiteNoiseTimeTrace


Module Contents
---------------


.. py:class:: WhiteNoiseTimeTrace(T2S, duration, segment_duration, seed = None)

   Bases: :py:obj:`spin_pulse.environment.noise.noise_time_trace.NoiseTimeTrace`


   Generate a white noise time trace.

   This class constructs a noise trace of length ``duration`` where each
   time step is drawn from an independent Gaussian distribution. The noise
   intensity is determined by the coherence time ``T2S`` that fixes the standard
   deviation :math:`\sqrt{2/T_2^*}`. White noise corresponds to a flat
   power spectral density and requires ``segment_duration = 1``.

   .. attribute:: - segment_duration

      Always equal to 1 for white noise.

      :type: int

   .. attribute:: - sigma

      Standard deviation controlling the noise intensity.

      :type: float

   .. attribute:: - T2S

      Coherence time parameter determining the noise intensity.

      :type: float

   .. attribute:: - values

      Noise samples of length ``duration``.

      :type: ndarray

   Initialize a white noise time trace for spin qubit simulations.

   Each value of the trace is drawn independently from a Gaussian
   distribution with zero mean and standard deviation :math:`\sqrt{2/T_2^*}`.
   The ``segment_duration`` parameter must be equal to 1, since white
   noise has no temporal correlations.

   :param T2S: Coherence time parameter determining the noise intensity.
   :type T2S: float
   :param duration: Total number of time steps in the noise trace.
   :type duration: int
   :param segment_duration: Must be equal to 1 for white noise.
   :type segment_duration: int
   :param seed: Optional seed for reproducible random
                number generation.
   :type seed: int | None

   :returns: The generated noise values are stored in ``self.values``.
   :rtype: None


   .. py:attribute:: segment_duration
      :value: 1



   .. py:attribute:: sigma


   .. py:attribute:: values


   .. py:attribute:: T2S


   .. py:method:: plot_ramsey_contrast(ramsey_duration)

      Plot analytical and numerical Ramsey contrast for white noise.

      The plot overlays:

      - the analytical exponential decay expected for white noise,
      - the numerical contrast computed from the generated time trace.

      :param ramsey_duration: Number of time steps used in the
                              Ramsey experiment evaluation.
      :type ramsey_duration: int

      :returns: The function produces a plot of the Ramsey contrast.
      :rtype: None
