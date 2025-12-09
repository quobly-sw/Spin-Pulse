# Installation


**Installing with `pip`**

Need to see with Matthieu and sortware team for PyPI installation.

```bash
    pip install spinpulse
```

**Installing with  `conda`**

Need to see with Matthieu and sortware team for conda installation.

```bash
    conda install -c conda-forge spinpulse
```

**Installing the version directly from github**

```bash
    git clone https://...
    cd spinpulse
    pip install .
```

This installs the package and its dependencies.

**Requirements**

The core packages `spinpulse` requires are:

- python 3.8+
- [numpy](http://www.numpy.org/)
- [scipy](https://www.scipy.org/)
- [numba](http://numba.pydata.org/)
- [tqdm](https://github.com/tqdm/tqdm)
- [quiskit](https://github.com/Qiskit/qiskit)


**Documentation toolchain**

To build the API documentation locally:

```bash
    pip install .[docs]
    sphinx-build -b html docs/source docs/build/html
```

**Verifying your installation**

```bash
    from spinpulse import HardwareSpecs, PulseSequence
    print("SpinPulse is correctly installed.")
```
