from glob import glob
from os.path import join
import obspy

kma_base_dir = "/mnt/research/seismolab2/japan_slab/data/data_kma/data.rotated"


def main():
    allsacs = glob(join(kma_base_dir, "*", "*sac"))
    fnames = [item.split("/")[-1] for item in allsacs]
    stations = [item.split(".")[-3] for item in fnames]
    stations = sorted(set(stations))
    # get stations mapper
    mapper = {}
    for item in stations:
        for each_sac in allsacs:
            fname = each_sac.split("/")[-1]
            if(item in fname):
                mapper[item] = each_sac
                break
    with open("kma_stations.txt", "w") as f:
        for item in stations:
            thetrace = obspy.read(mapper[item])[0]
            stla = thetrace.stats.sac.stla
            stlo = thetrace.stats.sac.stlo
            stel = thetrace.stats.sac.stel
            f.write(f"{item} KG {stla:.6f} {stlo:.6f} {stel:.1f} 0.0\n")


if __name__ == "__main__":
    main()
