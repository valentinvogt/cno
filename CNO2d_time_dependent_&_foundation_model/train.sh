#!/bin/bash

#SBATCH --job-name=cno-train
#SBATCH --output=cno-train-%j.out
#SBATCH --error=cno-train-%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --gpus-per-node=8
#SBATCH --time=20:00:00
#SBATCH --mem-per-cpu=8192
#SBATCH --mail-type=END

module load stack/2024-06
module load  gcc/12.2.0
module load python_cuda/3.11.6

python TrainCNO_time_L.py
