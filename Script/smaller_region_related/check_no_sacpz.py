"""
Check if there is the condition that we have sac files but not sacpz files.
"""
import numpy as np
from glob import glob
from os.path import join, basename

basedir = "/scratch/05880/tg851791/process_data/sac_raw_all_smallregion"

events_200 = sorted(set(np.loadtxt("./from200.txt", dtype=np.str)))
events_284 = sorted(set(np.loadtxt("./from284.txt", dtype=np.str)))

# test 200 events
for gcmtid in events_200:
    fpath = join(basedir, gcmtid)
    allsac = glob(join(fpath, "*"))
    allsac = set([basename(item)
                  for item in allsac if basename(item) != "SACPZ"])
    allpz = glob(join(fpath, "SACPZ", "*"))
    allpz = set([basename(item) for item in allpz])

    only_sac = allsac-allpz
    only_pz = allpz-allsac
    print(gcmtid, only_sac, only_pz)

# test 284 events
for gcmtid in events_284:
    fpath = join(basedir, gcmtid)
    allsac_raw = glob(join(fpath, "*"))
    allsac = set()
    for item in allsac_raw:
        fname = basename(item)
        if(fname != "SACPZ"):
            net, sta, _ = fname.split(".")
            allsac.add(".".join([net, sta]))
    allpz = glob(join(fpath, "SACPZ", "*"))
    allpz = set([basename(item) for item in allpz])

    only_sac = allsac-allpz
    only_pz = allpz-allsac
    print(gcmtid, only_sac, only_pz)
