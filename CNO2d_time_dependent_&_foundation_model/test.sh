#!/bin/bash
#SBATCH --job-name=ev-both-on-full
#SBATCH --output=ev-both-on-full-%j.out
#SBATCH --error=ev-both-on-full-%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6
#SBATCH --gpus-per-node=2
#SBATCH --time=4:00:00
#SBATCH --mem-per-cpu=8192

module load stack/2024-06
module load  gcc/12.2.0
module load python_cuda/3.11.6

python Eval.py
# python TestCNO_ALL.py
