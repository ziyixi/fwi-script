import numpy as np
from glob import glob
import subprocess
from os.path import basename, join

basedir = "/mnt/research/seismolab2/japan_slab/data/data_all_284"
temp_dir = "/mnt/home/xiziyi/data/temp_sacpz"
output_dir = "/mnt/home/xiziyi/data/fnet_sacpz"

# get gcmtid to extract
gcmtids = np.loadtxt("./from284.txt")

# extract all sacpzs to temp_dir
for gcmtid in gcmtids:
    command = f"mkdir -p {temp_dir}/{gcmtid}"
    subprocess.call(command, shell=True)
    command = f"rdseed -pf {basedir}/{gcmtid}/{gcmtid}.SEED -q {temp_dir}/{gcmtid}"
    subprocess.call(command, shell=True)

# * rename and combine sacpzs
# get keys
station_keys = {}
for gcmtid in gcmtids:
    station_keys[gcmtid] = set()
    all_files = glob(join(temp_dir, gcmtid, "SAC_PZs_*"))
    all_files = [basename(item) for item in all_files]
    for fname in all_files:
        fname_spliter = fname.split("_")
        sta = fname_spliter[3]
        station_keys[gcmtid].add(sta)

# combine files and output to output_dir
for gcmtid in gcmtids:
    # mkdir
    command = f"mkdir -p {output_dir}/{gcmtid}"
    subprocess.call(command, shell=True)
    # combine files
    for sta in sorted(station_keys[gcmtid]):
        sta_files = glob(join(temp_dir, gcmtid, f"SAC_PZs_BO_{sta}_*"))
        with open(f"{output_dir}/{gcmtid}/BO.{sta}", "w") as outfile:
            for f in sta_files:
                with open(f, "w") as infile:
                    outfile.write(infile.read())
