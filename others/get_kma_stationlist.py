from glob import glob
from os.path import join

kma_base_dir = "/mnt/research/seismolab2/japan_slab/data/data_kma/data.rotated"


def main():
    allsacs = glob(join(kma_base_dir, "*", "*sac"))
    fnames = [item.split("/")[-1] for item in allsacs]
    stations = [item.split(".")[-3] for item in fnames]
    stations = sorted(set(stations))
    with open("kma_stations.txt", "w") as f:
        for item in stations:
            f.write(f"{item}\n")


if __name__ == "__main__":
    main()
