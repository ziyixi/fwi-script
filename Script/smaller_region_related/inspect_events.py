"""
see if the events list Dr. Chen sent are in my events' list
"""
import numpy as np
from glob import glob
from os.path import join, basename

psmeca_data = np.loadtxt("./psmeca_gcmts_Japan_Slab", dtype=np.str)
events_set_psmeca = set()
for item in psmeca_data[:, -1]:
    events_set_psmeca.add(item)

cmt_files = glob(
    join("/Users/ziyixi/work/seismic-code/fwi-script/visualize/data/cmts", "*"))
cmt_fnames = [basename(item) for item in cmt_files]
cmt_fnames = set(cmt_fnames)

print(events_set_psmeca-cmt_fnames)
