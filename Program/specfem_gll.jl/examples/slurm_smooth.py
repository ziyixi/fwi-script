from slurmpy import Slurm

s = Slurm("smooth", {"partition": "skx-normal", "account": "TG-EAR140030",
                     "nodes": 10, "ntasks": 441, "time": "02:00:00"})

nproc = 441
mesh_dir = "/work/05880/tg851791/stampede2/japan_slab/gll_models/normal_6/work/control_file/ak135_bad"
model_dir = "/work/05880/tg851791/stampede2/japan_slab/gll_models/normal_6/work/perturbation/per_ak135_bad_min_tao"
model_tags = ",".join(["vph", "vpv", "vsh", "vsv", "eta", "qmu", "rho"])
sigma_h = 50  # tong 2 degree 2km in the crust
sigma_v = 5  # 10km in the mantle, 2km in the crust
output_dir = "/work/05880/tg851791/stampede2/japan_slab/gll_models/normal_6/work/perturbation/per_ak135_bad_min_tao_smooth"
out_suffix = ".bin"
sem_url = "/work/05880/tg851791/stampede2/japan_slab/gll_models/normal_6/sem_utils/bin"

command = f"module load netcdf; date; cd {sem_url}; ibrun ./xsem_smooth {nproc} {mesh_dir} {model_dir} {model_tags} {sigma_h} {sigma_v} {output_dir} {out_suffix}; date;"
