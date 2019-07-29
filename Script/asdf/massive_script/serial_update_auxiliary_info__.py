"""
Update the auxiliary info for all the data asdf files in one directory.
"""
import subprocess
import tempfile
from glob import glob
from os.path import join
import click
import tqdm


PY = "/mnt/home/xiziyi/anaconda3/envs/seismology/bin/python"


def get_all_files(main_dir):
    return sorted(glob(join(main_dir, "*h5")))


def get_ref_file(all_files):
    return all_files[0]


def write_single(thefile, ref_file):
    # create a temp file to store pkl info.
    file_obj = tempfile.NamedTemporaryFile(delete=False)
    file_obj.close()
    file_path = file_obj.name
    # calculate the pkl info.
    command = f"{PY} ../process/write_auxiliary_info2file.py --obs_path {thefile} --ref_path {ref_file} --pkl_path {file_path}"
    subprocess.call(command, shell=True)
    return file_path


def read_single(pkl_file, ref_file, thefile):
    command = f"{PY} ../process/update_auxiliary_from_file.py --obs_path {thefile}  --pkl_path {pkl_file}"
    subprocess.call(command, shell=True)


@click.command()
@click.option('--main_dir', required=True, type=str, help="the directory storing all simplified data asdf file")
def main(main_dir):
    all_files = get_all_files(main_dir)
    ref_file = get_ref_file(all_files)
    for each_file in tqdm.tqdm(all_files):
        pkl_file = write_single(each_file, ref_file)
        read_single(pkl_file, ref_file, each_file)


if __name__ == "__main__":
    main()
