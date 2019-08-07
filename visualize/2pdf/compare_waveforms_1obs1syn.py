import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
import obspy
import pyasdf
from obspy.geodetics.base import gps2dist_azimuth, locations2degrees
from obspy.taup import TauPyModel
from recordtype import recordtype
import numpy as np
import click
import matplotlib as mpl

label_size = 25
mpl.rcParams['xtick.labelsize'] = label_size

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


@click.command()
@click.option('--obs_asdf', required=True, type=str)
@click.option('--syn_asdf', required=True, type=str)
@click.option('--window_path', required=True, type=str)
@click.option('--azimuth_width', required=True, type=int)
@click.option('--output_pdf', required=True, type=str)
@click.option('--waves_perpage', required=True, type=int)
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
        # get num_pages for this azimuth bin
        if(num_azimuth_bin_plot_traces % waves_perpage == 0):
            num_pages = num_azimuth_bin_plot_traces // waves_perpage
        else:
            num_pages = (num_azimuth_bin_plot_traces // waves_perpage)+1

        for ipage in range(num_pages):
            start_index = ipage*waves_perpage
            end_index = (ipage+1)*waves_perpage
            azimuth_bin_plot_traces_this_page = azimuth_bin_plot_traces[start_index:end_index]

            fig = plt.figure(figsize=(150, 150))
            index_count = 1
            axr, axz, axt = None, None, None  # get the last axes
            xticks = None
            for each_plot_trace_all in azimuth_bin_plot_traces_this_page:
                each_plot_trace = each_plot_trace_all[1]
                each_plot_id = each_plot_trace_all[0]
                # z
                axz = fig.add_subplot(waves_perpage, 3, index_count)
                obs = each_plot_trace.obs_z
                syn = each_plot_trace.syn_z
                x_obs = np.linspace(0, obs.stats.endtime -
                                    obs.stats.starttime, obs.stats.npts)
                x_syn = np.linspace(0, syn.stats.endtime -
                                    syn.stats.starttime, syn.stats.npts)
                y_obs = obs.data
                y_syn = syn.data
                axz.plot(x_obs, y_obs, color="k")
                axz.plot(x_syn, y_syn, color="r")
                axz.get_yaxis().set_ticklabels([])
                index_count += 1
                # r
                axr = fig.add_subplot(waves_perpage, 3,
                                      index_count, sharey=axz)
                obs = each_plot_trace.obs_r
                syn = each_plot_trace.syn_r
                x_obs = np.linspace(0, obs.stats.endtime -
                                    obs.stats.starttime, obs.stats.npts)
                x_syn = np.linspace(0, syn.stats.endtime -
                                    syn.stats.starttime, syn.stats.npts)
                y_obs = obs.data
                y_syn = syn.data
                axr.plot(x_obs, y_obs, color="k")
                axr.plot(x_syn, y_syn, color="r")
                axr.get_yaxis().set_ticklabels([])
                index_count += 1
                # t
                axt = fig.add_subplot(waves_perpage, 3,
                                      index_count, sharey=axz)
                obs = each_plot_trace.obs_t
                syn = each_plot_trace.syn_t
                x_obs = np.linspace(0, obs.stats.endtime -
                                    obs.stats.starttime, obs.stats.npts)
                x_syn = np.linspace(0, syn.stats.endtime -
                                    syn.stats.starttime, syn.stats.npts)
                y_obs = obs.data
                y_syn = syn.data
                axt.plot(x_obs, y_obs, color="k")
                axt.plot(x_syn, y_syn, color="r")
                axt.get_yaxis().set_ticklabels([])
                index_count += 1

                # add labels
                axz.set_ylabel(
                    f"id:{each_plot_id}\ngcarc:{each_plot_trace.info['gcarc']:.2f}\nazimuth:{each_plot_trace.info['azimuth']:.2f}", fontsize=60)
                # get xticks
                xticks = np.arange(np.min(x_obs), np.max(x_obs)+1, 100)
                axz.set_xticks(xticks)
                axr.set_xticks(xticks)
                axt.set_xticks(xticks)

                # plot title
                if(index_count == 4):
                    axr.set_title(
                        f"azimuth:{azimuth_width*index_azimuth}-{azimuth_width*(index_azimuth+1)}\npage:{ipage}", fontsize=200)

                # plot travel times
                info=each_plot_trace.info
                # z
                plot_travel_times(axz,"p",info["p"],np.max(x_obs),"blue")
                plot_travel_times(axz,"pp",info["pp"],np.max(x_obs),"y")
                plot_travel_times(axz,"sp",info["sp"],np.max(x_obs),"r")
                plot_travel_times(axz,"rayleigh",info["rayleigh"],np.max(x_obs),"c")
                plot_travel_times(axz,"s",info["s"],np.max(x_obs),"green")
                plot_travel_times(axz,"ss",info["ss"],np.max(x_obs),"black")
                # r
                plot_travel_times(axr,"p",info["p"],np.max(x_obs),"blue")
                plot_travel_times(axr,"pp",info["pp"],np.max(x_obs),"y")
                plot_travel_times(axr,"sp",info["sp"],np.max(x_obs),"r")
                plot_travel_times(axr,"rayleigh",info["rayleigh"],np.max(x_obs),"c")
                plot_travel_times(axr,"s",info["s"],np.max(x_obs),"green")
                plot_travel_times(axr,"ss",info["ss"],np.max(x_obs),"black")
                # t
                plot_travel_times(axt,"s",info["s"],np.max(x_obs),"green")
                plot_travel_times(axt,"ss",info["ss"],np.max(x_obs),"black")
                plot_travel_times(axt,"scs",info["scs"],np.max(x_obs),"magenta")
                plot_travel_times(axt,"love",info["love"],np.max(x_obs),"teal")
                if(index_count==4):
                    axz.legend(loc='upper right')
                    axr.legend(loc='upper right')
                    axt.legend(loc='upper right')

                # plot windows
                # z
                plot_windows(axz,"p",each_plot_trace.win_z,"blue")
                plot_windows(axz,"pp",each_plot_trace.win_z,"y")
                plot_windows(axz,"sp",each_plot_trace.win_z,"r")
                plot_windows(axz,"rayleigh",each_plot_trace.win_z,"c")
                plot_windows(axz,"s",each_plot_trace.win_z,"green")
                plot_windows(axz,"ss",each_plot_trace.win_z,"black")
                # r
                plot_windows(axr,"p",each_plot_trace.win_r,"blue")
                plot_windows(axr,"pp",each_plot_trace.win_r,"y")
                plot_windows(axr,"sp",each_plot_trace.win_r,"r")
                plot_windows(axr,"rayleigh",each_plot_trace.win_r,"c")
                plot_windows(axr,"s",each_plot_trace.win_r,"green")
                plot_windows(axr,"ss",each_plot_trace.win_r,"black")
                # t
                plot_windows(axt,"s",each_plot_trace.win_t,"green")
                plot_windows(axt,"ss",each_plot_trace.win_t,"black")
                plot_windows(axt,"scs",each_plot_trace.win_t,"magenta")
                plot_windows(axt,"love",each_plot_trace.win_t,"teal")


            plt.subplots_adjust(wspace=0, hspace=0)
            pdf.savefig(fig)
        plt.close(fig=fig)
    pdf.close()

def plot_travel_times(ax,phasename,traveltime,length,thecolor):
    if(traveltime<1e-6):
        return
    if(traveltime<length):
        ax.scatter(traveltime,0,color=thecolor,label=phasename,s=9)

def plot_windows(ax,phasename,win,thecolor):
    if(type(win)==type(None)):
        return
    mapper={
        "p":(3,4),
        "s":(5,6),
        "pp":(7,8),
        "ss":(9,10),
        "sp":(11,12),
        "scs":(13,14),
        "rayleigh":(15,16),
        "love":(17,18)
    }
    start_time=win[mapper[phasename][0]]
    end_time=win[mapper[phasename][1]]
    if(start_time=="None" or end_time=="None"):
        return
    else:
        start_time=float(start_time)
        end_time=float(end_time)
        ax.axvspan(start_time, end_time, alpha=0.1, color=thecolor)

if __name__ == "__main__":
    main()
