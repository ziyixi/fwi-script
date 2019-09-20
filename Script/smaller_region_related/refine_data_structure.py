"""
Refine the data structure in order to send to Dr. Chen.
"""
from glob import glob
from os.path import join, basename
import subprocess

base_dir = "/scratch/05880/tg851791/process_data/sac_raw_all_smallregion"
output_dir = "/scratch/05880/tg851791/process_data/sac_raw_all_smallregion_refined"


def refine_single_event(gcmtid):
    # find which stations don't have three components
