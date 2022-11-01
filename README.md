## Badges

(Customize these badges with your own links, and check https://shields.io/ or https://badgen.net/ to see which other badges are available.)

| fair-software.eu recommendations | |
| :-- | :--  |
| (1/5) code repository              | [![github repo badge](https://img.shields.io/badge/github-repo-000.svg?logo=github&labelColor=gray&color=blue)](https://github.com/eWaterCycle/pywflow) |
| (2/5) license                      | [![github license badge](https://img.shields.io/github/license/eWaterCycle/pywflow)](https://github.com/eWaterCycle/pywflow) |
| (3/5) community registry           | [![RSD](https://img.shields.io/badge/rsd-pywflow-00a3e3.svg)](https://www.research-software.nl/software/pywflow) [![workflow pypi badge](https://img.shields.io/pypi/v/pywflow.svg?colorB=blue)](https://pypi.python.org/project/pywflow/) |
| (4/5) citation                     | [![DOI](https://zenodo.org/badge/DOI/<replace-with-created-DOI>.svg)](https://doi.org/<replace-with-created-DOI>) |
| (5/5) checklist                    | [![workflow cii badge](https://bestpractices.coreinfrastructure.org/projects/<replace-with-created-project-identifier>/badge)](https://bestpractices.coreinfrastructure.org/projects/<replace-with-created-project-identifier>) |
| howfairis                          | [![fair-software badge](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B-yellow)](https://fair-software.eu) |
| **Other best practices**           | &nbsp; |
| Static analysis                    | [![workflow scq badge](https://sonarcloud.io/api/project_badges/measure?project=eWaterCycle_pywflow&metric=alert_status)](https://sonarcloud.io/dashboard?id=eWaterCycle_pywflow) |
| Coverage                           | [![workflow scc badge](https://sonarcloud.io/api/project_badges/measure?project=eWaterCycle_pywflow&metric=coverage)](https://sonarcloud.io/dashboard?id=eWaterCycle_pywflow) |
| Documentation                      | [![Documentation Status](https://readthedocs.org/projects/pywflow/badge/?version=latest)](https://pywflow.readthedocs.io/en/latest/?badge=latest) |
| **GitHub Actions**                 | &nbsp; |
| Build                              | [![build](https://github.com/eWaterCycle/pywflow/actions/workflows/build.yml/badge.svg)](https://github.com/eWaterCycle/pywflow/actions/workflows/build.yml) |
| Citation data consistency               | [![cffconvert](https://github.com/eWaterCycle/pywflow/actions/workflows/cffconvert.yml/badge.svg)](https://github.com/eWaterCycle/pywflow/actions/workflows/cffconvert.yml) |
| SonarCloud                         | [![sonarcloud](https://github.com/eWaterCycle/pywflow/actions/workflows/sonarcloud.yml/badge.svg)](https://github.com/eWaterCycle/pywflow/actions/workflows/sonarcloud.yml) |
| MarkDown link checker              | [![markdown-link-check](https://github.com/eWaterCycle/pywflow/actions/workflows/markdown-link-check.yml/badge.svg)](https://github.com/eWaterCycle/pywflow/actions/workflows/markdown-link-check.yml) |

## How to use pywflow

Python wrapper for the Wflow.jl Basic Model Interface

The project setup is documented in [project_setup.md](project_setup.md). Feel free to remove this document (and/or the link to this document) if you don't need it.

## Installation

To install pywflow from GitHub repository, do:

```console
git clone https://github.com/eWaterCycle/pywflow.git
cd pywflow
python3 -m pip install .
```

If `juliacall` is confused by detecting both a Conda environment and a virtual environment, disable the automatic activation of conda's base environment with:
```console
conda config --set auto_activate_base false
```

## Documentation

Include a link to your project's full documentation here.

## Contributing

If you want to contribute to the development of pywflow,
have a look at the [contribution guidelines](CONTRIBUTING.md).

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [NLeSC/python-template](https://github.com/NLeSC/python-template).
