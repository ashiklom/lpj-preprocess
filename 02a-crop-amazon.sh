#!/usr/bin/env bash

source ./bash_utils.sh

# Amazon bbox: http://bboxfinder.com/#-28.149503,-81.738281,12.640338,-34.101563
LEFT_X="-81.738281"
BOTTOM_Y="-28.149503"
RIGHT_X="-34.101563"
TOP_Y="12.640338"
BBOX_SRS="EPSG:4326"

OUTDIR="CHELSA-clipped-amazon"
mkdir -p "$OUTDIR"

# find CHELSA-clipped/ -type f | sort | head

for file in $(find CHELSA-clipped/ -type f | sort); do
  OUTFILE="$OUTDIR/$(basename $file)"
  echo "$file --> $OUTFILE"
  if [[ -f $OUTFILE ]]; then
    echo "Skipping because exists: $OUTFILE"
    continue
  fi
  gdal_translate \
    -projwin $LEFT_X $TOP_Y $RIGHT_X $BOTTOM_Y \
    -projwin_srs $BBOX_SRS \
    $file $OUTFILE &
  pwait 48
done
