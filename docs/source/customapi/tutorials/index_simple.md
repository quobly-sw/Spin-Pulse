# Tutorials

Below are a few notebooks that explain the basics of `SpinPulse`.


```{toctree}
:numbered:
:maxdepth: 1

BasicUsage.ipynb
TimeTracesExamples.ipynb
ParametrizingfromQPUSpecs.ipynb
RamseySpinEcho.ipynb
AverageSuperoperatorsNoisyGates.ipynb
BernsteinVazirani.ipynb
QuimbSimulation.ipynb

```

## Details

- {doc}`BasicUsage <BasicUsage>`
  Introduces the core workflow of SpinPulse, from environment definition to pulse-level simulation.

- {doc}`TimeTracesExamples <TimeTracesExamples>`
  Shows the generation and analysis of noise time traces used in pulse-level simulations.

- {doc}`ParametrizingfromQPUSpecs <ParametrizingfromQPUSpecs>`
  Explains how to parametrize SpinPulse simulations directly from hardware (QPU) specifications.

- {doc}`RamseySpinEcho <RamseySpinEcho>`
  Illustrates Ramsey and spin-echo experiments for characterizing dephasing and coherence properties of spin qubits.

- {doc}`AverageSuperoperatorsNoisyGates <AverageSuperoperatorsNoisyGates>`
  Shows how to compute average quantum channels for noisy native gates under stochastic noise realizations.

- {doc}`BernsteinVazirani <BernsteinVazirani>`
  Demonstrates the execution of the Bernstein–Vazirani algorithm within the **`SpinPulse`** package.

- {doc}`QuimbSimulation <QuimbSimulation>`
Presents an example of integrating **`SpinPulse`** with **`Quimb`** for tensor-network-based circuit simulation.
