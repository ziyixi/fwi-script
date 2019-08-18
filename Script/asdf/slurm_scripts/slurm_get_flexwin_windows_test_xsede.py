from glob import glob
from os.path import join, basename
from slurmpy import Slurm

# some resources configuration
N_files = 8
N_nodes = 2
N_tasks = 96
N_each = 4
N_iter = 2
nproc = 24
TIME = "01:00:00"

# some paths
sync_dir = "/scratch/05880/tg851791/process_sync/1run_before_relocation_processed_test"
data_dir = "/scratch/05880/tg851791/process_data/data_processed_simplified_all_test"
PY = "/work/05880/tg851791/stampede2/anaconda3/envs/asdf/bin/python"
output_dir = "/scratch/05880/tg851791/process_windows/windows_0818_test"
log_file = "/scratch/05880/tg851791/process_windows/windows_0818.test.log"


def search_pairs(data_files, sync_files):
    # * should be the basename
    # for data
    data_key = set()
    for item in data_files:
        dot_spliter = item.split(".")
        gcmtid = dot_spliter[0].split("_")[1]
        process_flag = dot_spliter[1]
        data_key.add((gcmtid, process_flag))

    # for sync
    sync_key = set()
    for item in sync_files:
        dot_spliter = item.split(".")
        gcmtid = dot_spliter[0].split("_")[1]
        process_flag = dot_spliter[1]
        sync_key.add((gcmtid, process_flag))

    common_key = data_key & sync_key
    # get pairs according to common_key
    result = []
    for item in common_key:
        gcmtid = item[0]
        process_flag = item[1]
        sync_name = f"sync_{gcmtid}_raw.{process_flag}.h5"
        sync_path = join(sync_dir, sync_name)
        data_name = f"raw_{gcmtid}.{process_flag}.h5"
        data_path = join(data_dir, data_name)
        out_name = f"{gcmtid}.{process_flag}.pkl"
        out_path = join(output_dir, out_name)
        result.append((data_path, sync_path, out_path))

    return sorted(result)


def get_scripts(run_pairs):
    result = ""
    result += "date; "
    result += "module remove python2/2.7.15; "
    result += "module load mvapich2/2.3.1; "
    # run iters
    for iiter in range(N_iter):
        result += f"echo 'start iteration {iiter}'; "
        for ieach in range(N_each):
            # run N_node files at the same iter
            ievent = iiter*N_each+ieach
            if(ievent >= N_files):
                continue
            data_path, sync_path, out_path = run_pairs[ievent]
            inc = ieach*nproc
            result += f"ibrun -n {nproc} -o {inc} {PY} ../get_info/get_flexwin_windows.py --obs_path {data_path} --syn_path {sync_path} --out_path {out_path} --logfile {log_file} &"
        result += f"wait; "
        result += f"echo 'end iteration {iiter}'; "
    result += "date; "

    return result


def submit_job(thecommand):
    s = Slurm("flexwin", {"nodes": N_nodes, "ntasks": N_tasks,
                          "partition": 'skx-normal', "time": TIME, "account": "TG-EAR140030"})
    s.run(thecommand)


def main():
    data_files = [basename(item) for item in glob(join(data_dir, "*h5"))]
    sync_files = [basename(item) for item in glob(join(sync_dir, "*h5"))]
    run_pairs = search_pairs(data_files, sync_files)
    thecommand = get_scripts(run_pairs)
    submit_job(thecommand)


if __name__ == "__main__":
    main()
