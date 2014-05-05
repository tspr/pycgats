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
cdwpath= '/Users/tspr/Desktop/LabPlot'
h5filename = "./Farben.h5"
tvals_in = "CMYK_M"

import locale
locale.setlocale(locale.LC_ALL, 'de_DE')

from tables import *
from colormath.color_objects import LabColor
from mpl_toolkits.mplot3d import *
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from scipy import interpolate
from scipy.stats import lognorm

# import seaborn as sns
# sns.set(style="whitegrid")

def abL_2_sRGB(a_val,b_val,L_val):
    intermediatecolor = LabColor(lab_l=L_val,lab_a=a_val,lab_b=b_val).convert_to('rgb') 
    normtuple = (float(intermediatecolor.rgb_r)/256,float(intermediatecolor.rgb_g)/256,float(intermediatecolor.rgb_b)/256)
    return normtuple

class CGATScolors(IsDescription):
    SAMPLE_ID = StringCol(32)
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

cmpos=0.80
crossmark=ax.scatter3D(a_pchip(cmpos),b_pchip(cmpos),L_pchip(cmpos),marker='+',c=abL_2_sRGB(a_pchip(cmpos),b_pchip(cmpos),L_pchip(cmpos)),s=200, linewidth=1)


# show the thing
fig.show()


# create 100 nomrally distributed points along the line around cmpos.
# range should be 95% within +-5% of range of t-values (2 sigma)
# scale= sigma. so sigma = 5 (percent) * range / 2(sides)*2(sigma)*100(percent)
scale=(5*(linerange.max()-linerange.min())/400)
zufallspositionen = np.random.normal(loc=cmpos,scale=scale,size=1000)
rnd_a = a_pchip(zufallspositionen)
rnd_b = b_pchip(zufallspositionen)
rnd_L = L_pchip(zufallspositionen)

# add some noise (size: Lab units)
noise_size = 0.1
rnd_a += np.random.normal(0,noise_size,1000)
rnd_b += np.random.normal(0,noise_size,1000)
rnd_L += np.random.normal(0,noise_size,1000)

cntr_a = a_pchip(cmpos)
cntr_b = b_pchip(cmpos)
cntr_L = L_pchip(cmpos)

delta_a = cntr_a - rnd_a
delta_b = cntr_b - rnd_b
delta_L = cntr_L - rnd_L

delta_E = sqrt(square(delta_a) +square(delta_b) + square(delta_L))


# plot them green
rndplt=ax.scatter3D(rnd_a,rnd_b,rnd_L,marker='*',c='green',s=50,linewidth=1)

# histogramm delta E

plt.figure()

n, bins, patches = plt.hist(delta_E,bins=50,color='blue',normed=True,histtype='bar')
lnrm_shape, lnrm_loc, lnrm_scale = lognorm.fit(delta_E)

x= np.linspace(0, delta_E.max(), num=400)
y = lognorm.pdf(x,lnrm_shape,loc=lnrm_loc,scale=lnrm_scale)

pdflne=plt.plot(x,y,'r--',linewidth=2)

