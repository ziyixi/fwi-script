import subprocess
from glob import glob
from os.path import join, basename

cea_dir = "/mnt/research/seismolab2/japan_slab/data/data_cea_used"
fnet_dir = "/mnt/research/seismolab2/japan_slab/data/data_fnet"
fdsn_dir = "/mnt/research/seismolab2/japan_slab/data/data_fdsn/data"
all_dir = "/mnt/research/seismolab2/japan_slab/data/data_all_284"

cea_files = glob(join(cea_dir, "*"))
cea_files = [basename(item) for item in cea_files]

for item in cea_files:
    # ln cea
    command = f"mkdir {join(all_dir,item)}"
    subprocess.call(command, shell=True)
    command = f"ln -s {join(cea_dir,item,'*')} {join(all_dir,item)} "
    subprocess.call(command, shell=True)
    # ln fnet
    command = f"ln -s {join(fnet_dir,item,'*')} {join(all_dir,item)} "
    subprocess.call(command, shell=True)
    # ln fdsn
    fdsn_path = join(fdsn_dir, f"{item}*seed")
    command = f"ln -s {fdsn_path} {join(all_dir,item)} "
    subprocess.call(command, shell=True)
