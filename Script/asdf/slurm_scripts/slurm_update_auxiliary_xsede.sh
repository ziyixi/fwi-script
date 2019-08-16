#!/bin/bash
#----------------------------------------------------
# Sample Slurm job script
#   for TACC Stampede2 KNL nodes
#
#   *** MPI Job on Normal Queue ***
# 
# Last revised: 20 Oct 2017
#
# Notes:
#
#   -- Launch this script by executing
#      "sbatch knl.mpi.slurm" on Stampede2 login node.
#
#   -- Use ibrun to launch MPI codes on TACC systems.
#      Do not use mpirun or mpiexec.
#
#   -- Max recommended MPI tasks per KNL node: 64-68
#      (start small, increase gradually).
#
#   -- If you're running out of memory, try running
#      fewer tasks per node to give each task more memory.
#
#----------------------------------------------------

#SBATCH -J aux_200           # Job name
#SBATCH -o myjob.o%j       # Name of stdout output file
#SBATCH -e myjob.e%j       # Name of stderr error file
#SBATCH -p skx-normal          # Queue (partition) name
#SBATCH -N 1               # Total # of nodes 
#SBATCH -n 48              # Total # of mpi tasks
#SBATCH -t 04:00:00        # Run time (hh:mm:ss)
#SBATCH -A TG-EAR140030       # Allocation name (req'd if you have more than 1)

# Other commands must follow all #SBATCH directives...

module list
pwd
date
module remove python2/2.7.15
module load mvapich2/2.3.1
# Launch MPI code... 

PY="/work/05880/tg851791/stampede2/anaconda3/envs/asdf/bin/python"
main_dir="/scratch/05880/tg851791/process_data/all_200_processed_simplified"

cd ../process 
$PY serial_update_auxiliary_info__.py --main_dir $main_dir

date
# ---------------------------------------------------