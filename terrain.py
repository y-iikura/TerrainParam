#!/usr/bin/env python
# -*- coding: utf-8 -*-
#cd /Users/iikura/Desktop/TerrainParam 
# terrain.py kiban50_450F.tif


import sys
import numpy as np
import cv2
import terrain_util as ut

#reload(ut)

param=sys.argv

if (len(param) <2) or (len(param) > 4):
  print " * Usage : terrain.py dem.tif => for slope and aspect"
  print "         : terrain.py dem.tif  direction => for elevation angle"
  print "         : terrain.py dem.tif  sun_el sun_az_ => for solar incident "
  exit()

dem=ut.read_tif(param[1])
print ut.dx,ut.dy,ut.imax,ut.jmax

slp=ut.slope(dem)
asp=ut.orient(dem)

if len(param) == 2:
  ut.write_tif('slope.tif',slp.astype(np.float32))
  ut.write_tif('aspect.tif',asp.astype(np.float32))
  exit()

if len(param) == 4:
  sun_el=float(param[2])
  sun_az=float(param[3])
  inc=ut.incident(dem,sun_el,sun_az)
  ut.write_tif('incident.tif',inc.astype(np.float32))
  exit()
  

ut.asp=asp
ut.coss=np.cos(slp)
ut.sins=np.sin(slp)

if ut.dx != ut.dy or ut.imax != ut.jmax:
  print " For dx=dy and imax=jmax only !!"
  exit()

ut.dd=ut.dx
d_angle=float(param[2])
dview=ut.sky(dem,d_angle,1)

ut.write_tif('angle'+param[2]+'.tif',dview.astype(np.float32))

exit()


