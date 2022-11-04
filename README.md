# pywflow
[![github repo badge](https://img.shields.io/badge/github-repo-000.svg?logo=github&labelColor=gray&color=blue)](https://github.com/eWaterCycle/pywflow)
[![fair-software badge](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B-yellow)](https://fair-software.eu)
[![github license badge](https://img.shields.io/github/license/eWaterCycle/pywflow)](https://github.com/eWaterCycle/pywflow)
[![build](https://github.com/eWaterCycle/pywflow/actions/workflows/build.yml/badge.svg)](https://github.com/eWaterCycle/pywflow/actions/workflows/build.yml)
[![workflow scc badge](https://sonarcloud.io/api/project_badges/measure?project=eWaterCycle_pywflow&metric=coverage)](https://sonarcloud.io/dashboard?id=eWaterCycle_pywflow)


<!---
[![RSD](https://img.shields.io/badge/rsd-pywflow-00a3e3.svg)](https://www.research-software.nl/software/pywflow)
[![DOI](https://zenodo.org/badge/DOI/<replace-with-created-DOI>.svg)](https://doi.org/<replace-with-created-DOI>)
[![Documentation Status](https://readthedocs.org/projects/pywflow/badge/?version=latest)](https://pywflow.readthedocs.io/en/latest/?badge=latest)

-->

`pywflow` is a wrapper for the Basic Model Interface of the [Wflow.jl hydrological model](https://github.com/Deltares/Wflow.jl) developed by [Deltares](https://www.deltares.nl/en/).

This BMI wrapper can be used to interface with other models through Python, or through [grpc4bmi](https://github.com/eWaterCycle/grpc4bmi)

## Installation

To install `pywflow` from the GitHub repository, do:

```console
git clone https://github.com/eWaterCycle/pywflow.git
cd pywflow
pip install .
```

You can use either an existing Julia installation with `Wflow.jl` installed, or rely on `juliacall` to manage Julia and the dependencies. `juliacall` will set up Julia and `Wflow.jl` the first time that `pywflow` is run.


Note: if `juliacall` is confused by detecting both a Conda environment and a virtual environment, disable the automatic activation of conda's base environment with:
```console
conda config --set auto_activate_base false
```
And restart the shell/environment.

## Usage
```python
from pywflow import WflowBMI

# Config files and example data are available at:
#  https://deltares.github.io/Wflow.jl/stable/user_guide/sample_data/
config_file = "~/sbm_config.toml"

model = WflowBMI()
model.initialize(config_file)

model.update()  # Advance the model one time step
```

For a short overview of the base functionality, see the [example notebook](./notebooks/pywflow_example.ipynb).

<!---
## Documentation

Include a link to your project's full documentation here.

## Contributing

If you want to contribute to the development of pywflow,
have a look at the [contribution guidelines](CONTRIBUTING.md).
-->

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [NLeSC/python-template](https://github.com/NLeSC/python-template).
