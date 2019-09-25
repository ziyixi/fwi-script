"""
tar all the directories in a directory
"""
from os.path import join, basename
from glob import glob
import subprocess
import tqdm
import multiprocessing
import click
from functools import partial


def tar_onefile(fpath, output_dir):
    thebase = basename(fpath)
    tarpath = join(output_dir, f"{thebase}.tar.gz")
    command = f"tar -czf {tarpath} {fpath}"
    subprocess.call(command, shell=True)


@click.command()
@click.option('--base_dir', required=True, type=str)
@click.option('--output_dir', required=True, type=str)
def main(base_dir, output_dir):
    all_fpath = glob(join(base_dir, "*"))
    with multiprocessing.Pool(processes=48) as pool:
        r = list(tqdm.tqdm(pool.imap(
            partial(tar_onefile, output_dir=output_dir), all_fpath), total=len(all_fpath)))


if __name__ == "__main__":
    main()
