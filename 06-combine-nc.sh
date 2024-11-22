#!/usr/bin/env bash

# Combine along time dimension
INDIR="CHELSA-nc-amazon"
OUTDIR="CHELSA-combined"
mkdir -p "$OUTDIR"

for var in "pr" "rsds" "tas" "tasmax" "tasmin"; do
  echo "Processing ${var}"
  OUTFILE="$OUTDIR/${var}.nc"
  if [[ -f $OUTFILE ]]; then
    echo "Skipping ${var} because ${OUTFILE} exists"
    continue
  fi
  ncecat -u "time" $(find $INDIR -name "CHELSA_${var}_*.nc" | sort) -o "$OUTFILE" &
done

wait
