from glob import glob
from os.path import join, basename

basedir = "/mnt/ls15/scratch/users/xiziyi/process_asdf/relocation/processed"


def main():
    allfiles = glob(join(basedir, "*h5"))
    allfiles = [basename(item) for item in allfiles]

    keys = set()
    for item in allfiles:
        splitter = item.split("_")
        keys.add("_".join(splitter[:2]))
    for item in keys:
        keyfiles = glob(join(basedir, item+"*"))
        if(len(keyfiles) != 27):
            print(item)


if __name__ == "__main__":
    main()
    # sync_201202260617A_d-12.h5
