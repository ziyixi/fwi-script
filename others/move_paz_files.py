"""
Move all paz files into one file
"""
import subprocess
from glob import glob
from os.path import join

working_dir = "/mnt/research/seismolab2/japan_slab/data/raw_EARA2014"
output_dir = "/mnt/research/seismolab2/japan_slab/data/pazs_EARA2014"

all_pazs = sorted(glob(join(working_dir, "*", "PZ")))

counter = 0
for item in all_pazs:
    gcmtid = item.split("/")[-2]
    out_path = join(output_dir, gcmtid)
    command = f"cp -r {item} {out_path}"
    subprocess.call(command, shell=True)
    counter += 1
    print(counter, item)
