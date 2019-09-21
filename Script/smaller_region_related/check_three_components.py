from glob import glob
from os.path import join, basename

base_dir = "/scratch/05880/tg851791/process_data/sac_raw_all_smallregion"

all_dirs = glob(join(base_dir, "*"))
for each_dir in all_dirs:
    gcmtid = basename(each_dir)
    sac_files = sorted(glob(join(each_dir, "*")))
    sac_files = [basename(item) for item in sac_files]
    sac_files = sac_files.remove("SACPZ")
    no3comp_num = 0
    for sac_file in sac_files:
        net, sta, comp = sac_file.split(".")
        comp3_files = glob(join(each_dir, f"{net}.{sta}*"))
        if(len(comp3_files) % 3 != 0):
            no3comp_num += 1
    print(gcmtid, no3comp_num)
