import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
import obspy
import pyasdf
from obspy.geodetics.base import gps2dist_azimuth, locations2degrees
from obspy.taup import TauPyModel
from recordtype import recordtype
import numpy as np
import click

to_plot_trace = recordtype("to_plot_trace", [
                           "obs_z", "syn_z",  "obs_r", "syn_r",  "obs_t", "syn_t", "win_z", "win_r", "win_t", "info"])


def build_to_plot_traces(obs_ds, syn_ds, windows):
    # obs_ds,syn_ds opened asdf file, windows: loaded np array
    # get keys
    keys = set(windows[:, 0])
    result = {}
    # for each item in keys, get info
    # since the window is selected according to the two asdf files, we can just use keys
    for key in keys:
        axkey = key.replace(".", "_")
        tag_obs = obs_ds.waveforms[key].get_waveform_tags()[0]
        tag_syn = syn_ds.waveforms[key].get_waveform_tags()[0]

        info = obs_ds.auxiliary_data.Traveltimes[axkey].parameters
        obs_st = obs_ds.waveforms[key][tag_obs]
        syn_st = syn_ds.waveforms[key][tag_syn]
        obs_r = obs_st[0]
        obs_t = obs_st[1]
        obs_z = obs_st[2]
        syn_r = syn_st[0]
        syn_t = syn_st[1]
        syn_z = syn_st[2]

        # get windows
        wins = windows[windows[:, 0] == key]
        win_z = wins[wins[:, 2] == "vertical"]
        if(win_z.shape[0] == 0):
            win_z = None
        else:
            win_z = win_z[0]
        win_r = wins[wins[:, 2] == "radial"]
        if(win_r.shape[0] == 0):
            win_r = None
        else:
            win_r = win_r[0]
        win_t = wins[wins[:, 2] == "tangential"]
        if(win_t.shape[0] == 0):
            win_t = None
        else:
            win_t = win_t[0]
        result[key] = to_plot_trace(
            obs_z, syn_z, obs_r, syn_r, obs_t, syn_t, win_z, win_r, win_t, info)
    return result


def build_plottting_structure(plot_traces, azimuth_width):
    # we assume 360%azimuth_width==0
    num_azimuths = 360//azimuth_width
    result = [[] for i in range(num_azimuths)]
    # for each item in plot_traces, seprate them into different []
    for key in plot_traces:
        value = plot_traces[key]
        info = value.info
        azimuth = info["azimuth"]
        index_azimuth = int(azimuth//azimuth_width)
        result[index_azimuth].append((key, value))

    # for each azimuth bin, sort them according to the gcarc
    def sort_func(item):
        value = item[1]
        gcarc = value.info["gcarc"]
        return gcarc
    for index_azimuth in range(num_azimuths):
        result[index_azimuth] = sorted(result[index_azimuth], key=sort_func)
    return result


def main(obs_asdf, syn_asdf, window_path, azimuth_width, output_pdf, waves_perpage):
    obs_ds = pyasdf.ASDFDataSet(obs_asdf, mode="r")
    syn_ds = pyasdf.ASDFDataSet(syn_asdf, mode="r")
    windows = np.loadtxt(window_path, dtype=str)

    plot_traces = build_to_plot_traces(obs_ds, syn_ds, windows)
    plotting_structure = build_plottting_structure(plot_traces, azimuth_width)

    # plot figures
    pdf = matplotlib.backends.backend_pdf.PdfPages(output_pdf)
    figs = plt.figure()

    num_azimuths = 360//azimuth_width
    for index_azimuth in range(num_azimuths):
        # for each azimuth bin
        azimuth_bin_plot_traces = plotting_structure[index_azimuth]
        num_azimuth_bin_plot_traces = len(azimuth_bin_plot_traces)
        # get num_page for this azimuth bin
        if(num_azimuth_bin_plot_traces % waves_perpage == 0):
            num_page = num_azimuth_bin_plot_traces // waves_perpage
        else:
            num_page = (num_azimuth_bin_plot_traces // waves_perpage)+1
