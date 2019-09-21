from glob import glob
from os.path import join, basename
import subprocess

base_dir = "/scratch/05880/tg851791/process_data/sac_raw_all_smallregion"

all_dirs = glob(join(base_dir, "*"))
for each_dir in all_dirs:
    gcmtid = basename(each_dir)

    command = f"mkdir -p {base_dir}/{gcmtid}/extra"
    subprocess.call(command, shell=True)
    command = f"mv {base_dir}/{gcmtid}/SACPZ {base_dir}/{gcmtid}/PZ"
    subprocess.call(command, shell=True)

    sac_files = sorted(glob(join(each_dir, "*")))
    sac_files = [basename(item) for item in sac_files]
    sac_files.remove("SACPZ")
    no3comp_num = 0
    thekey = set()
    for sac_file in sac_files:
        net, sta, comp = sac_file.split(".")
        thekey.add(".".join([net, sta]))
        # comp3_files = glob(join(each_dir, f"{net}.{sta}*"))
        # if(len(comp3_files) % 3 != 0):
        #     no3comp_num += 1
    for net_sta in sorted(thekey):
        comp3_files = glob(join(each_dir, f"{net_sta}*"))
        if(len(comp3_files) % 3 != 0):
            no3comp_num += 1
            command = f"mv {each_dir}/{net_sta}* {each_dir}/extra"
            subprocess.call(command, shell=True)
    print(gcmtid, no3comp_num)
