from slurmpy import Slurm

# paths and constant values
nproc_old = 441
old_mesh_dir = "/work/05880/tg851791/stampede2/japan_slab/gll_models/normal_6/work/model/full_ak135_good_min_tao_smooth"
old_model_dir = "/work/05880/tg851791/stampede2/japan_slab/gll_models/normal_6/work/model/full_ak135_good_min_tao_smooth"
model_tags = "vpv,vph,vsv,vsh,eta,qmu,rho"
output_file = "/work/05880/tg851791/stampede2/japan_slab/gll_models/smaller_region/models_for_plot/ppm_refine_ref_big"
region = "75/0/165/65/0/805.232"
npts = "501/501/119"
nproc = "18/18"

basedir = "/work/05880/tg851791/stampede2/fwi-script/Program/specfem_gll.jl"

command = "date;"
command += f"cd {basedir};"
command += f"ibrun julia src/program/get_ppm_model.jl --nproc_old {nproc_old} --old_mesh_dir {old_mesh_dir} --old_model_dir {old_model_dir} --model_tags {model_tags} --output_file {output_file} --region {region} --npts {npts} --nproc {nproc};"
command += "date;"

s = Slurm("interp", {"partition": "skx-normal",
                     "nodes": 10, "ntasks": 324, "time": "04:00:00", "account": "TG-EAR130011"})

s.run(command)
