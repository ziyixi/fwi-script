from glob import glob
from os.path import join, basename

basedir = "/scratch/05880/tg851791/process_data/sac_raw_all_smallregion"

for fpath in sorted(glob(join(basedir, "*"))):
    sacpzpath = join(fpath, "SACPZ", "*")
    value = False
    for item in sacpzpath:
        print(item)
        if("BHZ" in item):
            value = True
    if(value):
        print(basename(fpath))
