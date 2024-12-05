#!/usr/bin/env bash

OUTDIR="LPJ-resampled-amazon"
mkdir -p "$OUTDIR"

# SOIL="/discover/nobackup/projects/LPJ/LPJ_inputs/Soil/soil_global_hd_filled.nc"
LANDUSE="/discover/nobackup/projects/LPJ/LPJ_inputs/LandUseChange/TRENDYv13/luhv2_1700-2024_05bil.nc"

GRIDFILE="chelsa-amazon-grid"

# cdo griddes "CHELSA-combined-amazon/pr.nc" | sed '0,/gridID 2/d' | sed 's/generic/lonlat/' > $GRIDFILE
# cat $GRIDFILE
#
# ncks -4 -x -v lon_bnds,lat_bnds $SOIL _soil.nc
# cdo -remapcon,"$GRIDFILE" _soil.nc "$OUTDIR/$(basename $SOIL)" &

# cdo -delvar,primn_to_c4ann "$LANDUSE" _luh.nc
ncks -4 -x -v primn_to_c4ann "$LANDUSE" _luh.nc
cdo -remapcon,"$GRIDFILE" _luh.nc "$OUTDIR/$(basename $LANDUSE)"

# wait
# rm -rf _soil.nc
