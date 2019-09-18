import subprocess
from os.path import join, basename
import numpy as np

psmeca_data = np.loadtxt("./psmeca_gcmts_Japan_Slab", dtype=np.str)
gcmtid_set = set(psmeca_data[:, -1])

source_dir1 = "/scratch/05880/tg851791/process_data/asdf_all_284"
source_dir2 = "/scratch/05880/tg851791/process_data/asdf_raw_EARA2014"
target_dir = "/scratch/05880/tg851791/process_data/asdf_raw_all_smallregion"

for gcmtid in sorted(gcmtid_set):
    # try to ln from dir1
    command = f"ln -s ../{source_dir1}/raw_{gcmtid}.h5 {target_dir}"
    try:
        subprocess.call(command, shell=True)
    except:
        pass
    # try to ln from dir2
    command = f"ln -s ../{source_dir2}/raw_{gcmtid}.h5 {target_dir}"
    try:
        subprocess.call(command, shell=True)
    except:
        pass
