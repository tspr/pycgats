#!/usr/bin/python
# coding=UTF-8



###  create 3D-Plot of color patches.
###  Assumes: List of Patches for measured values of Inking curve.
###  
###   To do the plot correctly:
###  0. set up tval: use one of CMYK_C...CMYK_K
###  1. get list of Points
###  2. convert Lab colors to sRGB
###  3. Plot small- sized Points
###  4. Plot Uncertainty-sized spheres (Rings of dE)
###  5. Generate Spline Fit (enumerate SampleID as time variable in spline fit)
###  6. Plot Spline

####  SETUP HERE
h5filename = "./Farben.h5"
tvals_in = "CMYK_M"

import locale
locale.setlocale(locale.LC_ALL, 'de_DE')

from tables import *
from colormath.color_objects import LabColor
from mpl_toolkits.mplot3d import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

def abL_2_sRGB(a_val,b_val,L_val):
    intermediatecolor = LabColor(lab_l=L_val,lab_a=a_val,lab_b=b_val).convert_to('rgb', RGB_target='sRGB') 
    normtuple = (float(intermediatecolor.rgb_r)/256,float(intermediatecolor.rgb_g)/256,float(intermediatecolor.rgb_b)/256)
    return normtuple

class CGATScolors(IsDescription):
    SamplID = StringCol(32)
    SAMPLE_NAME = StringCol(32)
    CMYK_C = FloatCol()
    CMYK_M = FloatCol()
    CMYK_Y = FloatCol()
    CMYK_K = FloatCol()
    LAB_L = FloatCol()
    LAB_A = FloatCol()
    LAB_B = FloatCol()



h5file = openFile(h5filename, mode = "r")
table=h5file.getNode('/Tabellen/Patches')

# Convert Lab  to rgb for plotting and append to data points
# make sure, your installation of matplotlib is patched according to:
# https://github.com/login?return_to=%2Fmatplotlib%2Fmatplotlib%2Fissues%2F1692

colours=[]
tvals=[]
avals=[]
bvals=[]
Lvals=[]


for row in table[:]:
    
    colours.append(abL_2_sRGB(a_val=row['LAB_A'],b_val=row['LAB_B'],L_val=row['LAB_L']))
    tvals.append(row[tvals_in]/100)
    avals.append(row['LAB_A'])
    bvals.append(row['LAB_B'])
    Lvals.append(row['LAB_L'])

h5file.close()


# Create Interpolation functions for a,b,L
a_pchip=interpolate.pchip(tvals,avals)
b_pchip=interpolate.pchip(tvals,bvals)
L_pchip=interpolate.pchip(tvals,Lvals)

pch_Inter=[a_pchip,b_pchip,L_pchip]




# Start plotting
# Disable depth shading
plt.ion()
art3d.zalpha = lambda *args:args[0]


# Setup canvas
fig = plt.figure()
ax = fig.gca(projection='3d')

ax.set_xlabel('a')
ax.set_ylabel('b')
ax.set_zlabel('L')
ax.set_xlim(-100,100)
ax.set_ylim(-100,100)
ax.set_zlim(0,100)


# plot the grey axis
gx=np.linspace(0,0,101)
gy=np.linspace(0,0,101)
gz=np.linspace(0,100,101)
gaxis=ax.plot(gx,gy,gz,c=(0,0,0))

# plot the points
#pointsplot=ax.scatter3D(table.cols.LAB_A[:],table.cols.LAB_B[:],table.cols.LAB_L[:],s=20,c=colours,linewidth=0)#
pointsplot=ax.scatter3D(avals,bvals,Lvals,s=20,c=colours,linewidth=0)
# maybe plot some cross marks as well
#q=ax.scatter3D(table.cols.LAB_A[:],table.cols.LAB_B[:],table.cols.LAB_L[:], s=100,c=(0,0,0), norm=None, marker='+', linewidth=1,alpha=0.5)

# plot the Interpolated Path
linerange = np.arange(np.amin(tvals),np.amax(tvals),0.01)
interline=ax.plot(a_pchip(linerange),b_pchip(linerange),L_pchip(linerange),c=(0,0,0),linewidth=1)

cmpos=0.15
crossmark=ax.scatter3D(a_pchip(cmpos),b_pchip(cmpos),L_pchip(cmpos),marker='+',c=abL_2_sRGB(a_pchip(cmpos),b_pchip(cmpos),L_pchip(cmpos)),s=200)


# show the thing
fig.show()
