from slurmpy import Slurm

# paths and constant values
nproc_old = 324
old_mesh_dir = "/work/05880/tg851791/stampede2/japan_slab/gll_models/smaller_region/specfem/DATABASES_MPI_smooth"
old_model_dir = "/work/05880/tg851791/stampede2/japan_slab/gll_models/smaller_region/perturbation/per_fwea18_fwea18_ref"
model_tags = "vpv,vph,vsv,vsh,eta,qmu,rho"
output_file = "/work/05880/tg851791/stampede2/japan_slab/gll_models/smaller_region/models_for_plot/per_fwea18_fwea18_ref"
region = "122/24/147/49/0/800"
npts = "501/501/161"
nproc = "18/18"

basedir = "/work/05880/tg851791/stampede2/fwi-script/Program/specfem_gll.jl"

command = "date;"
command += f"cd {basedir};"
command += f"ibrun julia src/program/get_ppm_model.jl --nproc_old {nproc_old} --old_mesh_dir {old_mesh_dir} --old_model_dir {old_model_dir} --model_tags {model_tags} --output_file {output_file} --region {region} --npts {npts} --nproc {nproc};"
command += "date;"

s = Slurm("interp", {"partition": "skx-normal",
                     "nodes": 10, "ntasks": 324, "time": "04:00:00", "account": "TG-EAR140030"})

s.run(command)
