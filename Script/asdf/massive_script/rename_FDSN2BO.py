"""
change network names in sync asdf file. FNET->BO
"""
import pyasdf
import obspy
import click


def kernel_rename(asdf_file):
    # ds = pyasdf.ASDFDataSet(asdf_file)
    with pyasdf.ASDFDataSet(asdf_file) as ds:
        station_list = ds.waveforms.list()
        event = ds.events[0]

        for id in station_list:
            network, station = id.split(".")
            if(network == "FNET"):
                waves = ds.waveforms[id].sync
                del ds.waveforms[id]
                for wave in waves:
                    wave.stats.network = "BO"
                ds.add_waveforms(waves, tag="sync", event_id=event)


@click.command()
@click.option('--asdf_file', required=True, type=str, help="asdf file path")
def main(asdf_file):
    kernel_rename(asdf_file)


if __name__ == "__main__":
    main()
