import argparse
import os
import sys
from pathlib import Path


SLURM_COMMAND = """#!/usr/bin/env bash
#SBATCH --array=0-{0}%10
#SBATCH --mem=125000
#SBATCH --cpus-per-task=8
#SBATCH -e errors.txt
#SBATCH -o out.txt
#SBATCH --time=0-10:00:00

source ~/.bashrc
conda activate venv_timelapse

exec python timelapse_zarr_to_h5.py $SLURM_ARRAY_TASK_ID {1} -o {2} 
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fld", type=str)
    parser.add_argument("-o", "--out_fld", type=str)
    args = parser.parse_args()

    fns = list(Path(args.fld).glob('*.zarr'))
    n = len(fns)

    command = SLURM_COMMAND.format(n - 1, " ".join(args.fld), args.out_fld)
    
    print(command)
    with open("temp.sh", "w") as f:
        f.write(command)
    os.system("sbatch temp.sh")
    os.unlink("temp.sh")


if __name__ == "__main__":
    main()