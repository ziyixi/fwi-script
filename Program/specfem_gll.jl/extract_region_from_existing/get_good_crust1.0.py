import numpy as np
from os.path import basename, join

modified_files = ["./crust1.0/crust1.vp",
                  "./crust1.0/crust1.vs", "./crust1.0/crust1.rho"]

for thefile in modified_files:
    data = np.loadtxt(thefile)
    out_path = join("./crust1.0_fixed", basename(thefile))

    # update data
    for row in data:
        for index in range(1, 9):
            if(row[index] == 0):
                row[index] = row[index-1]

    with open(out_path, "w") as f:
        for row in data:
            newline = ""
            for index in range(9):
                newline += f"{row[index]:.2f}  "
            newline += "\n"
            f.write(newline)
