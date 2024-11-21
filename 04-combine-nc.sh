#!/usr/bin/env bash

# Combine along time dimension
INDIR="CHELSA-nc-amazon"
OUTDIR="CHELSA-combined"
mkdir -p "$OUTDIR"

for var in "pr" "rsds" "tas" "tasmax" "tasmin"; do
  ncecat -u "time" $(find $INDIR -name "CHELSA_$var_*.nc" | sort) "$OUTDIR/$var.nc" &
done

wait
