from pathlib import Path
import re
from multiprocessing import Pool
import subprocess
from tqdm import tqdm

import xarray as xr
import pandas as pd

def parse_fname(cfile: Path|str):
    m = re.match(r".*CHELSA_([a-zA-Z0-9]+)_(\d+)_(\d+)_(\d+)_V.*", str(cfile))
    if m is None:
        raise ValueError(f"Invalid file name: {cfile}")
    varname = m.group(1)
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
    if outfile.exists():
        print(f"Skipping because target exists: {outfile}")
        return outfile
    dat = preprocess_file(fname)
    enc = {vname: {"zlib": True, "complevel": 9} for vname in ['lon', 'lat'] + list(dat.keys())}
    dat.to_netcdf(outfile, engine="h5netcdf", encoding = enc)
    return outfile

def is_clipped(fname: Path|str):
    result_raw = subprocess.run(["gdalinfo", fname], capture_output=True)
    return ("LAND_CLIPPED=1" in result_raw.stdout.decode("utf-8"))

if __name__ == "__main__":
    clipped_dir = Path("CHELSA-clipped/")
    flist = sorted(clipped_dir.glob("*.tif"))
    flist_sub = [f for f in tqdm(flist) if is_clipped(f)]
    print(f"Converting {len(flist_sub)}/{len(flist)} files")

    with Pool(35) as pool:
        pool.map(convert_file, flist_sub)
