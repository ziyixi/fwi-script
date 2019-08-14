1. we should first load phdf5, then compile with LDSHARED="mpicc -shared" CC=mpicc python setup.py configure --mpi --hdf5=/opt/apps/intel18/impi18_0/phdf5/1.10.4/x86_64/

2. we should compile hdf5 with version 1.10.2, and we should use mvapich2 instead.
