from slurmpy import Slurm

# * command 1
nproc_old = 336
old_mesh_dir = "/work/05880/tg851791/stampede2/japan_slab/gll_models/normal_6/work/control_file/tao"
old_model_dir = "/work/05880/tg851791/stampede2/japan_slab/gll_models/normal_6/work/perturbation/per_tao"
nproc_new = 441
new_mesh_dir = "/work/05880/tg851791/stampede2/japan_slab/gll_models/normal_6/work/control_file/ak135_bad"
new_model_dir = "/work/05880/tg851791/stampede2/japan_slab/gll_models/normal_6/work/perturbation/per_ak135_bad"
model_tags = ",".join(["vph", "vpv", "vsh", "vsv", "eta", "qmu", "rho"])
output_dir = "/work/05880/tg851791/stampede2/japan_slab/gll_models/normal_6/work/perturbation/per_ak135_bad_tao"

command1 = f"ibrun julia ./src/program/xsem_interp_mesh2.jl --nproc_old {nproc_old} --old_mesh_dir {old_mesh_dir} --old_model_dir {old_model_dir} --nproc_new {nproc_new} --new_mesh_dir {new_mesh_dir} --new_model_dir {new_model_dir} --model_tags {model_tags} --output_dir {output_dir}"

s = Slurm("interp", {"partition": "skx-normal",
                     "nodes": 10, "ntasks": 441, "time": "00:60:00","account":"TG-EAR140030"})

s.run(f"cd ..; date; {command1}; date;")