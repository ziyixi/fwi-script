"""
Calculate amp ratios using the window json files.
"""
import numpy as np
from glob import glob
from os.path import join, basename
import json
import pandas as pd

basedir = "/scratch/05880/tg851791/relocation/work/misfit_json"
process_flag_body = "d0.preprocessed_20s_to_120s.body.json"
process_flag_surf = "d0.preprocessed_20s_to_120s.surf.json"


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


def get_keys():
    all_files = glob(join(basedir, f"*{process_flag_body}"))
    result = set()
    for file_path in all_files:
        fname = basename(file_path)
        gcmtid = fname.split(".")[0]
        result.add(gcmtid)
    return sorted(result)


def extract_amp_info(gcmtid_list):
    result = {}
    for gcmtid in gcmtid_list:
        result[gcmtid] = {
            "pz_sz": [],
            "pr_sr": [],
            "pz_pr": [],
            "sz_sr": [],
            "sz_st": [],
            "sr_st": [],
            "surfz_pz": [],
            "surfz_sz": [],
            "surfr_pr": [],
            "surfr_sr": [],
            "surfz_surfr": []
        }
        file_path_body = join(basedir, f"{gcmtid}.{process_flag_body}")
        file_path_surf = join(basedir, f"{gcmtid}.{process_flag_surf}")
        with open(file_path_body, "r") as f_body:
            with open(file_path_surf, "r") as f_surf:
                data_dict_body = json.load(f_body)
                data_dict_surf = json.load(f_surf)
                data_dict = combine_json_dict(data_dict_body, data_dict_surf)
                for net_sta in data_dict:
                    amp_info = data_dict[net_sta]["amplitude"]
                    pz = (amp_info["z"]["p"] or amp_info["z"]["pn"])
                    sz = (amp_info["z"]["s"])
                    pr = (amp_info["r"]["p"] or amp_info["r"]["pn"])
                    sr = (amp_info["r"]["s"])
                    st = (amp_info["t"]["s"])
                    surfz = (amp_info["z"]["surf"])
                    surfr = (amp_info["r"]["surf"])
                    if(pz and sz):
                        result[gcmtid]["pz_sz"].append(pz/sz)
                    if(pr and sr):
                        result[gcmtid]["pr_sr"].append(pr/sr)
                    if(pz and pr):
                        result[gcmtid]["pz_pr"].append(pz/pr)
                    if(sz and sr):
                        result[gcmtid]["sz_sr"].append(sz/sr)
                    if(sz and st):
                        result[gcmtid]["sz_st"].append(sz/st)
                    if(sr and st):
                        result[gcmtid]["sr_st"].append(sr/st)
                    if(surfz and pz):
                        result[gcmtid]["surfz_pz"].append(surfz/pz)
                    if(surfz and sz):
                        result[gcmtid]["surfz_sz"].append(surfz/sz)
                    if(surfr and pr):
                        result[gcmtid]["surfr_pr"].append(surfr/pr)
                    if(surfr and sr):
                        result[gcmtid]["surfr_sr"].append(surfr/sr)
                    if(surfz and surfr):
                        result[gcmtid]["surfz_surfr"].append(surfz/surfr)
    json.dump(result, open("amp_ratio.json", 'w'))


if __name__ == "__main__":
    gcmtid_list = get_keys()
    extract_amp_info(gcmtid_list)
