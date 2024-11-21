#!/usr/bin/env bash
#SBATCH --account=s2958
#SBATCH --time=08:00:00
#SBATCH --job-name=combine
#SBATCH --output=logs/combine-%j.log
#SBATCH --no-requeue

srun pixi run bash 04-combine-nc.sh
