from glob import glob
import json
from os.path import join, basename
import tqdm

basedir = "/scratch/05880/tg851791/relocation/work/misfit_json"
allfiles = glob(join(basedir, "*json"))
for item in tqdm.tqdm(allfiles):
    try:
        f = open(item, "r")
        data = json.load(f)
    except:
        print(basename(item))
