#!/usr/bin/env bash
#SBATCH --account=s2958
#SBATCH --time=08:00:00
#SBATCH --job-name=resample
#SBATCH --output=logs/resample-%j.log
#SBATCH --no-requeue

srun pixi run bash 07-resample-land-soil.sh
