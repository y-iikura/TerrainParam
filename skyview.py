#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cd /Volumes/Transcend/TerrainParam
# skyview.py kiban50_450F.tif 6


import sys
import numpy as np
import cv2
import terrain_util as ut

#reload(ut)

param=sys.argv

if len(param) != 3:
  print " * Usage : skyview.py dem.tif num"
  print "           num : number of directions"
  exit()

dem=ut.read_tif(param[1])
num=int(param[2])

#dem=ut.read_tif('kiban50_450F.tif')
#num=6

sangle=np.arange(num)*360.0/num
print sangle

print ut.dx,ut.dy,ut.imax,ut.jmax

slp=ut.slope(dem)
asp=ut.orient(dem)

ut.asp=asp
ut.coss=np.cos(slp)
ut.sins=np.sin(slp)

if ut.dx != ut.dy or ut.imax != ut.jmax:
  print " For dx=dy and imax=jmax only !!"
  exit()

ut.dd=ut.dx

sky=np.zeros((ut.jmax,ut.imax),dtype=np.float32)

for angle in sangle:
  print '* '+ 'angle='+str(angle)+' *' 
  sky=sky+ut.sky(dem,angle,2)/num
  

#print np.max(sky),np.min(sky)

sky[np.where(sky<0.0)]=0.0
#skyx=cv2.resize(sky,(500,500))
#cv2.imshow('sky',skyx)
#cv2.destroyWindow('sky')


ut.write_tif('skyview.tif',sky.astype(np.float32))

exit()


