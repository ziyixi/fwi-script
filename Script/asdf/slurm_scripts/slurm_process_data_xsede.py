import sys
from glob import glob
from os.path import join

from slurmpy import Slurm

# some resources information
N_total = 284
N_each = 20
N_iter = 15
nproc = 24

# some configuration
PY = "/work/05880/tg851791/stampede2/anaconda3/envs/asdf/bin/python"
min_periods = "10,20,40"
max_periods = "120,120,120"
waveform_length = 2340
sampling_rate = 10
logfile = "/scratch/05880/tg851791/process_data/process_data_284.log"
RAW_DIR = "/scratch/05880/tg851791/process_data/asdf_all_284"
PROCESSED_DIR = "/scratch/05880/tg851791/process_data/all_284_processed"
cea_correction_file = "../data/cmpaz_segment.txt"


def get_files(base_dir):
    return sorted(glob(join(base_dir, "*h5")))


def get_scripts(run_files):
    result = ""
    result += "module remove python2/2.7.15; "
    result += "module load mvapich2/2.3.1"
    # run iters
    for iiter in range(N_iter):
        result += f"echo 'start iteration {iiter}'; "
        for ieach in range(N_each):
            # run N_node files at the same iter
            ievent = iiter*N_each+ieach
            if(ievent >= N_total):
                continue
            filename = run_files[ievent]
            inc = ieach*nproc
            result += f"ibrun -n {nproc} -o {inc} {PY} ../process/process_data.py --min_periods {min_periods} --max_periods {max_periods} --asdf_filename {filename} --waveform_length {waveform_length} --sampling_rate {sampling_rate} --output_directory {PROCESSED_DIR} --logfile {logfile} --correct_cea --cea_correction_file {cea_correction_file} &"
        result += f"wait; "
        result += f"echo 'end iteration {iiter}'; "

    return result


def submit_job(thecommand):
    # s = Slurm("process_data", {"nodes": N_node, "ntasks": N_cores,
    #                            "time": "12:00:00", "cpus-per-task": 1, "mem-per-cpu": "4G"})
    s = Slurm("process", {"nodes": 10, "ntasks": 480,
                          "partition": 'skx-normal', "time": "12:00:00", "account": "TG-EAR140030"})
    s.run(thecommand)


if __name__ == "__main__":
    run_files = get_files(RAW_DIR)
    thecommand = get_scripts(run_files)
    submit_job(thecommand)
