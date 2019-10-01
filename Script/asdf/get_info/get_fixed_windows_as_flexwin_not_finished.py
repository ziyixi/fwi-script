from pyflex import window
import json

import click
import numpy as np
import obspy
import pyasdf
from mpi4py import MPI
from obspy.geodetics.base import gps2dist_azimuth, locations2degrees
from obspy.taup import TauPyModel

model = TauPyModel(model='ak135')
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
isroot = (rank == 0)


def get_property_times(stla, stlo, evla, evlo, evdp):
    property_times = {
        "first_p": None,
        "first_s": None,
        "surface_wave": None,
        "local_station": False,
        "gcarc": None,
        "azimuth": None
    }

    # sphere gcircle distance, since taup use sphere
    gcarc = locations2degrees(stla, stlo, evla, evlo)
    property_times["gcarc"] = gcarc

    # calculate first arrivals
    arrivals = model.get_travel_times(source_depth_in_km=evdp,
                                      distance_in_degree=gcarc,
                                      phase_list=["p", "P", "s", "S", "3.5kmps"])

    for item in arrivals:
        # find p
        if(property_times["first_p"] == None):
            if(item.name == "p" or item.name == "P"):
                property_times["first_p"] = item.time

        # find s
        if(property_times["first_s"] == None):
            if(item.name == "s" or item.name == "S"):
                property_times["first_s"] = item.time

        # find surface wave
        if(property_times["surface_wave"] == None):
            if(item.name == "3.5kmps"):
                property_times["surface_wave"] = item.time

    # see if it's local stations:
    for item in arrivals:
        if(item.name == "p" or item.name == "s"):
            property_times["local_station"] = True
            break
        elif(item.name == "P" or item.name == "S"):
            property_times["local_station"] = False
            break

    # get azimuth, from the source to the stations
    _, property_times["azimuth"], _ = gps2dist_azimuth(evla, evlo, stla, stlo)

    # always could success
    return property_times


def get_windows(starttime, endtime,  property_times):
    ptime = property_times["first_p"]
    stime = property_times["first_s"]
    surftime = property_times["surface_wave"]
    is_close = property_times["local_station"]
    gcarc = property_times["gcarc"]

    result = {
        "pn": None,
        "p": None,
        "s": None,
        "surf": None
    }

    # different conditions
    if(gcarc < 10):  # local stations
        if(is_close):
            result["pn"] = (starttime, starttime+60)
        else:
            if(ptime < 20):
                result["pn"] = (starttime, starttime+stime)
                result["surf"] = (starttime+stime, starttime+stime+60)
            elif(20 <= ptime < 60):
                result["pn"] = (starttime+ptime-10, starttime+ptime+30)
                result["surf"] = (starttime+stime-10, starttime+stime+110)
            else:
                result["pn"] = (starttime+ptime-20, starttime+ptime+60)
                result["surf"] = (starttime+stime-10, starttime+stime+180)
    else:  # regional stations
        win_surface_start = starttime+surftime - 40
        win_surface_end = starttime+surftime + 180

        result["p"] = (starttime+ptime-20, starttime+ptime+60)
        result["s"] = (starttime+stime-20, starttime+stime+80)
        if(endtime-win_surface_start < 100):
            pass
        elif(win_surface_end > endtime):
            result["surf"] = (win_surface_start, endtime)
        else:
            result["surf"] = (win_surface_start, win_surface_end)

    return result
