import glob
import json
from os.path import join, basename

basedir = "/scratch/05880/tg851791/relocation/work/misfit_json"
allfiles = glob(join(basedir, "*json"))
for item in tqdm.tqdm(allfiles):
    try:
        f = open(item, "r")
        data = json.laod(f)
    except:
        print(basename(item))
