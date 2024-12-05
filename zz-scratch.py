#!/usr/bin/env python

import xarray as xr

orig_luh_path = "/discover/nobackup/projects/LPJ/LPJ_inputs/LandUseChange/TRENDYv13/luhv2_1700-2024_05bil.nc"
orig_luh = xr.open_dataset(orig_luh_path, decode_times=False)

target = xr.open_dataset("CHELSA-combined-amazon/pr.nc", decode_times=False)
tlat = target["lat"]
tlon = target["lon"]
luh_resampled = orig_luh.interp(lat=tlat, lon=tlon, method="nearest")

xmin = -81.7376392819
xmax = xmin + 5716 * 0.0083333333
ymax = 12.6373607006
ymin = ymax - 4895 * 0.0083333333
amazon = orig_luh.sel(lon = slice(xmin, xmax), lat = slice(ymin, ymax))



luh = xr.open_dataset("LPJ-resampled-amazon/luhv2_1700-2024_05bil.nc", decode_times=False)
soil = xr.open_dataset("LPJ-resampled-amazon/soil_global_hd_filled.nc")

################################################################################

import rasterio as rio
from rasterio.plot import show

drio = rio.open("CHELSA-clipped/CHELSA_tasmin_01_01_1980_V.2.1.tif")
show(drio)

# from matplotlib import pyplot as plt
# drio_npy = drio.read(1)
# plt.imshow(drio_npy)
# plt.show()

from pathlib import Path
import re
import xarray as xr
import pandas as pd

def parse_fname(cfile):
    m = re.match(r".*CHELSA_([a-zA-Z0-9]+)_(\d+)_(\d+)_(\d+)_V.*", str(cfile))
    if m is None:
        raise ValueError(f"Invalid file name: {cfile}")
    varname = m.group(1)
    # dt = np.array(np.datetime64(f"{m.group(4)}-{m.group(3)}-{m.group(2)}"), dtype="datetime64[ns]")
    dt = pd.date_range(f"{m.group(4)}-{m.group(3)}-{m.group(2)}", periods=1)
    return varname, dt

def preprocess_file(fname):
    varname, dt = parse_fname(fname)
    dat = xr.open_dataset(fname, engine="rasterio")
    result = (dat.squeeze("band", drop=True).
              rename_dims({"x": "lon", "y": "lat"}).
              expand_dims(time=dt).
              assign_coords(time=("time", dt)).
              rename_vars({"band_data": varname, "x": "lon", "y": "lat"}))
    return result

def convert_file(fname):
    outdir = Path("CHELSA-nc")
    outdir.mkdir(exist_ok=True)
    outfile = outdir / fname.with_suffix(".nc").name
    dat = preprocess_file(fname)
    enc = {vname: {"zlib": True, "complevel": 9} for vname in ['lon', 'lat'] + list(dat.keys())}
    dat.to_netcdf(outfile, engine="h5netcdf", encoding = enc)
    return outfile

fname = Path("CHELSA-clipped/CHELSA_tasmin_01_01_1980_V.2.1.tif")
