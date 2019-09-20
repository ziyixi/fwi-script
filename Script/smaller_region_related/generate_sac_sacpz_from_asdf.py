"""
Generate raw sac data files as Dr. Chen required.
"""
import pyasdf
import multiprocessing
import tqdm
from os.path import join, basename, isfile
from glob import glob
import os
import obspy
from obspy.geodetics.base import gps2dist_azimuth
from obspy.geodetics import kilometers2degrees
import numpy as np

basedir = "/scratch/05880/tg851791/process_data/asdf_raw_all_smallregion"
outdir = "/scratch/05880/tg851791/process_data/sac_raw_all_smallregion"


def generate_single(gcmtid):
    # firstly we get paths
    sac_path = join(outdir, gcmtid)
    try:
        os.mkdir(sac_path)
    except:
        pass
    sacpz_path = join(outdir, gcmtid, "SACPZ")
    try:
        os.mkdir(sacpz_path)
    except:
        pass
    asdf_path = join(basedir, f"raw_{gcmtid}.h5")
    ds = pyasdf.ASDFDataSet(asdf_path, mode="r")

    # get some info
    evla = ds.events[0].origins[0].latitude
    evlo = ds.events[0].origins[0].longitude
    evdp = ds.events[0].origins[0].depth/1000

    # get all net_sta list
    net_sta_list = ds.waveforms.list()

    # loop all
    for net_sta in net_sta_list:
        try:
            st = ds.waveforms[net_sta].raw
            inv = ds.waveforms[net_sta].StationXML
        except:
            print(asdf_path, net_sta)
            continue
        # write sac files
        for tr_raw in st:
            tr = tr_raw.copy()
            fname = tr.id
            fpath = join(sac_path, fname)
            if(isfile(fpath)):
                continue
            # add some info to sac files
            tr.stats.sac = obspy.core.util.attribdict.AttribDict()
            tr.stats.sac.stla = inv[0][0].latitude
            tr.stats.sac.stlo = inv[0][0].longitude
            tr.stats.sac.stel = inv[0][0].elevation/1000
            tr.stats.sac.evla = evla
            tr.stats.sac.evlo = evlo
            tr.stats.sac.evdp = evdp
            # calculate dist,az,baz,gcarc
            dist_m, az, baz = gps2dist_azimuth(
                evla, evlo, tr.stats.sac.stla, tr.stats.sac.stlo)
            dist = dist_m/1000
            gcarc = kilometers2degrees(dist)

            tr.stats.sac.dist = dist
            tr.stats.sac.az = az
            tr.stats.sac.baz = baz
            tr.stats.sac.gcarc = gcarc

            # write
            tr.write(fpath, format="SAC")

        # write sacpz files
        fname = net_sta
        fpath = join(sacpz_path, fname)
        if(isfile(fpath)):
            continue
        # there are possibility that inv has problem, log it
        try:
            inv.write(fpath, format="SACPZ")
        except:
            # failed inv means we process them using sacpz file before
            pass


def main():
    """
    Use multiprocessing to generate files in parallel
    """
    # get gcmtids
    npfile = np.loadtxt("./psmeca_gcmts_Japan_Slab", dtype=np.str)
    gcmtid_list = sorted(set(npfile[:, -1]))
    with multiprocessing.Pool(processes=48) as pool:
        r = list(tqdm.tqdm(pool.imap(generate_single,
                                     gcmtid_list), total=len(gcmtid_list)))


if __name__ == "__main__":
    main()
