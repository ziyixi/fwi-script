import sys
from glob import glob
from os.path import join

from slurmpy import Slurm

# some resources information
N_cores = 40
N_node = 2
N_cores_each_node = 20

# the base sync directory storing asdf files
N_files = 2
N_iters = 1

# some configuration
PY = "/mnt/home/xiziyi/anaconda3/envs/seismology/bin/python"
min_periods = "10,20,40"
max_periods = "120,120,120"
waveform_length = 2340
sampling_rate = 10
logfile = "/mnt/ls15/scratch/users/xiziyi/process_asdf/relocation/process_sync.log"
RAW_DIR = "/mnt/ls15/scratch/users/xiziyi/process_asdf/relocation/raw_sync"
PROCESSED_DIR = "/mnt/ls15/scratch/users/xiziyi/process_asdf/relocation/processed"


def get_files(base_dir):
    return [
        "/mnt/ls15/scratch/users/xiziyi/process_asdf/relocation/raw_sync/sync_201202260617A_d-12.h5",
        "/mnt/ls15/scratch/users/xiziyi/process_asdf/relocation/raw_sync/sync_201111241025A_d-8.h5"
    ]


def get_scripts(run_files):
    result = ""
    result += "module purge;"
    result += "module load GCC/8.2.0-2.31.1;"
    result += "module load OpenMPI/3.1.3;"
    for iiter in range(N_iters):
        result += f"echo 'start iteration {iiter}'; "
        for ieach in range(N_node):
            # run N_node files at the same iter
            offset = iiter*N_node+ieach
            if(offset >= N_files):
                continue
            filename = run_files[offset]
            result += f"srun -N 1 -n {N_cores_each_node} {PY} ../process/process_sync.py --min_periods {min_periods} --max_periods {max_periods} --asdf_filename {filename} --waveform_length {waveform_length} --sampling_rate {sampling_rate} --output_directory {PROCESSED_DIR} --logfile {logfile} &"
        result += f"wait; "
        result += f"echo 'end iteration {iiter}'; "
    return result


def submit_job(thecommand):
    s = Slurm("process_sync", {"nodes": N_node, "ntasks": N_cores,
                               "time": "00:30:00", "cpus-per-task": 1, "mem-per-cpu": "2G"})
    s.run(thecommand)


if __name__ == "__main__":
    run_files = get_files(RAW_DIR)
    thecommand = get_scripts(run_files)
    submit_job(thecommand)
