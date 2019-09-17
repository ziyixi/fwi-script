"""
In a specfem directory, for all ascii files in OUTPUT_FILES, generate the P window for the test.
"""
from glob import glob
from os.path import join
import subprocess
import obspy

basedir = "/scratch/05880/tg851791/kernel_simulation_test/specfem3d_globe"
