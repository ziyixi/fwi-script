from slurmpy import Slurm

# * command 1
nproc_old = 336
old_mesh_dir = "/work/05880/tg851791/stampede2/japan_slab/gll_models/smaller_region/specfem/s362ani_tao_gll/DATABASES_MPI"
old_model_dir = "/work/05880/tg851791/stampede2/japan_slab/gll_models/smaller_region/perturbation/per_tao"
nproc_new = 324
new_mesh_dir = "/work/05880/tg851791/stampede2/japan_slab/gll_models/smaller_region/specfem/s362ani_good_gll/DATABASES_MPI"
new_model_dir = "/work/05880/tg851791/stampede2/japan_slab/gll_models/smaller_region/perturbation/per_bad"
model_tags = ",".join(["vph", "vpv", "vsh", "vsv", "eta", "qmu", "rho"])
output_dir = "/work/05880/tg851791/stampede2/japan_slab/gll_models/smaller_region/perturbation/per_s362ani_tao"

command1 = f"remora ibrun julia ./src/program/xsem_interp_mesh2.jl --nproc_old {nproc_old} --old_mesh_dir {old_mesh_dir} --old_model_dir {old_model_dir} --nproc_new {nproc_new} --new_mesh_dir {new_mesh_dir} --new_model_dir {new_model_dir} --model_tags {model_tags} --output_dir {output_dir}"

s = Slurm("interp", {"partition": "skx-normal",
                     "nodes": 7, "ntasks": 324, "time": "02:00:00", "account": "TG-EAR140030"})

s.run(
    f"module load remora; cd /work/05880/tg851791/stampede2/fwi-script/Program/specfem_gll.jl; date; {command1}; date;")
