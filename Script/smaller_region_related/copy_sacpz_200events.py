"""
copy sacpz files for 200 events.
"""
from os.path import join, basename
from glob import glob
import subprocess

output_dir = "/scratch/05880/tg851791/process_data/sac_raw_all_smallregion"
source_dir = "/scratch/05880/tg851791/pazs_EARA/pazs_EARA2014"

# get all fnames
all_paths = glob(join(source_dir, "*"))
all_gcmtids = [basename(item) for item in all_paths]

# copy files for each gcmtid
for gcmtid in all_gcmtids:
    command = f"cp {source_dir}/{gcmtid}/* {output_dir}/{gcmtid}/SACPZ"
    subprocess.call(command, shell=True)
