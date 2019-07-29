from glob import glob
from os.path import join, basename

from slurmpy import Slurm

# some resources information
N_cores = 200
N_node = 10
N_cores_each_node = 20

# the base sync directory storing asdf files
N_files = 810
N_iters = 81

# some configuration
PY = "/mnt/home/xiziyi/anaconda3/envs/seismology/bin/python"
OBS_DIR = "/mnt/ls15/scratch/users/xiziyi/process_asdf/validation/processed_simple"
SYN_DIR = "/mnt/ls15/scratch/users/xiziyi/process_asdf/relocation/processed"
OUTPUT_DIR = "/mnt/ls15/scratch/users/xiziyi/process_asdf/windows_nonode"
logfile = "/mnt/ls15/scratch/users/xiziyi/process_asdf/windows_nonode.log"
min_periods = "10,20,40"
max_periods = "120,120,120"
depths = "-16,-12,-8,-4,0,4,8,12,16"


def get_pairs(gcmtid, min_period, max_period, depth):
    obs_fname = f"raw_{gcmtid}.preprocessed_{min_period}s_to_{max_period}s.h5"
    syn_fname = f"sync_{gcmtid}_d{depth}.preprocessed_{min_period}s_to_{max_period}s.h5"
    output_fname = f"{gcmtid}.{min_period}s.{max_period}s.d{depth}.pkl"
    obs_path = join(OBS_DIR, obs_fname)
    syn_path = join(SYN_DIR, syn_fname)
    out_path = join(OUTPUT_DIR, output_fname)
    return obs_path, syn_path, out_path


def get_gcmtids():
    allfiles = glob(join(OBS_DIR, "*h5"))
    allfiles = [basename(item) for item in allfiles]
    gcmtid_set = set()
    for item in allfiles:
        thekey = item.split("_")[1].split(".")[0]
        gcmtid_set.add(thekey)
    return sorted(gcmtid_set)


def get_runfile_pairs():
    result = {}
    depth_items = depths.split(",")
    min_period_items = min_periods.split(",")
    max_period_items = max_periods.split(",")
    gcmtids = get_gcmtids()
    keys = {}
    for min_period, max_period in zip(min_period_items, max_period_items):
        for depth in depth_items:
            for gcmtid in gcmtids:
                thekey = (gcmtid, depth, min_period, max_period)
                pairs = get_pairs(gcmtid, min_period, max_period, depth)
                result[thekey] = pairs
    return result


def get_scripts():
    runfile_pairs = get_runfile_pairs()
    runfile_keys = list(runfile_pairs.keys())
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
            thekey = runfile_keys[offset]
            obs_path, syn_path, out_path = runfile_pairs[thekey]
            result += f"srun -N1-20 -n {N_cores_each_node} {PY} ../get_info/get_flexwin_windows.py --obs_path {obs_path} --syn_path {syn_path} --out_path {out_path} --logfile {logfile} &"
        result += f"wait; "
        result += f"echo 'end iteration {iiter}'; "
    return result


def submit_job(thecommand):
    s = Slurm("flexwin", {"ntasks": N_cores,
                          "time": "06:00:00", "cpus-per-task": 1, "mem-per-cpu": "2G"})
    s.run(thecommand)


if __name__ == "__main__":
    thecommand = get_scripts()
    submit_job(thecommand)
