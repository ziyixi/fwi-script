import numpy as np
stations = np.loadtxt("./stations", dtype=str)

stwin_path = "/mnt/ls15/scratch/users/xiziyi/process_asdf/logs/stwin_num_10.txt"
stwins = np.loadtxt(stwin_path, dtype=str)

with open("./stwin_stations", "w") as f:
    for item in stwins:
        key = item[0]
        for stitem in stations:
            if(stitem[1] == "FNET"):
                stitem[1] = "BO"
            stkey = f"{stitem[1]}.{stitem[0]}"
            if(key == stkey):
                f.write(f"{stitem[3]} {stitem[2]} {item[1]}\n ")
