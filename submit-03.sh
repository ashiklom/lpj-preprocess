#!/usr/bin/env bash
#SBATCH --account=s2958
#SBATCH --time=03:00:00
#SBATCH --job-name=tif2nc
#SBATCH --output=logs/tif2nc-%j.log

srun pixi run python 03-chelsa-tif2nc.py
