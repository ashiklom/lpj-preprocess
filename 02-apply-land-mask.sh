#!/usr/bin/env bash

# Convert non-land values in CHELSA to NODATA (based on NaturalEarth)

# Function for restricted parallelization
function pwait() {
  while [ $(jobs -p | wc -l) -ge $1 ]; do
    sleep 1
  done
}

# Generate list of files
if [[ $BASH_VERSION > 4.4 ]]; then
  FLIST_STR=$(find CHELSA-raw -type f | sort)
  readarray -t FLIST <<< $FLIST_STR
else
  # Older, jankier method, but should still work here
  echo "WARNING: Detected Bash < 4.4. Using older, less reliable method."
  FLIST=($(find CHELSA-raw -type f | sort))
fi

NODATA=$(gdalinfo "${FLIST[0]}" | grep "NoData Value" | sed 's/.*NoData Value=//g')
echo "Using NODATA value $NODATA"

OUTDIR="CHELSA-clipped"
mkdir -p "$OUTDIR"

for INFILE in "${FLIST[@]}"; do
  OUTFILE="$OUTDIR/$(basename $INFILE)"
  echo "$INFILE --> $OUTFILE"
  cp -n $INFILE $OUTFILE
  if gdalinfo "$OUTFILE" | grep -q "LAND_CLIPPED"; then
    echo "Skipping..."
    continue
  fi
  # Note: Do this step asynchronously!
  gdal_rasterize \
    -burn $NODATA \
    -i \
    "land-polygons/ne_10m_land.shp" \
    "$OUTFILE" && \
    gdal_edit -mo LAND_CLIPPED=1 "$OUTFILE" &
  pwait 35
done

echo "Done!"
