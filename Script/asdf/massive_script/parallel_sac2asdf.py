"""
convert sac files (different directories) to asdf files in parallel
"""
from glob import glob
import click
from os.path import join, basename
from sac2pdf import add_to_adsf_file
import multiprocessing
import tqdm
from functools import partial


def kernel(gcmtid, tag, working_dir, output_dir):
    filename = join(output_dir, f"raw_{gcmtid}.h5")
    folder = join(working_dir, gcmtid)
    add_to_asdf_file(filename=filename, folder=folder, tag=tag, verbose=False)


@click.command()
@click.option('--working_dir', required=True, type=str)
@click.option('--output_dir', required=True, type=str)
def main(working_dir, output_dir):
    all_dirs = glob(join(working_dir, "*"))
    all_gcmtid = [basename(item) for item in all_dirs]
    with multiprocessing.Pool(processes=36) as pool:
        r = list(tqdm.tqdm(pool.imap(partial(kernel, tag="raw",
                                             working_dir=working_dir, output_dir=output_dir), all_gcmtid), total=len(all_gcmtid)))


if __name__ == "__main__":
    main()
