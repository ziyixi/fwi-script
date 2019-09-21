"""
Check if there is the condition that we have sac files but not sacpz files.
"""
import numpy as np

from200_events = np.loadtxt("./from200_events.txt", dtype=np.str)
from284_events = np.loadtxt("./from284_events.txt", dtype=np.str)
basedir = "/scratch/05880/tg851791/process_data/sac_raw_all_smallregion"


# test from200 events
