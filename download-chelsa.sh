#!/usr/bin/env bash

OUTDIR="CHELSA-raw"
mkdir -p "$OUTDIR"
wget -i chelsa-paths-small.txt -nc -P "$OUTDIR"
