#!/usr/bin/env python

import xarray as xr
import numpy as np

dat = xr.open_dataset("CHELSA-raw/CHELSA_tasmin_01_01_1980_V.2.1.tif", engine="rasterio")

lat = dat.x.values
lon = dat.y.values

latgrid, longrid = np.meshgrid(lat, lon)
latgrid = np.reshape(latgrid, (-1))
longrid = np.reshape(longrid, (-1))

with open("chelsa_grid.txt", "w") as f:
    f.write("longitude,latitude\n")
    for i in range(len(latgrid)):
        f.write(f"{longrid[i]:.4f},{latgrid[i]:.4f}\n")
