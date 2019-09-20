from glob import glob
from os.path import join, basename

basedir = "/scratch/05880/tg851791/process_data/sac_raw_all_smallregion"

for fpath in sorted(glob(join(basedir, "*"))):
    sacpzpath = join(fpath, "SACPZ", "*")
    value = False
    for item in sorted(glob(sacpzpath)):
        if("BHZ" in item):
            value = True
    if(not value):
        print(basename(fpath))
