"""
copy cmt solution files for the small region
"""
from glob import glob
from os.path import join, basename
import subprocess
import numpy as np

basedir = "/mnt/research/seismolab2/japan_slab/cmts/Japan_slab"
target = "/mnt/research/seismolab2/japan_slab/cmts/small_region"

# get all gcmt ids
psmeca_data = np.loadtxt("./psmeca_gcmts_Japan_Slab", dtype=np.str)
gcmt_ids = set(psmeca_data[:, -1])
for item in sorted(gcmt_ids):
    command = f"cp {join(basedir,item)} {join(target,item)}"
    subprocess.call(command, shell=True)
