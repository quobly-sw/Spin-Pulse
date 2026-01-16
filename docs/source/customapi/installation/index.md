# Installation


**Installing with `pip`**

```bash
    pip install spin-pulse
```

<!-- **Installing with  `conda`**

Need to see with Matthieu and sortware team for conda installation.

```bash
    conda install -c conda-forge spinpulse
``` -->

**Installing the version directly from github**

```bash
    git clone https://github.com/quobly-sw/SpinPulse.git
    cd spin-pulse
    pip install .
```

This installs the package and its dependencies.

**Requirements**

The core packages **`SpinPulse`** requires are:

- python 3.11+
- [numpy](http://www.numpy.org/)
- [scipy](https://www.scipy.org/)
- [numba](http://numba.pydata.org/)
- [tqdm](https://github.com/tqdm/tqdm)
- [qiskit](https://github.com/Qiskit/qiskit)


**Documentation toolchain**

To build the API documentation locally:

```bash
    pip install .[docs]
    sphinx-build -b html docs/source docs/build/html
```

To update the notebooks visible in the documentation:
```bash
    export TQDM_DISABLE=1; for f in examples/*.py; do jupytext --to notebook --execute "$f" -o "docs/source/customapi/tutorials/$(basename "${f%.py}.ipynb")"; done
```

**Verifying your installation**

```bash
    from spin_pulse import HardwareSpecs, PulseSequence
    print("SpinPulse is correctly installed.")
```
