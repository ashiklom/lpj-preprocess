#!/usr/bin/env bash

# Combine along time dimension
ncecat -u "time" CHELSA-nc/CHELSA_tasmin_*.nc tasmin.nc
