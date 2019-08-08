#!/bin/bash
#----------------------------------------------------
# Sample Slurm job script
#   for TACC Stampede2 SKX nodes
#
#   *** OpenMP Job on SKX Normal Queue ***
# 
# Last revised: 20 Oct 2017
#
# Notes:
#
#   -- Launch this script by executing
#   -- Copy/edit this script as desired.  Launch by executing
#      "sbatch skx.openmp.slurm" on a Stampede2 login node.
#
#   -- OpenMP codes run on a single node (upper case N = 1).
#        OpenMP ignores the value of lower case n,
#        but slurm needs a plausible value to schedule the job.
#
#   -- Default value of OMP_NUM_THREADS is 1; be sure to change it!
#
#   -- Increase thread count gradually while looking for optimal setting.
#        If there is sufficient memory available, the optimal setting
#        is often 48 (1 thread per core) but may be higher.

#----------------------------------------------------

#SBATCH -J generate_sync           # Job name
#SBATCH -o myjob.o%j       # Name of stdout output file
#SBATCH -e myjob.e%j       # Name of stderr error file
#SBATCH -p skx-normal      # Queue (partition) name
#SBATCH -N 1               # Total # of nodes (must be 1 for OpenMP)
#SBATCH -n 1               # Total # of mpi tasks (should be 1 for OpenMP)
#SBATCH -t 04:00:00        # Run time (hh:mm:ss)
#SBATCH -A TG-EAR140030       # Allocation name (req'd if you have more than 1)

# Other commands must follow all #SBATCH directives...

module list
pwd
date

# Set thread count (default value is 1)...

# Launch OpenMP code...
PY="/work/05880/tg851791/stampede2/anaconda3/envs/seismology/bin/python"
. activate seismology
$PY parallel_generate_sync_asdf_working.py --base_dir /scratch/05880/tg851791/sync_work/sync/hybrid_lns --out_dir /scratch/05880/tg851791/sync_work/sync/asdf_hybrid --cmt_dir /work/05880/tg851791/stampede2/japan_slab/cmts/Japan_slab         # Do not use ibrun or any other MPI launcher

date
# ---------------------------------------------------