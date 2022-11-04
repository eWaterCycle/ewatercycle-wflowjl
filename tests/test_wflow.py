import shutil
import urllib
import pytest
from pywflow import WflowBMI


staticmaps_src = "https://github.com/visr/wflow-artifacts/releases/download/v0.2.1/staticmaps-lahn.nc"
forcing_src = "https://github.com/visr/wflow-artifacts/releases/download/v0.2.0/forcing-lahn.nc"
config_src = "./tests/hbv_config.toml"


@pytest.fixture(scope="session")
def model_config(tmp_path_factory):
    tempdir = tmp_path_factory.mktemp("data")

    urllib.request.urlretrieve(staticmaps_src, tempdir / "staticmaps-lahn.nc")
    urllib.request.urlretrieve(forcing_src, tempdir / "forcing-lahn.nc")

    config_dest = tempdir / "hbv_config.toml"
    shutil.copy(config_src, config_dest)

    return str(config_dest)


def test_bmi(model_config):
    model = WflowBMI()
    model.initialize(model_config)
