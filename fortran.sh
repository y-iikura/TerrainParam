cd Fortran
gfortran -c sky_util.f90
gfortran -c elv_angle.f90
gfortran -o elv_angle sky_util.o elv_angle.o
#elv_angle kiban50_450F.futm 60.0