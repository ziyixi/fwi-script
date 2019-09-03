"""
massively get misfit json files.
"""
from glob import glob
from os.path import join, basename
from slurmpy import Slurm
import collections

# some settings
N_total = 2730  # 2340
N_each = 20
N_iter = 137  # 117
nproc = 24

PY = "/work/05880/tg851791/stampede2/anaconda3/envs/asdf/bin/python"
data_dir = "/scratch/05880/tg851791/process_data/all_484_processed_simplified"
sync_dir = "/scratch/05880/tg851791/relocation/work/asdf_processed_new"
log_file = "/scratch/05880/tg851791/relocation/work/misfit.log"
json_dir = "/scratch/05880/tg851791/relocation/work/misfit_json"

# a tuple about the paired asdf files
Pair = collections.namedtuple('Pair', 'data sync maxp minp jsonb jsons')


def extract_info():
    data_files = glob(join(data_dir, "*h5"))
    data_files = [basename(item) for item in data_files]
    sync_files = glob(join(sync_dir, "*h5"))
    sync_files = [basename(item) for item in sync_files]
    # we assume for each file in sync_dir, we can find a file in data_dir.
    result_list = []
    for sync_file_item in sync_files:
        event_flag, process_flag, _ = sync_file_item.split(".")
        _, gcmtid, depth, _ = event_flag.split("_")
        _, minp, _, maxp = process_flag.split("_")
        minp = int(minp[:-1])
        maxp = int(maxp[:-1])
        data_file_item = f"raw_{gcmtid}.{process_flag}.h5"
        jsonb_file_item = f"{gcmtid}.{depth}.{process_flag}.body.json"
        jsons_file_item = f"{gcmtid}.{depth}.{process_flag}.surf.json"
        result_list.append(
            Pair(join(data_dir, data_file_item), join(sync_dir, sync_file_item), maxp, minp, join(json_dir, jsonb_file_item), join(json_dir, jsons_file_item)))
    return result_list


def get_scripts(run_pairs):
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
            thepair = run_pairs[ievent]
            inc = ieach*nproc
            # some flags
            obs_path = thepair.data
            syn_path = thepair.sync
            max_period = thepair.maxp
            min_period = thepair.minp
            jsonfileb = thepair.jsonb
            jsonfiles = thepair.jsons

            result += f"ibrun -n {nproc} -o {inc} {PY} ./get_misfit2json.py --obs_path {obs_path} --syn_path {syn_path} --max_period {max_period} --min_period {min_period} --status body --logfile {log_file} --jsonfile {jsonfileb} &"
        result += f"wait; "
        for ieach in range(N_each):
            # run N_node files at the same iter
            ievent = iiter*N_each+ieach
            if(ievent >= N_total):
                continue
            thepair = run_pairs[ievent]
            inc = ieach*nproc
            # some flags
            obs_path = thepair.data
            syn_path = thepair.sync
            max_period = thepair.maxp
            min_period = thepair.minp
            jsonfileb = thepair.jsonb
            jsonfiles = thepair.jsons

            result += f"ibrun -n {nproc} -o {inc} {PY} ./get_misfit2json.py --obs_path {obs_path} --syn_path {syn_path} --max_period {max_period} --min_period {min_period} --status surf --logfile {log_file} --jsonfile {jsonfiles} &"
        result += f"wait; "

        result += f"echo 'end iteration {iiter}'; "

    return result


def submit_job(thecommand):
    s = Slurm("process", {"nodes": 10, "ntasks": 480,
                          "partition": 'skx-normal', "time": "06:00:00", "account": "TG-EAR130011"})
    s.run(thecommand)


if __name__ == "__main__":
    run_pairs = extract_info()
    thecommand = get_scripts(run_pairs)
    submit_job(thecommand)
