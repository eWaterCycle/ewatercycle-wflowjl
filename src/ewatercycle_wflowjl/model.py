from pathlib import Path
from typing import Optional
from ewatercycle.base.model import eWaterCycleModel, LocalModel
from bmipy import Bmi
from pydantic import PrivateAttr, model_validator
from grpc4bmi.bmi_julia_model import BmiJulia
from ewatercycle_wflowjl.forcing.forcing import WflowJlForcing
from ewatercycle.base.parameter_set import ParameterSet
import toml
from ewatercycle.util import get_time
from juliacall import JuliaError
from juliacall import Main as jl

# def find_dtype(julia_type: str) -> str:
#     """Find the Julia type from the Wflow `bmi.get_var_type` output."""
#     julia_type_fmt = r"(float\d{2})|(int\d{2})|(bool)"
#     match = re.search(julia_type_fmt, julia_type)
#     if match is None:
#         msg = ""
#         raise ValueError(msg)
#     return match.group()


def _iso_to_wflow(time):
    dt = get_time(time)
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


class WflowJlMixins(eWaterCycleModel):
    forcing: Optional[WflowJlForcing] = None
    parameter_set: ParameterSet

    _config: dict = PrivateAttr()

    @model_validator(mode="after")
    def _initialize_config(self):
        """Load config from parameter set and update with forcing info."""
        cfg = toml.load(self.parameter_set.directory / self.parameter_set.config)

        if self.forcing is not None:
            raise NotImplementedError()

        self._config = cfg

    def _make_cfg_file(self, **kwargs) -> Path:
        """Create a new wflow config file and return its path."""
        if "start_time" in kwargs:
            self._config["starttime"] = _iso_to_wflow(kwargs["start_time"])
        if "end_time" in kwargs:
            self._config["endtime"] = _iso_to_wflow(kwargs["end_time"])

        config_file = self._cfg_dir / "wflow_ewatercycle.toml"

        self._config["state"]["path_input"] = str(Path(self.parameter_set.directory) / self._config["state"]["path_input"])
        self._config["state"]["path_output"] = str(Path(self.parameter_set.directory) / self._config["state"]["path_output"])
        self._config["input"]["path_forcing"] = str(Path(self.parameter_set.directory) / self._config["input"]["path_forcing"])
        self._config["input"]["path_static"] = str(Path(self.parameter_set.directory) / self._config["input"]["path_static"])
        self._config["output"]["path"] = str(Path(self.parameter_set.directory) / self._config["output"]["path"])
        self._config["csv"]["path"] = str(Path(self.parameter_set.directory) / self._config["csv"]["path"])
        self._config["netcdf"]["path"] = str(Path(self.parameter_set.directory) / self._config["netcdf"]["path"])

        with config_file.open(mode="w") as f:
            f.write(toml.dumps(self._config))

        return config_file


def install_wflow():
    jl.seval("import Pkg")
    jl.Pkg.add(name="Wflow", rev="BMI")
    jl.Pkg.add("BasicModelInterface")


def check_wflow_install():
    try:
        jl.seval("using Wflow")
    except JuliaError(match="not found in current path"):
        install_wflow()


class WflowBmi(BmiJulia):
    @classmethod
    def from_name(cls, model_name, implementation_name='BasicModelInterface'):
        m = super().from_name(model_name, implementation_name)
        return m

    def __init__(self):
        check_wflow_install()
        
        m = self.from_name("Wflow.Model", implementation_name="Wflow.BMI")
        super().__init__(m.model, m.implementation)


class WflowJl(WflowJlMixins, LocalModel):
    bmi_class: type[Bmi] = WflowBmi
