"""
Generate the snr ranking for each station and each event.
"""
import numpy as np
from glob import glob
from os.path import join, basename
import pandas as pd
import tqdm

basedir = "/scratch/05880/tg851791/process_data/snr_more"
process_flag = "preprocessed_10s_to_120s"


def load_data():
    all_snr_files = glob(join(basedir, f"*{process_flag}.h5"))
    result = {}
    for item in all_snr_files:
        fname = basename(item)
        gcmtid_flag = fname.split(".")[0]
        gcmtid = gcmtid_flag.split("_")[-1]
        result[gcmtid] = np.loadtxt(item, dtype=np.str)
    return result


def get_stationnames(data):
    stationnames = set()
    for gcmtid in data:
        loaded_data = data[gcmtid]
        if(np.shape(loaded_data)[0] == 0):
            net_sta = []
        else:
            net_sta = loaded_data[:, 0]
        stationnames = stationnames | set(net_sta)
    return sorted(stationnames)


def extract_information():
    event_snr = {}
    event_snr_count = {}
    station_snr = {}
    station_snr_count = {}
    data = load_data()
    stationnames = get_stationnames(data)

    # init two dicts
    for gcmtid in data.keys():
        event_snr[gcmtid] = np.zeros(3)
        event_snr_count[gcmtid] = 0
    for stname in stationnames:
        station_snr[stname] = np.zeros(3)
        station_snr_count[stname] = 0

    # loop for all items:
    for gcmtid in tqdm.tqdm(data):
        data_array = data[gcmtid]
        for row in data_array:
            stname = row[0]
            event_snr[gcmtid] += np.array([float(row[1]),
                                           float(row[2]), float(row[3])])
            event_snr_count[gcmtid] += 1
            station_snr[stname] += np.array([float(row[1]),
                                             float(row[2]), float(row[3])])
            station_snr_count += 1

    return event_snr, event_snr_count, station_snr, station_snr_count


def write_to_pd(event_snr, event_snr_count, station_snr, station_snr_count):
    df_event = pd.DataFrame(columns=["gcmtid", "snr_r", "snr_t", "snr_z",
                                     "allsnr_r", "allsnr_t", "allsnr_z", "count"])
    df_station = pd.DataFrame(columns=["netsta", "snr_r", "snr_t", "snr_z",
                                       "allsnr_r", "allsnr_t", "allsnr_z", "count"])
    # event
    for index, gcmtid in enumerate(sorted(event_snr.keys())):
        count_info = event_snr_count[gcmtid]
        snr_info = event_snr[gcmtid]
        if(count_info == 0):
            df_event.loc[i] = [np.nan, np.nan, np.nan,
                               snr_info[0], snr_info[1], snr_info[2], count_info]
        else:
            df_event.loc[i] = [gcmtid, snr_info[0] /
                               count_info, snr_info[1]/count_info, snr_info[2]/count_info,  snr_info[0], snr_info[1], snr_info[2], count_info]
    # station
    for index, netsta in enumerate(sorted(station_snr.keys())):
        count_info = station_snr_count[netsta]
        snr_info = station_snr[netsta]
        df_station.loc[i] = [netsta, snr_info[0] /
                             count_info, snr_info[1]/count_info, snr_info[2]/count_info,  snr_info[0], snr_info[1], snr_info[2], count_info]

    df_event.to_csv(f"{process_flag}.event.csv", index=False)
    df_station.to_csv(f"{process_flag}.station.csv", index=False)


if __name__ == "__main__":
    event_snr, event_snr_count, station_snr, station_snr_count = extract_information()
    write_to_pd(event_snr, event_snr_count, station_snr, station_snr_count)
