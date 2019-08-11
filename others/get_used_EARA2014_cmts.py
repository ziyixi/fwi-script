from glob import glob
from os.path import join, basenmame
import subprocess

alldir = "/mnt/research/seismolab2/japan_slab/cmts/Japan_slab"
newdir = "/mnt/research/seismolab2/japan_slab/cmts/Japan_slab_from_used_EARA2014"
downloadeddir = "/mnt/research/seismolab2/japan_slab/data/data_fnet"

downloaded = glob(join(downloadeddir, "*"))
downloaded = [basenmame(item) for item in downloaded]
theall = glob(join(alldir, "*"))
theall = [basenmame(item) for item in theall]

tocp = sorted(set(theall)-set(downloaded))
for item in tocp:
    command = f"cp {join(alldir,item)} {join(newdir,item)}"
    subprocess.call(command, shell=True)
