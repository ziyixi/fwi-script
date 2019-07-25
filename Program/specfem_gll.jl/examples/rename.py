import sh
from glob import glob
from os.path import join
import tqdm
import click

@click.command()
@click.option('--baseurl', required=True, help="the working directory", type=str)
def main(baseurl):
    raw_files = glob(join(baseurl, "*"))
    for eachfile in tqdm.tqdm(raw_files):
        fname = eachfile.split("/")[-1]
        fbody = "/".join(eachfile.split("/")[:-1])
        newfname = join(fbody, ".".join(fname.split(".")[:-1]))
        sh.mv(eachfile, newfname)
if __name__ == "__main__":
    main()