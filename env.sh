#!/usr/bin/env bash

module purge

module load \
  git/2.45.0 \
  python/GEOSpyD/Min24.4.0-0_py3.12 \
  gdal/3.7.2 \
  gnuParallel/20230722 \
  nco/5.1.7 \
  netcdf4/4.9.2-ser
