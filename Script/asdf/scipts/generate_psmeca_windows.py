import numpy as np

raw = np.loadtxt("./psmeca_gcmts.25.log", dtype=str)
windows = "/mnt/ls15/scratch/users/xiziyi/process_asdf/logs/windows_num.txt"
new = np.loadtxt(windows, dtype=str)

# for win in new:
#     key=win[0].split(".")[0]
#     for item in raw:

for item in raw:
    key = item[-1]
    item[2] = 0
    for win in new:
        winkey = win[0].split(".")[0]
        if(key == winkey):
            item[2] = win[1]

# np.savetxt("./25d0.psmeca", raw, dtype=str)
with open("./25d0.psmeca", "w") as f:
    for item in raw:
        line = ""
        for each in item:
            line += f"{each} "
        line += "\n"
        f.write(line)
