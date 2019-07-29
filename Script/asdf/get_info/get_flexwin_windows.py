import pyflex
from pyasdf import ASDFDataSet
import pickle
from loguru import logger
import click
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
isroot = (rank == 0)

# ! There may be possibility that the npts for obs/syn are not the same


def get_asdf_info(ds):
    waveform_list = ds.waveforms.list()
    wg_name = waveform_list[0]
    wg = ds.waveforms[wg_name]
    data_tags = wg.get_waveform_tags()
    thetag = data_tags[0]
    thetag_splitted = thetag.split("_")
    min_period = int(thetag_splitted[1][:-1])
    max_period = int(thetag_splitted[3][:-1])
    return thetag, min_period, max_period


def build_config(min_period, max_period):
    config = pyflex.Config(
        min_period=min_period, max_period=max_period,
        stalta_waterlevel=0.11,
        tshift_acceptance_level=15.0,
        dlna_acceptance_level=2.5,
        cc_acceptance_level=0.6,
        c_0=0.7, c_1=2.0, c_2=0.0, c_3a=1.0,
        c_3b=2.0, c_4a=3.0, c_4b=10.0,
        s2n_limit=0.5,
        max_time_before_first_arrival=-50.0,
        min_surface_wave_velocity=3.5,
        window_signal_to_noise_type="energy")
    return config


def run(ds_obs, ds_syn):
    thetag_obs, min_period, max_period = get_asdf_info(ds_obs)
    thetag_syn, _, _ = get_asdf_info(ds_syn)
    config = build_config(min_period, max_period)
    event = ds_obs.events[0]

    # the kernel function
    def process(gp_obs, gp_syn):
        stationxml = gp_obs.StationXML
        observed = gp_obs[thetag_obs].copy()
        synthetic = gp_syn[thetag_syn].copy()
        all_windows = []

        for index in range(3):
            obs = observed[index]
            syn = synthetic[index]
            # there may have possibility that the npts are not equal
            if(obs.stats.npts != syn.stats.npts):
                if(obs.stats.npts < syn.stats.npts):
                    # cut according to the obs
                    syn.trim(obs.stats.starttime, obs.stats.endtime)
                else:
                    # cut according to the syn
                    obs.trim(syn.stats.starttime, syn.stats.endtime)

            # must have the same starttime
            syn.stats.starttime = obs.stats.starttime

            windows = pyflex.select_windows(
                obs, syn, config, event=event, station=stationxml)

            # log
            component = ["R", "T", "Z"][index]
            logger.info(
                f"station {stationxml[0].code}.{stationxml[0][0].code} component {component} picked {len(windows)} windows")

            if not windows:
                continue
            all_windows.append(windows)
        return all_windows

    results = ds_obs.process_two_files_without_parallel_output(
        ds_syn, process)
    return results


@click.command()
@click.option('--obs_path', required=True, type=str, help="obs path")
@click.option('--syn_path', required=True, type=str, help="syn path")
@click.option('--out_path', required=True, type=str, help="pickle file path")
@click.option('--logfile', required=True, type=str, help="log file")
def main(obs_path, syn_path, out_path, logfile):
    logger.add(logfile, format="{time} {level} {message}", level="INFO")

    with ASDFDataSet(obs_path, mode="r") as ds_obs:
        with ASDFDataSet(syn_path, mode="r") as ds_syn:
            logger.info(f"start to process {obs_path} & {syn_path}")
            results = run(ds_obs, ds_syn)
            logger.info(f"finish processing {obs_path} & {syn_path}")

    if(isroot):
        with open(out_path, "wb") as handle:
            pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)
    comm.Barrier()


if __name__ == "__main__":
    main()
