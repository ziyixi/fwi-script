"""
Get weighted misfit
"""
from recordtype import recordtype
import numpy as np
import json
import collections
from glob import glob
from os.path import join, basename, isfile
import pandas as pd
import tqdm

base_dir = "/scratch/05880/tg851791/relocation/work/misfit_json"
snr_dir = "/scratch/05880/tg851791/process_data/snr"
bin_angle = 20
min_snr = 3

misfit_windows = recordtype("misfit_windows", [
                            "channel", "phase", "misfit", "length", "amplitude", "gcarc", "azimuth", "azimuth_weight"])
Misfit = collections.namedtuple('Misfit', ["p_z", "p_r", "s_z", "s_r", "s_t", "surf_z",
                                           "surf_r", "surf_z_mt", "surf_r_mt", "p_all", "sv_all", "sh_all", "ray_all", "theall"])


def extract_information(json_dict, misfit_mapper):
    p_z = []
    p_r = []
    s_z = []
    s_r = []
    s_t = []
    surf_z = []
    surf_r = []
    surf_z_mt = []
    surf_r_mt = []
    for net_sta in json_dict:
        info = json_dict[net_sta]
        if(misfit_mapper != None):
            snrr, snrt, snrz = misfit_mapper[net_sta]
        else:
            snrr, snrt, snrz = 100

        if((info["misfit_r"]["pn"] != None) and (info["amplitude"]["r"]["pn"] != None) and (snrr >= min_snr)):
            p_r.append(misfit_windows(
                "r", "pn", info["misfit_r"]["pn"], info["window_length"]["r"]["pn"], info["amplitude"]["r"]["pn"], info["property_times"]["gcarc"], info["property_times"]["azimuth"], 0))
        if((info["misfit_z"]["pn"] != None) and (info["amplitude"]["z"]["pn"] != None) and (snrz >= min_snr)):
            p_z.append(misfit_windows(
                "z", "pn", info["misfit_z"]["pn"], info["window_length"]["z"]["pn"], info["amplitude"]["z"]["pn"], info["property_times"]["gcarc"], info["property_times"]["azimuth"], 0))
        if((info["misfit_r"]["p"] != None) and (info["amplitude"]["r"]["p"] != None) and (snrr >= min_snr)):
            p_r.append(misfit_windows(
                "r", "p", info["misfit_r"]["p"], info["window_length"]["r"]["p"], info["amplitude"]["r"]["p"], info["property_times"]["gcarc"], info["property_times"]["azimuth"], 0))
        if((info["misfit_z"]["p"] != None) and (info["amplitude"]["z"]["p"] != None) and (snrz >= min_snr)):
            p_z.append(misfit_windows(
                "z", "p", info["misfit_z"]["p"], info["window_length"]["z"]["p"], info["amplitude"]["z"]["p"], info["property_times"]["gcarc"], info["property_times"]["azimuth"], 0))
        if((info["misfit_r"]["s"] != None) and (info["amplitude"]["r"]["s"] != None) and (snrr >= min_snr)):
            s_r.append(misfit_windows(
                "r", "s", info["misfit_r"]["s"], info["window_length"]["r"]["s"], info["amplitude"]["r"]["s"], info["property_times"]["gcarc"], info["property_times"]["azimuth"], 0))
        if((info["misfit_t"]["s"] != None) and (info["amplitude"]["t"]["s"] != None) and (snrt >= min_snr)):
            s_t.append(misfit_windows(
                "t", "s", info["misfit_t"]["s"], info["window_length"]["t"]["s"], info["amplitude"]["t"]["s"], info["property_times"]["gcarc"], info["property_times"]["azimuth"], 0))
        if((info["misfit_z"]["s"] != None) and (info["amplitude"]["z"]["s"] != None) and (snrz >= min_snr)):
            s_z.append(misfit_windows(
                "z", "s", info["misfit_z"]["s"], info["window_length"]["z"]["s"], info["amplitude"]["z"]["s"], info["property_times"]["gcarc"], info["property_times"]["azimuth"], 0))
        if((info["misfit_r"]["surf_rs"] != None) and (info["amplitude"]["r"]["surf"] != None) and (snrr >= min_snr)):
            surf_r.append(misfit_windows(
                "r", "surf", info["misfit_r"]["surf_rs"], info["window_length"]["r"]["surf"], info["amplitude"]["r"]["surf"], info["property_times"]["gcarc"], info["property_times"]["azimuth"], 0))
        if((info["misfit_z"]["surf_rs"] != None) and (info["amplitude"]["z"]["surf"] != None) and (snrz >= min_snr)):
            surf_z.append(misfit_windows(
                "z", "surf", info["misfit_z"]["surf_rs"], info["window_length"]["z"]["surf"], info["amplitude"]["z"]["surf"], info["property_times"]["gcarc"], info["property_times"]["azimuth"], 0))
        if((info["misfit_r"]["surf"] != None) and (info["amplitude"]["r"]["surf"] != None) and (snrr >= min_snr)):
            surf_r_mt.append(misfit_windows(
                "r", "surf_mt", info["misfit_r"]["surf"], info["window_length"]["r"]["surf"], info["amplitude"]["r"]["surf"], info["property_times"]["gcarc"], info["property_times"]["azimuth"], 0))
        if((info["misfit_z"]["surf"] != None) and (info["amplitude"]["z"]["surf"] != None) and (snrz >= min_snr)):
            surf_z_mt.append(misfit_windows(
                "z", "surf_mt", info["misfit_z"]["surf"], info["window_length"]["z"]["surf"], info["amplitude"]["z"]["surf"], info["property_times"]["gcarc"], info["property_times"]["azimuth"], 0))

    return p_z, p_r, s_z, s_r, s_t, surf_z, surf_r, surf_z_mt, surf_r_mt


def adjust_distance_influence(p_z, p_r, s_z, s_r, s_t, surf_z, surf_r, surf_z_mt, surf_r_mt):
    """
    the distance coefficient shouldn't be considered as a type of weight, but a kind of "normalization"
    """
    for item in p_z:
        item.misfit = item.misfit*item.gcarc
        item.amplitude = item.amplitude*item.gcarc
    for item in p_r:
        item.misfit = item.misfit*item.gcarc
        item.amplitude = item.amplitude*item.gcarc
    for item in s_z:
        item.misfit = item.misfit*item.gcarc
        item.amplitude = item.amplitude*item.gcarc
    for item in s_r:
        item.misfit = item.misfit*item.gcarc
        item.amplitude = item.amplitude*item.gcarc
    for item in s_t:
        item.misfit = item.misfit*item.gcarc
        item.amplitude = item.amplitude*item.gcarc
    for item in surf_z:
        item.misfit = item.misfit*np.sqrt(item.gcarc)
        item.amplitude = item.amplitude*np.sqrt(item.gcarc)
    for item in surf_r:
        item.misfit = item.misfit*np.sqrt(item.gcarc)
        item.amplitude = item.amplitude*np.sqrt(item.gcarc)
    return p_z, p_r, s_z, s_r, s_t, surf_z, surf_r, surf_z_mt, surf_r_mt


def adjust_timewindow_influence(p_z, p_r, s_z, s_r, s_t, surf_z, surf_r, surf_z_mt, surf_r_mt):
    """
    we should use the misfit per second
    """
    for item in p_z:
        item.misfit = item.misfit/item.length
    for item in p_r:
        item.misfit = item.misfit/item.length
    for item in s_z:
        item.misfit = item.misfit/item.length
    for item in s_r:
        item.misfit = item.misfit/item.length
    for item in s_t:
        item.misfit = item.misfit/item.length
    for item in surf_z:
        item.misfit = item.misfit/item.length
    for item in surf_r:
        item.misfit = item.misfit/item.length
    return p_z, p_r, s_z, s_r, s_t, surf_z, surf_r, surf_z_mt, surf_r_mt


def calculate_azimuth_weight(p_z, p_r, s_z, s_r, s_t, surf_z, surf_r, surf_z_mt, surf_r_mt, bin_angle=20):
    """
    only calculate azimuth weight, consider number of windows within the bin angle for the same kind of phase
    """
    # get numpy arrays storing azimuth information for each type of windows
    def get_azimuth_weight_for_a_type(misfit_win_list):
        N_misfit_win = len(misfit_win_list)
        azimuth_array = np.zeros(N_misfit_win)
        # store to azimuth_array
        for index, misfit_win in enumerate(misfit_win_list):
            azimuth_array[index] = misfit_win.azimuth
        return azimuth_array

    # get the number of stations inside the azimuth bin, don't consider extreme conditions
    def get_number_of_stations_within_bin(azimuth_array, bin_angle, azimuth_this_station):
        azimuth_start = azimuth_this_station-bin_angle/2
        azimuth_end = azimuth_this_station+bin_angle/2
        # different conditions
        selected_azimuth_list = None
        if((azimuth_start >= 0) and (azimuth_end <= 360)):
            selected_azimuth_list = azimuth_array[(
                azimuth_array >= azimuth_start) & (azimuth_array <= azimuth_end)]
        elif((azimuth_start < 0) and (azimuth_end <= 360)):
            azimuth_start = azimuth_start+360
            selected_azimuth_list = azimuth_array[(
                azimuth_array >= azimuth_start) | (azimuth_array <= azimuth_end)]
        elif((azimuth_start >= 0) and (azimuth_end > 360)):
            azimuth_end = azimuth_end-360
            selected_azimuth_list = azimuth_array[(
                azimuth_array >= azimuth_start) | (azimuth_array <= azimuth_end)]
        else:
            raise Exception(
                "not implemented, azimuth_this_station is too large")
        return len(selected_azimuth_list)

    # get azimuth_weight for each window
    all_list = [p_z, p_r, s_z, s_r, s_t, surf_z, surf_r, surf_z_mt, surf_r_mt]
    for pha_cha_item in all_list:
        weight_store = np.zeros(len(pha_cha_item))
        azimuth_array = get_azimuth_weight_for_a_type(pha_cha_item)
        for index, window_item in enumerate(pha_cha_item):
            azimuth_this_station = window_item.azimuth
            N_in = get_number_of_stations_within_bin(
                azimuth_array, bin_angle, azimuth_this_station)
            # wait to normalize
            weight_store[index] = 1/N_in
        weight_all = np.sum(weight_store)
        weight_store = weight_store/weight_all
        # now we can set the azimuth_weight
        for index, window_item in enumerate(pha_cha_item):
            pha_cha_item[index].azimuth_weight = weight_store[index]
    return p_z, p_r, s_z, s_r, s_t, surf_z, surf_r, surf_z_mt, surf_r_mt


def get_weighted_misfit(p_z, p_r, s_z, s_r, s_t, surf_z, surf_r, surf_z_mt, surf_r_mt):
    """
    Here we only consider the azimuth weight as the distance has the meaning of "normalization"
    """
    all_list = [p_z, p_r, s_z, s_r, s_t, surf_z, surf_r, surf_z_mt, surf_r_mt]
    all_misfit_list = [0.0 for item in range(len(all_list))]
    for index, pha_cha_item in enumerate(all_list):
        weighted_misfit = 0.0
        for item in pha_cha_item:
            weighted_misfit += item.misfit*item.azimuth_weight
        all_misfit_list[index] = weighted_misfit
    return np.array(all_misfit_list)


def combine_json_dict(body_dict, surf_dict):
    """
    combine the json dict for both the surface wave and the body wave
    """
    for net_sta in body_dict:
        for level1_key in ["misfit_r", "misfit_t", "misfit_z", "property_times"]:
            for level2_key in body_dict[net_sta][level1_key]:
                body_dict[net_sta][level1_key][level2_key] = body_dict[net_sta][
                    level1_key][level2_key] or surf_dict[net_sta][level1_key][level2_key]

        for level1_key in ["window_length", "amplitude"]:
            for level2_key in body_dict[net_sta][level1_key]:
                for level3_key in body_dict[net_sta][level1_key][level2_key]:
                    body_dict[net_sta][level1_key][level2_key][level3_key] = body_dict[net_sta][level1_key][
                        level2_key][level3_key] or surf_dict[net_sta][level1_key][level2_key][level3_key]
    return body_dict


def get_misfit_each_pair(body_json, surf_json, bin_angle, misfit_path):
    # combine json files
    body_f = open(body_json, "r")
    surf_f = open(surf_json, "r")
    body_dict = json.load(body_f)
    surf_dict = json.load(surf_f)
    json_dict = combine_json_dict(body_dict, surf_dict)

    # get snr information
    misfit_mat = None
    misfit_mapper = None
    if(isfile(misfit_path)):
        misfit_mat = np.loadtxt(misfit_path, dtype=np.str)
        misfit_mat[:, 1:] = misfit_mat[:, 1:].astype(np.float)
        for row in misfit_mat:
            misfit_mapper[row[0]] = (row[1], row[2], row[3])
    else:
        print(misfit_path)

    # extract to windows
    p_z, p_r, s_z, s_r, s_t, surf_z, surf_r, surf_z_mt, surf_r_mt = extract_information(
        json_dict, misfit_mapper)
    p_z, p_r, s_z, s_r, s_t, surf_z, surf_r, surf_z_mt, surf_r_mt = adjust_distance_influence(
        p_z, p_r, s_z, s_r, s_t, surf_z, surf_r, surf_z_mt, surf_r_mt)
    p_z, p_r, s_z, s_r, s_t, surf_z, surf_r, surf_z_mt, surf_r_mt = adjust_timewindow_influence(
        p_z, p_r, s_z, s_r, s_t, surf_z, surf_r, surf_z_mt, surf_r_mt)
    p_z, p_r, s_z, s_r, s_t, surf_z, surf_r, surf_z_mt, surf_r_mt = calculate_azimuth_weight(
        p_z, p_r, s_z, s_r, s_t, surf_z, surf_r, surf_z_mt, surf_r_mt, bin_angle=bin_angle)
    p_z_misfit, p_r_misfit, s_z_misfit, s_r_misfit, s_t_misfit, surf_z_misfit, surf_r_misfit, surf_z_mt_misfit, surf_r_mt_misfit = get_weighted_misfit(
        p_z, p_r, s_z, s_r, s_t, surf_z, surf_r, surf_z_mt, surf_r_mt)

    # calculate misfit for some phases
    p_all_misfit = 0.5*(p_z_misfit+p_r_misfit)
    sv_all_misfit = 0.5*(s_z_misfit+s_r_misfit)
    sh_all_misfit = s_t_misfit
    ray_all_misfit = 0.5*(surf_z_misfit+surf_r_misfit)
    theall_misfit = 0.25*(0.5*(p_z_misfit+p_r_misfit) +
                          0.5*(s_z_misfit+s_r_misfit)+s_t_misfit+0.5*(surf_z_misfit+surf_r_misfit))

    # get the weighted misfit
    return Misfit(p_z_misfit, p_r_misfit, s_z_misfit, s_r_misfit, s_t_misfit, surf_z_misfit, surf_r_misfit, surf_z_mt_misfit, surf_r_mt_misfit, p_all_misfit, sv_all_misfit, sh_all_misfit, ray_all_misfit, theall_misfit)


def get_pairs():
    json_paths = glob(join(base_dir, "*json"))
    keys = set()
    for json_item in json_paths:
        json_fname = basename(json_item)
        gcmtid, depth, process_flag, pos_flag, _ = json_fname.split(".")
        thekey = ".".join([gcmtid, depth, process_flag])
        keys.add(thekey)
    keys = sorted(keys)
    result_pairs = []
    for thekey in keys:
        thebody = thekey+".body.json"
        thesurf = thekey+".surf.json"
        gcmtid, depth, process_flag = thekey.split(".")
        # the misfit path
        misfit_path = join(snr_dir, f"raw_{gcmtid}.{process_flag}.h5")
        result_pairs.append((join(base_dir, thebody), join(
            base_dir, thesurf), gcmtid, depth, process_flag, misfit_path))
    return result_pairs


def sum2pd(result_pairs):
    df = pd.DataFrame(columns=["gcmtid", "depth", "process_flag", "snr", "p_z", "p_r", "s_z", "s_r", "s_t",
                               "surf_z", "surf_r", "surf_z_mt", "surf_r_mt", "p_all", "sv_all", "sh_all", "ray_all", "theall"])
    num_pairs = len(result_pairs)
    for i in tqdm.tqdm(range(num_pairs), total=num_pairs):
        thepair = result_pairs[i]
        themisfit = get_misfit_each_pair(
            thepair[0], thepair[1], bin_angle, thepair[5])
        df.loc[i] = [thepair[2], thepair[3], thepair[4], themisfit.p_z, themisfit.p_r, themisfit.s_z, themisfit.s_r, themisfit.s_t,
                     themisfit.surf_z, themisfit.surf_r, themisfit.surf_z_mt, themisfit.surf_r_mt, themisfit.p_all, themisfit.sv_all,
                     themisfit.sh_all, themisfit.ray_all, themisfit.theall]
    df.to_csv("misfit.csv")


if __name__ == "__main__":
    result_pairs = get_pairs()
    sum2pd(result_pairs)
