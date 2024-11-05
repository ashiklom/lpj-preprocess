#!/usr/bin/env bash

# Convert non-land values in CHELSA to NODATA (based on NaturalEarth)

# Generate list of files
FLIST_STR=$(find CHELSA-raw -type f | sort)
readarray -t FLIST <<< $FLIST_STR

NODATA=$(gdalinfo "${FLIST[0]}" | grep "NoData Value" | sed 's/.*NoData Value=//g')

OUTDIR="CHELSA-clipped"
mkdir -p "$OUTDIR"

for INFILE in "${FLIST[@]}"; do
  OUTFILE="$OUTDIR/$(basename $INFILE)"
  echo "$INFILE --> $OUTFILE"
  if [[ -f $OUTFILE ]]; then
    echo "Skipping..."
    continue
  fi
  cp $INFILE $OUTFILE
  # Note: Do this step asynchronously!
  gdal_rasterize \
    -burn $NODATA \
    -i \
    "land-polygons/ne_10m_land.shp" \
    "$OUTFILE" &
done

wait
echo "Done!"
