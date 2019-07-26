import numpy as np
from glob import glob
from os.path import join

cmts_dir = "/Users/ziyixi/work/seismic-code/fwi-scripts/visualize/data/cmts"


def main():
    events_info = np.loadtxt("./events.txt", dtype=str)
    cmtids = events_info[:, 0]
    cmt_paths = glob(join(cmts_dir, "*"))
    for item in cmt_paths:
        fname = item.split("/")[-1]
        if(not (fname in cmtids)):
            print(fname)


if __name__ == "__main__":
    main()
