"""
Calculate misfit for data and sync asdf pairs, using the windows from WindowPicker.
"""
import numpy as np
import click
import obspy
import pyasdf
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

CCT_treshold = 0.75
