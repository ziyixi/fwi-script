"""
copy sacpz files for 200 events.
"""
from os.path import join, basename
from glob import glob
import subprocess
import multiprocessing
import tqdm

output_dir = "/scratch/05880/tg851791/process_data/sac_raw_all_smallregion"
source_dir = "/scratch/05880/tg851791/pazs_EARA/pazs_EARA2014"

# get all fnames
all_paths = glob(join(source_dir, "*"))
all_gcmtids = [basename(item) for item in all_paths]

# copy files for each gcmtid


def kernel(gcmtid):
    command = f"cp {source_dir}/{gcmtid}/* {output_dir}/{gcmtid}/SACPZ"
    subprocess.call(command, shell=True)


with multiprocessing.Pool(processes=48) as pool:
    r = list(tqdm.tqdm(pool.imap(kernel, all_gcmtids), total=len(all_gcmtids)))
