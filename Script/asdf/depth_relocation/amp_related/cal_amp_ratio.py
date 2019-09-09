"""
Calculate amp ratios using the window json files.
"""
import numpy as np
from glob import glob
from os.path import join, basename
import json
import pandas as pd

basedir = "/scratch/05880/tg851791/relocation/work/misfit_json"
process_flag = "d0.preprocessed_10s_to_120s.surf.json"


def get_keys():
    all_files = glob(join(basedir, f"*{process_flag}"))
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
            "sr_st": []
        }
        file_path = join(basedir, f"{gcmtid}.{process_flag}")
        with open(file_path, "r") as f:
            data_dict = json.load(f)
            if(gcmtid == "201802112314A"):
                print(data_dict["HL.BAQ"]["amplitude"], file_path)
            for net_sta in data_dict:
                amp_info = data_dict[net_sta]["amplitude"]
                pz = (amp_info["z"]["p"] or amp_info["z"]["pn"])
                sz = (amp_info["z"]["s"])
                pr = (amp_info["r"]["p"] or amp_info["r"]["pn"])
                sr = (amp_info["r"]["s"])
                st = (amp_info["t"]["s"])
                if(net_sta == "HL.BAQ" and gcmtid == "201802112314A"):
                    print(pz, sz, pr, sr, st, data_dict[net_sta]["amplitude"])
                if(pz and sz):
                    print(gcmtid, "pz_sz")
                    result[gcmtid]["pz_sz"].append(pz/sz)
                if(pr and sr):
                    print(gcmtid, "pr_sr")
                    result[gcmtid]["pr_sr"].append(pr/sr)
                if(pz and pr):
                    print(gcmtid, "pz_pr")
                    result[gcmtid]["pz_pr"].append(pz/pr)
                if(sz and sr):
                    print(gcmtid, "sz_sr")
                    result[gcmtid]["sz_sr"].append(sz/sr)
                if(sz and st):
                    print(gcmtid, "sz_st")
                    result[gcmtid]["sz_st"].append(sz/st)
                if(sr and st):
                    print(gcmtid, "sr_st")
                    result[gcmtid]["sr_st"].append(sr/st)
    json.dump(result, open("amp_ratio.json", 'w'))


if __name__ == "__main__":
    gcmtid_list = get_keys()
    extract_amp_info(gcmtid_list)
