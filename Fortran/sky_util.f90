module sky_util
	implicit none
	integer, parameter :: imax=1000,jmax=1000
	real, parameter :: dx=10.0,dy=10.0,pie=3.1415927
	real,dimension(imax,jmax) :: DEM,DVIEW
        real,dimension(1600,1600) :: DEM2,DVIEW2
! VISIT :: dummy

contains
    real function eangle(j,k,m)
	integer j,k,m
	real z1,z2
	if(k == m) then
		eangle=0.0; return
	else 
		z1=DEM2(k,j)
		z2=DEM2(m,j)
		eangle=(z2-z1)/(m-k); return		
	end if
    end function eangle

    subroutine suihei()
	integer,dimension(1600) :: dline
	integer i,j,k,m,found
	real z0,z1,tmp1,tmp2
	dline(1600)=1600-1
	do j=1,1600
		i=1600-2
		z0=DEM2(i,j)
		do while ((z0 == 0.0) .and. (i > 0))
			dline(i)=i
			DVIEW2(i,j)=0
			i=i-1
			z0=DEM2(i,j) 
		enddo
		do while (i > 0)  
			k=i+1
			found = 1
			do while (found == 1)
				tmp1=eangle(j,i,k)
 				m = dline(k)
        			tmp2 = eangle(j,k,m)
        			if ((tmp1 < tmp2) .and. (m .ne. k)) then
					 k = m
        			else 
          				found = 0
          				if (tmp1 > tmp2) then
						dline(i) = k
          				else 
						dline(i) = m
					endif
				endif
			enddo
      			DVIEW2(i,j) = tmp1/10.0
      			i = i - 1
 		enddo
	enddo
    end subroutine suihei

    subroutine view(angle)
	real angle
	integer i,j,ii,jj
	DEM2=0
        DVIEW=0
	angle=angle*pie/180.0
	do j=1,1600
	do i=1,1600
		ii=nint(cos(angle)*(i-1600/2.0)-sin(angle)*(j-1600/2.0)+imax/2.0)
		jj=nint(sin(angle)*(i-1600/2.0)+cos(angle)*(j-1600/2.0)+jmax/2.0)
		if ((ii < 1) .or. (jj < 1) .or. (ii > imax) .or. (jj > jmax)) then
			DEM2(i,j)=0
		else
			DEM2(i,j)=DEM(ii,jj)
		endif
	enddo
	enddo
        call suihei()
	do j=1,jmax
	do i=1,imax
		ii=nint(cos(angle)*(i-imax/2.0)+sin(angle)*(j-jmax/2.0)+1600/2.0)
		jj=nint(-sin(angle)*(i-imax/2.0)+cos(angle)*(j-jmax/2.0)+1600/2.0)
		if (ii < 1) ii=1
		if (jj < 1) jj=1
		if (ii > 1600) ii=1600
		if (jj > 1600) jj=1600
		DVIEW(i,j)=DVIEW2(ii,jj)
	enddo
	enddo

    end subroutine view

end module sky_util
