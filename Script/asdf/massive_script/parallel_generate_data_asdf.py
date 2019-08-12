import multiprocessing
import tqdm
from glob import glob
from os.path import join, basename
from seed2asdf import generate_asdf_for_single_event
from functools import partial


def kernel(gcmtid, seed_dir, cmt_dir, output_dir, logfile):
    seed_directory = join(seed_dir, gcmtid)
    cmt_path = join(cmt_dir, gcmtid)
    output_path = join(output_dir, f"raw_{gcmtid}.h5")
    generate_asdf_for_single_event(
        seed_directory, cmt_path, output_path, True, logfile)


@click.command()
@click.option('--seed_dir', required=True, type=str)
@click.option('--cmt_dir', required=True, type=str)
@click.option('--output_dir', required=True, type=str)
@click.option('--logfile', required=True, type=str)
def main(seed_dir, cmt_dir, output_dir, logfile):
    all_dirs = glob(join(seed_dir, "*"))
    all_cmtids = [basename(item) for item in all_dirs]
    with multiprocessing.Pool(processes=36) as pool:
        r = list(tqdm.tqdm(pool.imap(partial(kernel, seed_dir=seed_dir, cmt_dir=cmt_dir,
                                             output_dir=output_dir, logfile=logfile), all_cmtids), total=len(all_cmtids)))


if __name__ == "__main__":
    main()
