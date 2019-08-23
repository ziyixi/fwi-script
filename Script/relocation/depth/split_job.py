"""
split the big job into smaller jobs.
"""
from os.path import join, basename
from glob import glob
import subprocess
import numpy as np

base_dir = "/work/05880/tg851791/stampede2/japan_slab/relocation/depth_simulation/work/work"
splited_works_dir = "/work/05880/tg851791/stampede2/japan_slab/relocation/depth_simulation/work/splited_works"

# get all events
all_events_path = glob(join(base_dir, "*"))
splited_events_paths = np.array_split(all_events_path, 5)

for index in range(len(splited_events_paths)):
    # mkdir
    thepath = join(splited_works_dir, f"work{index}")
    command = f"mkdir -p {thepath}"
    subprocess.call(command, shell=True)

    # ln events
    splited_events_path_this_index = splited_events_paths[index]
    for item in splited_events_path_this_index:
        thebasename = basename(item)
        new_path = join(thepath, thebasename)
        command = f"ln -s {item} {new_path}"
        subprocess.call(command, shell=True)
