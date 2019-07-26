
baseurl = "/Users/ziyixi/work/Datas/stations/STATIONS"


def main():
    with open("/Users/ziyixi/work/Datas/stations/STATIONS_new", "w") as g:
        with open(baseurl, "r") as f:
            for line_raw in f:
                if(not ("FNET" in line_raw)):
                    g.write(line_raw)
                else:
                    fnet_pos = line_raw.find("FNET")
                    line = line_raw[:fnet_pos]+"BO"+line_raw[fnet_pos+4:]
                    g.write(line)


if __name__ == "__main__":
    main()
