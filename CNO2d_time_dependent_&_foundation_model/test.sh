#!/bin/bash

#SBATCH --job-name=eval-cno
#SBATCH --output=eval-cno-%j.out
#SBATCH --error=eval-cno-%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6
#SBATCH --gpus-per-node=2
#SBATCH --time=4:00:00
#SBATCH --mem-per-cpu=8192
#SBATCH --constraint=EPYC_7742

module load stack/2024-06
module load  gcc/12.2.0
module load python_cuda/3.11.6

python Eval.py
