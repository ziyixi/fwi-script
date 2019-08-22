#!/bin/bash
#----------------------------------------------------
# Sample Slurm job script
#   for TACC Stampede2 SKX nodes
#
#   *** Serial Job on SKX Normal Queue ***
# 
# Last revised: 20 Oct 2017
#
# Notes:
#
#   -- Copy/edit this script as desired.  Launch by executing
#      "sbatch skx.serial.slurm" on a Stampede2 login node.
#
#   -- Serial codes run on a single node (upper case N = 1).
#        A serial code ignores the value of lower case n,
#        but slurm needs a plausible value to schedule the job.
#
#   -- For a good way to run multiple serial executables at the
#        same time, execute "module load launcher" followed
#        by "module help launcher".

#----------------------------------------------------

#SBATCH -J setup_dir           # Job name
#SBATCH -o myjob.o%j       # Name of stdout output file
#SBATCH -e myjob.e%j       # Name of stderr error file
#SBATCH -p skx-normal      # Queue (partition) name
#SBATCH -N 1               # Total # of nodes (must be 1 for serial)
#SBATCH -n 1               # Total # of mpi tasks (should be 1 for serial)
#SBATCH -t 03:00:00        # Run time (hh:mm:ss)
#SBATCH --mail-user=xiziyi@mail.egr.msu.edu
#SBATCH --mail-type=all    # Send email at begin and end of job
#SBATCH -A TG-EAR140030       # Allocation name (req'd if you have more than 1)

# Other commands must follow all #SBATCH directives...

module list
pwd
date

# Launch serial code...

PY="/work/05880/tg851791/stampede2/anaconda3/envs/seismology/bin/python"
$PY setup_relocation_dir.py --main_dir /work/05880/tg851791/stampede2/japan_slab/relocation/depth_simulation/work --output_dir /scratch/05880/tg851791/relocation/depth_simulation --ref_dir /work/05880/tg851791/stampede2/japan_slab/relocation/depth_simulation/ref --cmts_dir /work/05880/tg851791/stampede2/japan_slab/relocation/depth_simulation/cmts --depth_perturbation -15,-10,-5,5,10,15
date

# ---------------------------------------------------