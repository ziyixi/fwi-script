"""
calculate snr for all the asdf files in a directory
"""

import numpy as np
import obspy
import pyasdf
from obspy.geodetics.base import gps2dist_azimuth, locations2degrees
from obspy.taup import TauPyModel
from tqdm import tqdm
from glob import glob
from os.path import join, basename
import multiprocessing

model = TauPyModel(model='ak135')
basedir = "/scratch/05880/tg851791/process_data/all_484_processed_simplified"
outputdir = "/scratch/05880/tg851791/process_data/snr"


def get_first_arrival(stla, stlo, evla, evlo, evdp, comp):
    gcarc = locations2degrees(stla, stlo, evla, evlo)
    if(comp == "Z" or comp == "R"):
        phase_list = ["p", "P"]
    elif(comp == "T"):
        phase_list = ["s", "S"]
    arrivals = model.get_travel_times(source_depth_in_km=evdp,
                                      distance_in_degree=gcarc,
                                      phase_list=phase_list)
    return arrivals[0].time


def calculate_snr(tr, first_arrival):
    starttime = tr.stats.starttime
    endtime = tr.stats.endtime

    noise = tr.slice(starttime, starttime+first_arrival)
    signal = tr.slice(starttime+first_arrival, endtime)

    noise_data = noise.data
    signal_data = signal.data
    noise_npts = noise.stats.npts
    signal_npts = signal.stats.npts

    pn = np.sum(noise_data**2)/noise_npts
    ps = np.sum(signal_data**2)/signal_npts
    snr = 10*np.log10(ps/pn)
    return snr


def handle_one_asdf(asdf_path, output_path):
    ds = pyasdf.ASDFDataSet(asdf_path, mode="r")
    all_stations = ds.waveforms.list()
    event = ds.events[0]
    origin = event.preferred_origin() or event.origins[0]
    evla = origin.latitude
    evlo = origin.longitude
    evdp = origin.depth/1000

    with open(output_path, "w") as f:
        for station in all_stations:
            sg = ds.waveforms[station]
            waveform_tags = sg.get_waveform_tags()
            thetag = waveform_tags[0]
            st = sg[thetag]
            inv = sg["StationXML"]
            stla = inv[0][0].latitude
            stlo = inv[0][0].longitude
            snr = np.zeros(3)
            mapper = ["R", "T", "Z"]
            for i in range(3):
                comp = mapper[i]
                first_arrival = get_first_arrival(
                    stla, stlo, evla, evlo, evdp, comp)
                snr[i] = calculate_snr(st[i], first_arrival)
            f.write(f"{station} {snr[0]:.4f} {snr[1]:.4f} {snr[2]:.4f}\n")


def kernel(kernel_input):
    asdf_path = kernel_input[0]
    output_path = kernel_input[1]
    handle_one_asdf(asdf_path, output_path)


def calculate_for_all_asdf_files():
    all_files = glob(join(basedir, "*h5"))
    all_fnames = [basename(item) for item in all_files]
    all_output = [join(outputdir, item) for item in all_fnames]
    kernel_iters = list(zip(all_files, all_output))

    with multiprocessing.Pool(48) as pool:
        r = list(tqdm(pool.imap(kernel, kernel_iters), total=len(kernel_iters)))


if __name__ == "__main__":
    calculate_for_all_asdf_files()
