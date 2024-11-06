#!/usr/bin/env bash
#SBATCH --account=s2958
#SBATCH --time=03:00:00
#SBATCH --job-name=landmask
#SBATCH --output=logs/landmask-%j.log

pixi run bash 02-apply-land-mask.sh
