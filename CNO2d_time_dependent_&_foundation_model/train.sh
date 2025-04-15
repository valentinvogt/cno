#!/bin/bash

#SBATCH --job-name=train-cno
#SBATCH --output=train-cno-%j.out
#SBATCH --error=train-cno-%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --gpus-per-node=8
#SBATCH --time=2-12:00:00
#SBATCH --mem-per-cpu=8192
#SBATCH --constraint=EPYC_7742
#SBATCH --mail-type=END

module load stack/2024-06
module load  gcc/12.2.0
module load python_cuda/3.11.6

python TrainCNO_time_L.py
