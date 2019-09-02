import sys
from glob import glob
from os.path import join

from slurmpy import Slurm

# some resources information
N_total = 8
N_each = 4
N_iter = 2
nproc = 24

# some configuration
PY = "/work/05880/tg851791/stampede2/anaconda3/envs/asdf/bin/python"
min_periods = "10,20,40"
max_periods = "120,120,120"
waveform_length = 2340
sampling_rate = 10
logfile = "/scratch/05880/tg851791/relocation/work/process_sync_test.log"
RAW_DIR = "/scratch/05880/tg851791/relocation/work/asdf_test"
PROCESSED_DIR = "/scratch/05880/tg851791/relocation/work/asdf_processed_test"


def get_files(base_dir):
    return sorted(glob(join(base_dir, "*h5")))


def get_scripts(run_files):
    result = ""
    result += "module remove python2/2.7.15; "
    result += "module load mvapich2/2.3.1; "
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
            result += f"ibrun -n {nproc} -o {inc} {PY} ../process/process_sync.py --min_periods {min_periods} --max_periods {max_periods} --asdf_filename {filename} --waveform_length {waveform_length} --sampling_rate {sampling_rate} --output_directory {PROCESSED_DIR} --logfile {logfile} &"
        result += f"wait; "
        result += f"echo 'end iteration {iiter}'; "

    return result


def submit_job(thecommand):
    # s = Slurm("process_data", {"nodes": N_node, "ntasks": N_cores,
    #                            "time": "12:00:00", "cpus-per-task": 1, "mem-per-cpu": "4G"})
    s = Slurm("process", {"nodes": 2, "ntasks": 96,
                          "partition": 'skx-normal', "time": "01:00:00", "account": "TG-EAR140030"})
    s.run(thecommand)


if __name__ == "__main__":
    run_files = get_files(RAW_DIR)
    thecommand = get_scripts(run_files)
    submit_job(thecommand)
