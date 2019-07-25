# Examples

## Overview

Here we write some script to handle all the tasks. And also slurm scripts are provided.

Also the sem_utils is [Dr. Kai Tao's work](https://github.com/taotaokai/sem_utils)

## Workflow

1. Create a directory acting as the direcctory "specfem". In this directory, we will have the following specfem working directories:
    + tao: model FWEA18, the region should be the same with Dr. Tao's region.
    + min: model EARA2014, the region should be the same with Dr. Chen's region.
    + s362ani_bad_gll: model s362ani+crust1.0 not fixed
    + s362ani_good_gll: model s362ani+crust1.0 that has been fixed.
    + s362ani_min_gll: model s362ani+crust2.0 not fixed, with Dr. Chen's region.
    + s362ani_tao_gll: model s362ani+crust1.0 not fixed, with Dr. Tao's region.

2. Using the established directory "specfem", run tasks/generate_new_gll/structure.py, set up the working directory.

3. submit jobs in the specfem directory to run xmeshfem3D with the flag mesh_out turned on. (the settings are recorded in the setting directory). Use the script in tasks/submit_jobs/muljobs.py

4. Calculate the perturbation using get_perturbation.jl. We will have to calculate:
    + per_tao by tao/s362_tao_gll
    + per_min by min/s362_min_gll
    + per_bad by s362ani_bad_gll/s362ani_bad_gll

5. interpolate the models.
    + per_bad+per_min->per_s362ani_min
    + per_s362ani_min+per_tao->per_s362ani_min_tao

6. smooth the perturbation.
    + smooth the model using slurm_smooth.py. (compile sem_utils first)
    + per_s362ani_min_tao -> per_s362ani_min_tao_smooth

7. rename the files after smoothing.
    + use rename.py

8. retrive the model using retrive_model.jl
    + per_s362ani_min_tao_smooth*s362ani_good_gll -> s362ani_min_tao_smooth
    + cp s362ani_good_gll/\*reg2\* s362ani_min_tao_smooth
    + cp s362ani_good_gll/\*reg3\* s362ani_min_tao_smooth
