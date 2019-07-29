#!/bin/bash --login
########## SBATCH Lines for Resource Request ##########
 
#SBATCH --time=03:00:00             # limit of wall clock time - how long the job will run (same as -t)
#SBATCH --ntasks=1                 # number of tasks - how many tasks (nodes) that you require (same as -n)
#SBATCH --cpus-per-task=1           # number of CPUs (or cores) per task (same as -c)
#SBATCH --mem-per-cpu=2G            # memory required per allocated CPU (or core) - amount of memory (in bytes)
#SBATCH --job-name simplify      # you can give your job a name for easier identification (same as -J)
 
########## Command Lines to Run ##########

PY=/mnt/home/xiziyi/anaconda3/envs/seismology/bin/python 
base_dir=/mnt/ls15/scratch/users/xiziyi/process_asdf/validation/processed 
log_file=/mnt/ls15/scratch/users/xiziyi/process_asdf/validation/simple.log
output_dir=/mnt/ls15/scratch/users/xiziyi/process_asdf/validation/processed_simple 

$PY ../process/simplify_stations_in_a_directory.py --base_dir $base_dir --log_file $log_file --output_dir $output_dir             ### call your executable (similar to mpirun)
 
scontrol show job $SLURM_JOB_ID     ### write job information to output file
