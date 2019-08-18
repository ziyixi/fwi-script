"""
convert asdf to sac files.
"""
import pyasdf
import obspy
from os.path import join
import click


def convert_single(asdf_path, out_dir, tag):
    with pyasdf.ASDFDataSet(asdf_path, mode="r") as ds:
        for item in ds.waveforms.list():
            st = ds.waveforms[item][tag]
            for tr in st:
                id = tr.id
                out_path = join(out_dir, id)
                # update sac info
                tr.stats.sac = obspy.core.util.attribdict.AttribDict()
                tr.stats.sac["stla"] = ds.waveforms[item].StationXML[0][0].latitude
                tr.stats.sac["stlo"] = ds.waveforms[item].StationXML[0][0].longitude
                tr.write(out_path, format="SAC")


@click.command()
@click.option('--asdf_path', required=True, type=str)
@click.option('--out_dir', required=True, type=str)
@click.option('--tag', required=True, type=str)
def main(asdf_path, out_dir, tag):
    convert_single(asdf_path, out_dir, tag)


if __name__ == "__main__":
    main()
