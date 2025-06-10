#!/bin/bash

#SBATCH --job-name=ft-cno
#SBATCH --output=ft-cno-%j.out
#SBATCH --error=ft-cno-%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --gpus-per-node=2
#SBATCH --time=8:00:00
#SBATCH --mem-per-cpu=8192
#SBATCH --mail-type=END

module load stack/2024-06
module load  gcc/12.2.0
module load python_cuda/3.11.6

python TrainCNO_time_L.py
# python CNO_FineTune.py
