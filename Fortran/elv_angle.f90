program main
	use sky_util
	implicit none
	real t0,t1,temp
	real angle
	character arg*20
!	real ref
!	real,dimension(imax,jmax) :: REF

	if (iargc().ne.2) stop 'Argument number should be 3 !'
	call getarg(1,arg)
!	open(1,file="kiban50_450F.futm",form='unformatted')
	open(1,file=arg,form='unformatted')
	read(1) DEM
	close(1)
	call getarg(2,arg)
	read(arg,*) angle
	call cpu_time(t0)
	call view(angle)
	call cpu_time(temp)
	write(*,*) temp-t0,'sec'
	!open(2,file="dem2.img",form='unformatted')
	!write(2) DEM2
	!close(2)
	!open(3,file="view2.img",form='unformatted')
	!write(3) DVIEW2
	!close(3)
	open(4,file="angle.img",form='unformatted')
	write(4) DVIEW
	close(4)

end program main



