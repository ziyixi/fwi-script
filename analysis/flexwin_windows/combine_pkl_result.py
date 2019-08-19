"""
Combine all the pickle files
"""
import pickle
from os.path import join, basename
from glob import glob
import tqdm

basedir = "/scratch/05880/tg851791/process_windows/windows_0818"
process_flag = "preprocessed_10s_to_120s"
outpath = f"/scratch/05880/tg851791/process_windows/{process_flag}.log"


def read_single_file(filename):
    result = None
    with open(filename, "rb") as f:
        result = pickle.load(f)
    return result


def main():
    # get all files
    allfiles = glob(join(basedir, f"*{process_flag}*"))
    allfnames = [basename(item) for item in allfiles]
    result = {}
    for filename, fname in tqdm.tqdm(zip(allfiles, allfnames), total=len(allfiles)):
        gcmtid = fname.split(".")[0]
        result[gcmtid] = read_single_file(filename)

    with open(outpath, "wb") as handle:
        pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()
