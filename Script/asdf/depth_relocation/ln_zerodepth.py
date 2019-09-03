"""
link zero depth asdf files to the relocation sync directory.
"""

from glob import glob
from os.path import join, basename
import subprocess

zero_sync_dir = "/scratch/05880/tg851791/process_sync/1run_before_relocation_processed"
relocation_dir = "/scratch/05880/tg851791/relocation/work/asdf_processed_new"


def get_keys():
    """
    get all used gcmtids
    """
    relocation_files = glob(join(relocation_dir, "*h5"))
    relocation_files = [basename(item) for item in relocation_files]
    gcmtid_set = set()
    for item in relocation_files:
        gcmtid = item.split(".")[0].split("_")[1]
        gcmtid_set.add(gcmtid)
    gcmtid_list = sorted(gcmtid_set)
    return gcmtid_list


def ln_files(gcmtid_list):
    """
    for each key in gcmtid_list, make a soft link
    """
    for gcmtid in gcmtid_list:
        source = join(zero_sync_dir, f"*{gcmtid}*h5")
        target = None
        source_files = glob(source)
        source_files = [basename(item) for item in source_files]
        for source_file in source_files:
            _, process_flag, _ = source_file.split(".")
            target = join(relocation_dir,
                          f"sync_{gcmtid}_d0_raw.{process_flag}.h5")
            source_path = join(zero_sync_dir, source_file)
            command = f"ln -s {source_path} {target}"
            subprocess.call(command, shell=True)


if __name__ == "__main__":
    gcmtid_list = get_keys()
    ln_files(gcmtid_list)
