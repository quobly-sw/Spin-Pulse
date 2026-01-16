# Welcome to SpinPulse's documentation!

<!-- [![Tests](https://github.com/jcmgray/quimb/actions/workflows/tests.yml/badge.svg)]()
[![Code Coverage](https://codecov.io/gh/jcmgray/quimb/branch/main/graph/badge.svg)]()
[![Documentation Status](https://readthedocs.org/projects/quimb/badge/?version=latest)]()
[![Vermersch Paper](http://joss.theoj.org/papers/10.21105/joss.00819/status.svg)]()
[![PyPI](https://img.shields.io/pypi/v/quimb?color=teal)]() -->
[![Doc](https://img.shields.io/badge/Doc-dev-green.svg)](https://quobly-sw.github.io/SpinPulse)
![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
[![arXiv](https://img.shields.io/badge/arXiv-2601.10435-b31b1b.svg)](https://arxiv.org/abs/2601.10435)


<!-- [`spinpulse`](https://github.com/) -->
We introduce **`SpinPulse`**, an open-source **`python`** package for simulating spin qubit-based quantum computers at the pulse-level.
**`SpinPulse`** models the specific physics of spin qubits, particularly through the inclusion of classical non-Markovian noise. This enables realistic simulations of native gates and noise-accurate quantum circuits, in order to support hardware development.


In **`SpinPulse`**, a quantum circuit defined in [**`Qiskit`**](https://qiskit.org/) is first transpiled into the native gate set of our model (see (1) in {numref}`fig:spinpulse_global_view`) and then converted to a pulse sequence (see (2) in {numref}`fig:spinpulse_global_view`).

This pulse sequence is subsequently integrated numerically in the presence of a simulated noisy experimental environment (see (3) in {numref}`fig:spinpulse_global_view`), which can account for non-Markovian noise, a key noise feature of spin qubits.
We showcase workflows including transpilation, pulse-level compilation, hardware benchmarking, quantum error mitigation, and large-scale simulations via integration with the tensor-network library [**`Quimb`**](https://quimb.readthedocs.io/).

We expect **`SpinPulse`** to be a valuable open-source tool for the quantum computing community, fostering efforts to devise
high-fidelity quantum circuits and improved strategies for quantum error mitigation and correction, and we encourage people to join this effort and to propose improvement and feature tailored to spin-qubit technology.

This documentation provides comprehensive guides, API references, and examples to help you get started with SpinPulse.
The documentation is complemented by a paper published in arxiv. <!-- [arxiv](link). -->

```{figure} customapi/figures/global_fig.png
:name: fig:spinpulse_global_view
:width: 100%
:align: center
**`SpinPulse`** working scheme.
```

## Package Modules
::::{grid} 3
:::{grid-item-card} Transpilation
The {doc}`transpilation <autoapi/spin_pulse/transpilation/index>` module provides a set of classes that enable the simulation of quantum  circuits defined in `Qiskit` on silicon-based spin-qubit hardware models.
:::

:::{grid-item-card} Noise Environment
The {doc}`environment <autoapi/spin_pulse/environment/index>` module provides a set of classes for defining and configuring a quantum experimental environment tailored to spin-qubit systems.

:::


:::{grid-item-card} Qubits Characterization
The {doc}`characterization <autoapi/spin_pulse/characterization/index>`module provides a set of functions for characterizing spin-qubit control operations and quantifying noise strength.

:::
::::

## Installation
To install the package, consult the {doc}`installation <customapi/installation/index>` page.

## Package tutorials

The following tutorial notebooks, generated from the notebooks in ``docs/source/customapi/tutorials``,
illustrate the usage of the **``SpinPulse``** package steps by steps.


- {doc}`BasicUsage <customapi/tutorials/BasicUsage>`
  Introduces the core workflow of **`SpinPulse`**, from environment definition to pulse-level simulation.

- {doc}`TimeTracesExamples <customapi/tutorials/TimeTracesExamples>`
  Shows the generation and analysis of noise time traces used in pulse-level simulations.

- {doc}`ParametrizingfromQPUSpecs <customapi/tutorials/ParametrizingfromQPUSpecs>`
  Explains how to parametrize SpinPulse simulations directly from hardware (QPU) specifications.

- {doc}`RamseySpinEcho <customapi/tutorials/RamseySpinEcho>`
  Illustrates Ramsey and spin-echo experiments for characterizing dephasing and coherence properties of spin qubits.

- {doc}`AverageSuperoperatorsNoisyGates <customapi/tutorials/AverageSuperoperatorsNoisyGates>`
  Shows how to compute average quantum channels for noisy native gates under stochastic noise realizations.

- {doc}`BernsteinVazirani <customapi/tutorials/BernsteinVazirani>`
  Demonstrates the execution of the Bernstein–Vazirani algorithm within the **`SpinPulse`** package.

- {doc}`QuimbSimulation <customapi/tutorials/QuimbSimulation>`
Presents an example of integrating **`SpinPulse`** with **`Quimb`** for tensor-network-based circuit simulation.


## API documentation

The {doc}`API documentation <autoapi/spin_pulse/index>` provides a detailed description of the **`SpinPulse`** package architecture, including its core modules, classes and functions.


## Citing

If you use **`SpinPulse`** in your research work, please cite our publication

```latex
@misc{vermersch2025spinpulse,
      title={The SpinPulse library for transpilation and noise-accurate simulation of spin qubit quantum computers},
      author={Beno\^it Vermersch, Oscar Gravier, Nathan Miscopein, Julia Guignon, Carlos Ramos Marim\'on, Jonathan Durandau, Matthieu Dartiailh, Tristan Meunier and Valentin Savin},
      year={2026},
      eprint={2601.10435},
      archivePrefix={arXiv},
      primaryClass={quant-ph},
      url={https://arxiv.org/abs/2601.10435},
}
```


```{toctree}
:maxdepth: 1
:caption: Contents

Installation Guide <customapi/installation/index>

Tutorials <customapi/tutorials/index_simple>

API Reference <autoapi/spin_pulse/index>

Github <https://github.com/quobly-sw/SpinPulse>
```
