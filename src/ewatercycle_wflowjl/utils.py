import json
from pathlib import Path
import numpy as np


def get_geojson_locs(fname: str | Path) -> tuple[np.ndarray, np.ndarray]:
    with Path(fname).open(mode="r") as f:
        data = json.loads(f.read())
    
    npoints = len(data["features"])
    lats = np.zeros((npoints))
    lons = np.zeros((npoints))
    for ix in range(npoints):
        lons[ix], lats[ix] = data['features'][ix]['geometry']["coordinates"]
    return lats, lons
