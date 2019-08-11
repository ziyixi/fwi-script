import multiprocessing
from os.path import join
from glob import glob
from rename_FDSN2BO import kernel_rename
import tqdm
import click


def kernel(asdf_file):
    kernel_rename(asdf_file)


@click.command()
@click.option('--basedir', required=True, type=str)
def main(basedir):
    all_dirs = glob(join(basedir, "*h5"))
    with multiprocessing.Pool(processes=36) as pool:
        r = list(tqdm.tqdm(pool.imap(kernel, all_dirs), total=len(all_dirs)))


if __name__ == "__main__":
    main()
