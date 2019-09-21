from os.path import basename, join
import subprocess
from glob import glob
import tqdm

fnet_sacpz_path = "/scratch/05880/tg851791/process_data/fnet_lack_sacpz/fnet_sacpz"
output_path = "/scratch/05880/tg851791/process_data/sac_raw_all_smallregion"

all_dirs = glob(join(fnet_sacpz_path, "*"))
for each_dir in tqdm.tqdm(all_dirs):
    gcmtid = basename(each_dir)
    from_path = join(each_dir, "*")
    to_path = join(output_path, gcmtid, "SACPZ")
    command = f"cp {from_path} {to_path}"
    subprocess.call(command, shell=True)
