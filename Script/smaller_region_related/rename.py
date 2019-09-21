"""
Rename all the sac files.
"""
from glob import glob
from os.path import join, basename, isfile
import subprocess
import multiprocessing
import os
import tqdm

basename = "/scratch/05880/tg851791/process_data/sac_raw_all_smallregion"


def modify_one_dir(dir_path):
    # files = [basename(file) for file in os.listdir(dir_path)
    #          if os.path.isfile(os.path.join(dir_path, file))]
    files = []
    newfiles = []
    for file in os.listdir(dir_path):
        if(isfile(join(dir_path, file))):
            files.append(file)
            net, sta, _, comp = file.split(".")
            newfiles.append(".".join([net, sta, comp]))
    # newfiles = [".".join([item[0], item[1], item[-1]]) for item in files]
    for of, nf in zip(files, newfiles):
        opath = join(dir_path, of)
        npath = join(dir_path, nf)
        command = f"mv {opath} {npath}"
        subprocess.call(command, shell=True)


if __name__ == "__main__":
    # get all the dir paths
    dir_paths = glob(join(basename, "*"))
    with multiprocessing.Pool(processes=48) as pool:
        r = list(tqdm.tqdm(pool.imap(modify_one_dir,
                                     dir_paths), total=len(dir_paths)))
