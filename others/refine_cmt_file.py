from glob import glob
from os.path import join

cmts_dir = "/Users/ziyixi/work/seismic-code/fwi-scripts/visualize/data/cmts"
output_dir = "/Users/ziyixi/work/seismic-code/fwi-scripts/visualize/data/cmts_new"


def main():
    all_cmt_urls = glob(join(cmts_dir, "*"))
    for item in all_cmt_urls:
        fname = item.split("/")[-1]
        with open(join(output_dir, fname), "w") as f:
            with open(item, "r") as g:
                for line in g:
                    if(line[:7] == " PDE 2 "):
                        newline = " PDE "+line[7:]
                        f.write(newline)
                    else:
                        f.write(line)


if __name__ == "__main__":
    main()
