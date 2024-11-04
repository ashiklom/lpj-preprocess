# Preprocessing CHELSA data for LPJ

1. `download-chelsa.sh` -- Download CHELSA data into `CHELSA-raw/`

2. `apply-land-mask.sh` -- Replace non-land data with NODATA (to shrink volumes later). Puts results in `CHELSA-clipped/`.

3. `chelsa-tif2nc.py` -- Convert clipped CHELSA files into NetCDF-4 (with Zlib compression).
