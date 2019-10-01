"""
Rank the snr of stations for each event in a directory.
"""

import numpy as np
from glob import glob
from os.path import basename, join
import tqdm

base_dir = "/scratch/05880/tg851791/process_data/snr_more"
output_dir = "/scratch/05880/tg851791/process_data/snr_ranked"


def reorder_single(raw_name, out_name):
    data = np.loadtxt(raw_name, dtype=np.str)
    z_snr = data[:, -1].astype(np.float)
    z_order = np.argsort(z_snr)
    print(z_order.shape, data.shape)
    data = data[:, z_order]
    np.savetxt(out_name, data)


def sort_all():
    all_files = glob(join(base_dir, "*"))
    all_bases = [basename(item) for item in all_files]
    all_outputs = [join(output_dir, item) for item in all_bases]
    for raw_name, out_name in tqdm.tqdm(zip(all_files, all_outputs)):
        reorder_single(raw_name, out_name)


if __name__ == "__main__":
    sort_all()
