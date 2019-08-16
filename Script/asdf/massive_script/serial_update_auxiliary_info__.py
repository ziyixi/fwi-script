"""
Update the auxiliary info for all the data asdf files in one directory.
"""
import subprocess
import tempfile
from glob import glob
from os.path import join
import click
import tqdm
# from multiprocessing import Pool

PY = "/work/05880/tg851791/stampede2/anaconda3/envs/asdf/bin/python"


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
    command = f"mpirun -np 48 {PY} ../process/write_auxiliary_info2file.py --obs_path {thefile} --ref_path {ref_file} --pkl_path {file_path}"
    subprocess.call(command, shell=True)
    return file_path


def read_single(pkl_file, ref_file, thefile):
    command = f"{PY} ../process/update_auxiliary_from_file.py --obs_path {thefile}  --pkl_path {pkl_file}"
    subprocess.call(command, shell=True)


# def kernel(each_file):
#     ref_file = each_file
#     pkl_file = write_single(each_file, ref_file)
#     read_single(pkl_file, ref_file, each_file)


@click.command()
@click.option('--main_dir', required=True, type=str, help="the directory storing all simplified data asdf file")
def main(main_dir):
    all_files = get_all_files(main_dir)
    ref_file = get_ref_file(all_files)
    for each_file in tqdm.tqdm(all_files):
        ref_file = each_file
        pkl_file = write_single(each_file, ref_file)
        read_single(pkl_file, ref_file, each_file)

    # with Pool(36) as p:
        # r = list(tqdm.tqdm(p.imap(kernel, all_files), total=len(all_files)))


if __name__ == "__main__":
    main()
