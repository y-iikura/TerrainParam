#!/usr/bin/env python
# -*- coding: utf-8 -*-
#cd /Users/iikura/Desktop/ViewShed
#PATH=$PATH:/Applications/exelis/idl85/bin:~/bin
#fangle.py kiban50_450F.tif 60.0

import sys
import os
import numpy as np
import cv2
import subprocess as sub

param=sys.argv
print param
if len(param)!= 3:
  print " * Usage : fangle.py dem.tif angle"


fname=param[1]
dem=cv2.imread(fname,-1)
jmax,imax=dem.shape

#demx=cv2.resize(dem,(500,500))
#cv2.imshow('dem',demx/np.max(demx))
#cv2.waitKey(0)
#cv2.destroyWindow('dem')

fname2=fname[:-4]+'.futm'
print fname2

if os.path.exists(fname2) == False:
  recl = np.zeros(1,dtype=np.uint32)+4000000
  g=open(fname2,'wb')
  g.write(recl.tobytes())
  g.write(dem.tobytes())
  g.write(recl.tobytes())
  g.close()

f = open(fname2,'rb')
recl = np.fromfile(f, dtype='uint32', count=1)
tmp = np.fromfile(f, dtype='float32', count=dem.size) 
recl = np.fromfile(f, dtype='uint32', count=1)
f.close()


angle=param[2]
while True:
  command='Fortran/elv_angle '+fname2+' '+angle
  print command
  sub.call(command,shell=True)
  f = open('angle.img','rb')
  recl = np.fromfile(f, dtype='uint32', count=1)
  tmp = np.fromfile(f, dtype='float32', count=imax*jmax) 
  recl = np.fromfile(f, dtype='uint32', count=1)
  f.close()
  view=tmp.reshape(jmax,imax)
  viewx=cv2.resize(view,(500,500))
  cv2.imshow('view',viewx)
  print 'To continue, enter 1 at view'
  k=cv2.waitKey(0)
  if k !=49: exit()
  cv2.destroyWindow('view')
  print ' Input angle :'
  angle = raw_input()
  
exit()

