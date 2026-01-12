
spin_pulse.environment.noise.pink
=================================

.. py:module:: spin_pulse.environment.noise.pink



Classes
-------

.. autoapisummary::

   spin_pulse.environment.noise.pink.PinkNoiseTimeTrace


Functions
---------

.. autoapisummary::

   spin_pulse.environment.noise.pink.get_pink_noise
   spin_pulse.environment.noise.pink.get_pink_noise_with_repetitions


Module Contents
---------------


.. py:function:: get_pink_noise(segment_duration, seed = None)

   Generate a single segment of pink noise using an inverse FFT method.

   The generated sequence has length ``segment_duration`` and follows a
   spectral density proportional to ``1/freq``.

   This implementation is adapted from the Matlab implementation of
   the algorithm described in [Little2007].

   .. rubric:: References

   [Little2007] M. A. Little, P. E. McSharry, S. J. Roberts,
   D. A. E. Costello, and I. M. Moroz,
   "Exploiting nonlinear recurrence and fractal scaling properties
   for voice disorder detection",
   BioMedical Engineering OnLine, 6:23 (2007).

   :param segment_duration: Number of time points in the generated
                            pink noise segment.
   :type segment_duration: int
   :param seed: Optional seed for reproducible random
                number generation.
   :type seed: int | None

   :returns:

             Array of length ``segment_duration`` containing a
               realization of pink noise.
   :rtype: ndarray

   :raises ValueError: If ``segment_duration`` is odd.


.. py:function:: get_pink_noise_with_repetitions(duration, segment_duration, seed = None)

   Generate pink noise of a given total duration by repeating segments.

   A base pink noise segment of length ``segment_duration`` is generated
   repeatedly and concatenated until the total length reaches ``duration``.
   A low frequency cutoff of ``1/segment_duration`` is implicitly imposed.

   :param duration: Total number of time points in the final noise trace.
   :type duration: int
   :param segment_duration: Length of each repeated pink noise segment.
   :type segment_duration: int
   :param seed: Optional seed for reproducible random
                number generation.
   :type seed: int | None

   :returns: Pink noise trace of length ``duration``.
   :rtype: ndarray


.. py:class:: PinkNoiseTimeTrace(T2S, duration, segment_duration, seed = None)

   Bases: :py:obj:`spin_pulse.environment.noise.noise_time_trace.NoiseTimeTrace`


   Generate a pink noise time trace with a 1/f power spectral density.

   This class constructs a noise trace of length ``duration`` where the
   spectral density follows a pink noise distribution proportional to
   ``1/f``. A low-frequency cutoff is enforced at ``1/segment_duration`` by
   building the trace from repeated pink noise segments. The parameter ``T2S``
   determines the noise intensity through the scaling factor ``S0`` defined as::

       S0 = 1 / (4 * pi^2 * log(segment_duration) * T2S^2)

   The internal array ``values`` contains the generated noise samples and
   is used by methods such as ``ramsey_contrast`` to evaluate the effect of
   pink noise on qubit coherence.

   .. attribute:: - segment_duration

      Length of each pink noise segment.

      :type: int

   .. attribute:: - S0

      Scaling factor controlling the noise intensity.

      :type: float

   .. attribute:: - T2S

      Coherence time parameter determining the noise intensity.

      :type: float

   .. attribute:: - sigma

      Standard deviation of the generated noise values.

      :type: float

   .. attribute:: - values

      Noise values of length ``duration``.

      :type: ndarray

   Create a pink noise time trace for spin qubit simulations.

   The generated noise satisfies a spectral density proportional to
   ``1/(f*ts)`` with a low frequency cutoff ``f_min=1/segment_duration``.
   The parameter ``T2S`` sets the noise intensity through the relation
   ``S0 = 1 / (4 * pi^2 * log(segment_duration) * T2S^2)``. The internal
   noise trace has length ``duration`` and is constructed by repeating
   pink noise segments.

   :param T2S: Coherence time parameter determining the noise
               intensity.
   :type T2S: float
   :param duration: Total number of time steps in the noise trace.
   :type duration: int
   :param segment_duration: Length of each pink noise segment.
   :type segment_duration: int
   :param seed: Optional seed for reproducible random
                number generation.
   :type seed: int | None

   :returns: The time trace is stored internally in ``self.values``.
   :rtype: None


   .. py:attribute:: segment_duration


   .. py:attribute:: values


   .. py:attribute:: S0


   .. py:attribute:: T2S


   .. py:attribute:: sigma


   .. py:method:: plot_ramsey_contrast(ramsey_duration)

      Plot analytical and numerical Ramsey contrast curves.

      This method overlays:
          - the analytical Gaussian contrast expected for pink noise,
          - a corrected analytical contrast that accounts for the
            frequency cutoff imposed by ``segment_duration``,
          - the numerical contrast obtained from the underlying noise trace.

      :param ramsey_duration: Number of time steps used in the
                              Ramsey experiment evaluation.
      :type ramsey_duration: int

      :returns: The function produces a plot of the Ramsey contrast.
      :rtype: None
