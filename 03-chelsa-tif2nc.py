from pathlib import Path
import re
from multiprocessing import Pool

import xarray as xr
import pandas as pd

def parse_fname(cfile: Path|str):
    m = re.match(r".*CHELSA_([a-zA-Z0-9]+)_(\d+)_(\d+)_(\d+)_V.*", str(cfile))
    if m is None:
        raise ValueError(f"Invalid file name: {cfile}")
    varname = m.group(1)
    # dt = np.array(np.datetime64(f"{m.group(4)}-{m.group(3)}-{m.group(2)}"), dtype="datetime64[ns]")
    dt = pd.date_range(f"{m.group(4)}-{m.group(3)}-{m.group(2)}", periods=1)
    return varname, dt

def preprocess_file(fname: Path|str):
    varname, dt = parse_fname(fname)
    dat = xr.open_dataset(fname, engine="rasterio")
    result = (dat.squeeze("band", drop=True).
              rename_dims({"x": "lon", "y": "lat"}).
              expand_dims(time=dt).
              assign_coords(time=("time", dt)).
              rename_vars({"band_data": varname, "x": "lon", "y": "lat"}))
    return result

def convert_file(fname: Path) -> Path:
    outdir = Path("CHELSA-nc")
    outdir.mkdir(exist_ok=True)
    outfile = outdir / fname.with_suffix(".nc").name
    dat = preprocess_file(fname)
    enc = {vname: {"zlib": True, "complevel": 9} for vname in ['lon', 'lat'] + list(dat.keys())}
    dat.to_netcdf(outfile, engine="h5netcdf", encoding = enc)
    return outfile

if __name__ == "__main__":
    clipped_dir = Path("CHELSA-clipped/")
    flist = sorted(clipped_dir.glob("*.tif"))

    with Pool() as pool:
        pool.map(convert_file, flist)
