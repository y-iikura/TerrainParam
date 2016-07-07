#!/usr/bin/env python
# -*- coding: utf-8 -*-
#cd /Users/iikura/Desktop/ViewShed
#PATH=$PATH:/Applications/exelis/idl85/bin:~/bin
#fskyview.py kiban50_450F.tif 6

import sys
import os
import numpy as np
import cv2
import subprocess as sub
import terrain_util as ut

param=sys.argv
print param
if len(param)!= 3:
  print " * Usage : fskyview.py dem.tif num"
  print "        num : number of directions"


fname=param[1]
#dem=cv2.imread(fname,-1)
dem=ut.read_tif(fname)
print ut.dx,ut.dy,ut.imax,ut.jmax
jmax,imax=dem.shape

#demx=cv2.resize(dem,(500,500))
#cv2.imshow('dem',demx/np.max(demx))
#cv2.waitKey(0)
#cv2.destroyWindow('dem')

slp=ut.slope(dem)
asp=ut.orient(dem)

coss=np.cos(slp)
sins=np.sin(slp)

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


num=param[2]
sangle=np.arange(int(num))*360.0/float(num)
print sangle

view=np.zeros((jmax,imax),dtype=np.float32)
for angle in sangle:
  command='Fortran/elv_angle '+fname2+' '+str(angle)
  print command
  t0=angle*np.pi/180.0
  cosfa=np.cos(t0-asp)
  sub.call(command,shell=True)
  f = open('angle.img','rb')
  recl = np.fromfile(f, dtype='uint32', count=1)
  tmp = np.fromfile(f, dtype='float32', count=imax*jmax) 
  recl = np.fromfile(f, dtype='uint32', count=1)
  f.close()
  tmp[tmp < 0.0] = 0.0
  tmp=tmp.reshape(jmax,imax)
  hf=np.pi/2-np.arctan(tmp)
  view=view+coss*np.sin(hf)**2+sins*cosfa*(hf-np.sin(hf)*np.cos(hf))
  
#viewx=cv2.resize(view,(500,500))
#cv2.imshow('view',viewx)

ut.write_tif('fskyview.tif',view)
  
exit()

