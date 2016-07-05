#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
from osgeo import gdal
from osgeo import osr

dx=0.0
dy=0.0
imax=0
jmax=0
asp=0.0
slp=0.0
coss=0.0
sins=0.0
dd=0.0

# for utm zone54
wkt='PROJCS["WGS 84 / UTM zone 54N",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",141],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH],AUTHORITY["EPSG","32654"]]'

def read_tif(fname):
  global xs,ye,dx,dy,imax,jmax
  src = gdal.Open(fname, gdal.GA_Update)
  pdem = src.GetRasterBand(1)
  gt = src.GetGeoTransform()
  image = pdem.ReadAsArray()
  proj = osr.SpatialReference()
  proj.ImportFromWkt(src.GetProjectionRef())
  wkt=proj.ExportToWkt()
  xs=gt[0]
  ye=gt[3]
  dx=gt[1]
  dy=-gt[5]
  jmax,imax=image.shape
  return image

def write_tif(dname,data):
  driver = gdal.GetDriverByName('GTiff')
  #wkt_projection=proj.ExportToWkt()
  y_pixels,x_pixels=data.shape
  dataset = driver.Create(
    dname,
    x_pixels,
    y_pixels,
    1,
    gdal.GDT_Float32, )
  dataset.SetGeoTransform((
    xs,
    dx,
    0, 
    ye,
    0,
    -dy))  
  #dataset.SetProjection(wkt_projection)
  dataset.SetProjection(wkt)
  dataset.GetRasterBand(1).WriteArray(data)
  dataset.FlushCache()

def yama(height,i0,j0,sigma) :
  temp=np.zeros([jmax,imax])
  for j in range(jmax):
    for i in range(imax):
      temp[j,i]=height*np.exp(((-(i-i0)**2-(j-j0)**2))/sigma**2)
  return temp

def slope(dem):
    a=(np.roll(dem,-1,1)-np.roll(dem,1,1))/dx/2
    a[:,0]=a[:,1] ; a[:,imax-1]=a[:,imax-2] 
    b=(np.roll(dem,1,0)-np.roll(dem,-1,0))/dy/2
    b[0,:]=b[1,:] ; b[jmax-1,:]=b[jmax-2,:]
    return np.sqrt(a**2+b**2)

def orient(dem):
    a=(np.roll(dem,-1,1)-np.roll(dem,1,1))/dx/2
    a[:,0]=a[:,1] ; a[:,imax-1]=a[:,imax-2] 
    b=(np.roll(dem,1,0)-np.roll(dem,-1,0))/dy/2
    b[0,:]=b[1,:] ; b[jmax-1,:]=b[jmax-2,:]
    return (np.arctan2(-a,-b)+2.0*np.pi) % (2.0*np.pi)

def incident(dem,sun_el,sun_az) :
  el=np.pi*sun_el/180 ; az=np.pi*sun_az/180
  a=(np.roll(dem,-1,1)-np.roll(dem,1,1))/60.0
  a[:,0]=a[:,1] ; a[:,imax-1]=a[:,imax-2] 
  b=(np.roll(dem,1,0)-np.roll(dem,-1,0))/60.0
  b[0,:]=b[1,:] ; b[jmax-1,:]=b[jmax-2,:]
  temp=-a*np.cos(el)*np.sin(az)-b*np.cos(el)*np.cos(az)+np.sin(el)
  return temp/np.sqrt(1+a**2+b**2)

def eangle(image,j,k,m):
  if k==m: return 0
  else:
    z1=image[j,k]
    z2=image[j,m]
    return (z2-z1)/(m-k)

def suihei(image,flag):
  ymax,xmax=image.shape
  print ymax,xmax
  dview=np.zeros([ymax,xmax],dtype=np.float32)
  dline=np.zeros(xmax,dtype=np.int16)
  dline[xmax-1]=xmax-1
  for j in np.arange(ymax):
    if (j % 100) == 0: print j
    i = xmax-2
    z0 = image[j,i]
    while (z0 == 0.0) and (i >= 0) :
      dline[i] = i
      dview[j,i] = 0
      i = i-1
      z0 = image[j,i]
    while i >= 0:
      k = i+1
      found = 1
      while found == 1:
        tmp1 = eangle(image,j,i,k)
        m = dline[k]
        tmp2 = eangle(image,j,k,m)
        if (tmp1 < tmp2) and (m != k): k = m
        else:
          found = 0
          if (tmp1 > tmp2) : dline[i] = k
          else: dline[i] = m
      if flag >= 1 : dview[j,i] = tmp1/dd
      else: dview[j,i]=dline[i]-i
      i = i - 1
  return dview

def sky(dem,tt,flag):
  global imax,jmax
  # flag = 0 : distance
  #      = 1 : slope
  #      = 2 : sky view factor  t0=tt*np.pi/180.0  cosfa=np.cos(t0-asp)
  M=cv2.getRotationMatrix2D((imax/2.0,jmax/2.0),tt,1)
  xmax=int(1.6*imax)
  ymax=int(1.6*jmax)  M[0,2]=M[0,2]+0.3*imax
  M[1,2]=M[1,2]+0.3*jmax
  image = cv2.warpAffine(dem,M,(xmax,ymax))
  #return image
  dview=suihei(image,flag)
  #return dview
  M2=cv2.getRotationMatrix2D((xmax/2.0,ymax/2.0),-tt,1)
  M2[0,2]=M2[0,2]-0.3*imax-1
  M2[1,2]=M2[1,2]-0.3*jmax-1 
  eview = cv2.warpAffine(dview,M2,(imax,jmax))
  if flag < 2: return eview
  eview[eview < 0.0] = 0.0
  hf=np.pi/2-np.arctan(eview)  return coss*np.sin(hf)**2+sins*cosfa*(hf-np.sin(hf)*np.cos(hf))  
