"""Forcing related functionality for wflow."""

from datetime import datetime
from pathlib import Path

from ewatercycle.base.forcing import DefaultForcing
from ewatercycle.esmvaltool.builder import RecipeBuilder
from ewatercycle.esmvaltool.schema import Dataset


class WflowJlForcing(DefaultForcing):
    """Container for wflow forcing data.

    Args:
        directory: Directory where forcing data files are stored.
        start_time: Start time of forcing in UTC and ISO format string e.g.
            'YYYY-MM-DDTHH:MM:SSZ'.
        end_time: End time of forcing in UTC and ISO format string e.g.
            'YYYY-MM-DDTHH:MM:SSZ'.
        shape: Path to a shape file. Used for spatial selection.
        netcdfinput (str) = "inmaps.nc": Path to forcing file.
        Inflow (str) = None: Variable name of inflow data in input file.
    """

    netcdfinput: str = "inmaps.nc"
    Inflow: str | None = None

    @classmethod
    def generate(  # type: ignore
        cls,
        dataset: str | Dataset | dict,
        start_time: str,
        end_time: str,
        shape: str,
        dem_file: str,
        directory: str | None = None,
        extract_region: dict[str, float] | None = None,
    ) -> "WflowJlForcing":
        """Generate forcings for a model.

        The forcing is generated with help of
        `ESMValTool <https://esmvaltool.org/>`_.

        Args:
            dataset: Dataset to get forcing data from.
                When string is given a predefined dataset is looked up in
                :py:const:`ewatercycle.esmvaltool.datasets.DATASETS`.
                When dict given it is passed to
                :py:class:`ewatercycle.esmvaltool.models.Dataset` constructor.
            start_time: Start time of forcing in UTC and ISO format string e.g.
                'YYYY-MM-DDTHH:MM:SSZ'.
            end_time: nd time of forcing in UTC and ISO format string e.g.
                'YYYY-MM-DDTHH:MM:SSZ'.
            shape: Path to a shape file. Used for spatial selection.
            directory:  Directory in which forcing should be written.
                If not given will create timestamped directory.
            dem_file: Name of the dem_file to use.
            extract_region: Region specification, dictionary must
                contain `start_longitude`, `end_longitude`, `start_latitude`,
                `end_latitude`
        """
        return super().generate(
            dataset=dataset,
            start_time=start_time,
            end_time=end_time,
            shape=shape,
            dem_file=dem_file,
            directory=directory,
            extract_region=extract_region,
        )

    @classmethod
    def _build_recipe(
        cls,
        start_time: datetime,
        end_time: datetime,
        shape: Path,
        dataset: Dataset | str | dict,
        **model_specific_options,
    ):
        extract_region = model_specific_options["extract_region"]
        return build_wflow_recipe(
            start_year=start_time.year,
            end_year=end_time.year,
            shape=shape,
            dataset=dataset,
            dem_file=model_specific_options["dem_file"],
            extract_region=extract_region,
        )

    @classmethod
    def _recipe_output_to_forcing_arguments(cls, recipe_output, model_specific_options):
        first_file = next(iter(recipe_output.values()))
        return {
            "netcdfinput": first_file,
        }


def build_wflow_recipe(
    start_year: int,
    end_year: int,
    shape: Path,
    dataset: Dataset | str | dict,
    dem_file: str,
    extract_region: dict[str, float] | None = None,
):
    """Build an ESMValTool recipe for the WFlow hydrological model.

    Args:
        start_year: Start year of forcing.
        end_year: End year of forcing.
        shape: Path to a shape file. Used for spatial selection.
        dataset: Dataset to get forcing data from.
            When string is given a predefined dataset is looked up in
            :py:const:`ewatercycle.esmvaltool.datasets.DATASETS`.
            When dict given it is passed to
            :py:class:`ewatercycle.esmvaltool.models.Dataset` constructor.
        dem_file: Name of the dem_file to use.
        extract_region: Region specification, dictionary must
            contain `start_longitude`, `end_longitude`, `start_latitude`,
            `end_latitude`
    """
    partial = (
        RecipeBuilder()
        .title("Generate forcing for the WFlow hydrological model")
        .dataset(dataset)
        .start(start_year)
        .end(end_year)
    )
    if extract_region is None:
        if dataset == "ERA5":
            magic_pad = 3  # TODO why 3?
        else:
            magic_pad = 9  # CMIP datasets require more padding?
        partial = partial.region_by_shape(shape, pad=magic_pad)
    else:
        partial = partial.region(
            start_longitude=extract_region["start_longitude"],
            end_longitude=extract_region["end_longitude"],
            start_latitude=extract_region["start_latitude"],
            end_latitude=extract_region["end_latitude"],
        )
    if dataset == "ERA5":
        return (
            partial.add_variables(["tas", "pr", "psl", "rsds"])
            .add_variable("rsdt", mip="CFday")
            .add_variable("orog", mip="fx", start_year=False, end_year=False)
            .script(
                str((Path(__file__).parent / "diagnostic_script.py").absolute()),
                {
                    "basin": shape.stem,
                    "dem_file": dem_file,
                    "regrid": "area_weighted",
                },
            )
            .build()
        )

    else:
        return (
            partial.add_variables(["tas", "pr", "rsds"])
            .add_variable("orog", mip="fx", start_year=False, end_year=False)
            .script(
                str((Path(__file__).parent / "diagnostic_script.py").absolute()),
                {
                    "basin": shape.stem,
                    "dem_file": dem_file,
                    "regrid": "area_weighted",
                },
            )
            .build()
        )
