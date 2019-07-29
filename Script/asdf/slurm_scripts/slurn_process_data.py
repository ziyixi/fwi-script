import sys
from glob import glob
from os.path import join

from slurmpy import Slurm

# some resources information
N_cores = 300
N_node = 15
N_cores_each_node = 20

# the base sync directory storing asdf files
N_files = 30
N_iters = 2

# some configuration
PY = "/mnt/home/xiziyi/anaconda3/envs/seismology/bin/python"
min_periods = "10,20,40"
max_periods = "120,120,120"
waveform_length = 2340
sampling_rate = 10
logfile = "/mnt/ls15/scratch/users/xiziyi/process_asdf/validation/process_data.log"
RAW_DIR = "/mnt/ls15/scratch/users/xiziyi/process_asdf/validation/asdf_for_validation"
PROCESSED_DIR = "/mnt/ls15/scratch/users/xiziyi/process_asdf/validation/processed"
SIMPLED_DIR = "/mnt/ls15/scratch/users/xiziyi/process_asdf/validation/processed_simple"
cea_correction_file = "../data/cmpaz_segment.txt"


def get_files(base_dir):
    return glob(join(base_dir, "*h5"))


def get_scripts(run_files):
    result = ""
    result += "module purge;"
    result += "module load GCC/8.2.0-2.31.1;"
    result += "module load OpenMPI/3.1.3;"
    # run iters
    for iiter in range(N_iters):
        result += f"echo 'start iteration {iiter}'; "
        for ieach in range(N_node):
            # run N_node files at the same iter
            offset = iiter*N_node+ieach
            if(offset >= N_files):
                continue
            filename = run_files[offset]
            result += f"srun -N 1 -n {N_cores_each_node} {PY} ../process/process_data.py --min_periods {min_periods} --max_periods {max_periods} --asdf_filename {filename} --waveform_length {waveform_length} --sampling_rate {sampling_rate} --output_directory {PROCESSED_DIR} --logfile {logfile} --correct_cea --cea_correction_file {cea_correction_file} &"
        result += f"wait; "
        result += f"echo 'end iteration {iiter}'; "

    return result


def submit_job(thecommand):
    s = Slurm("process_data", {"nodes": N_node, "ntasks": N_cores,
                               "time": "04:00:00", "cpus-per-task": 1, "mem-per-cpu": "4G"})
    s.run(thecommand)


if __name__ == "__main__":
    run_files = get_files(RAW_DIR)
    thecommand = get_scripts(run_files)
    submit_job(thecommand)
