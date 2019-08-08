"""
generate asdf files from a relocation working directory.
"""
from functools import partial
import multiprocessing
import sys
sys.path.append("..")
from generate.sync2asdf_specfem import convert_sync_to_asdf
import numpy as np
from os.path import join
from glob import glob
import click
import tqdm

# from mpi4py import MPI
# ! no print, we have to find a way to log the process
# ! never use mpi to generate asdf files, otehrwise the file will be broken

# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()
# size = comm.Get_size()
# isroot = (rank == 0)


def kernel(each_dir, out_dir,cmt_dir):
    # print(f"start to handle {each_dir}")
    split_path = each_dir.split("/")
    event = split_path[-1]
    output_path = join(out_dir, f"sync_{event}_raw.h5")
    cmt_path=join(cmt_dir,event)
    files_in_output = glob(join(out_dir, "*"))
    if(output_path in files_in_output):
        return
    convert_sync_to_asdf(each_dir,cmt_path, output_path, True)


@click.command()
@click.option('--base_dir', required=True, type=str, help="the relocation working directory")
@click.option('--out_dir', required=True, type=str, help="the asdf output directory")
@click.option('--cmt_dir', required=True, type=str, help="the cmt files directory")
def main(base_dir, out_dir,cmt_dir):
    all_dirs = glob(join(base_dir, "*"))
    with multiprocessing.Pool(processes=48) as pool:
        r=list(pool.imap(partial(kernel, out_dir=out_dir,cmt_dir=cmt_dir), all_dirs),total=len(all_dirs))


if __name__ == "__main__":
    main()
