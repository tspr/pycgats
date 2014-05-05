#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 20:49:23 2014

@author: tspr
"""
####  SETUP HERE
h5filename = "/Users/tspr/Desktop/spec_convert/Türkis7712-HolmenX60.h5"


import locale
locale.setlocale(locale.LC_ALL, 'de_DE')

from tables import *
from colormath.color_objects import LabColor, SpectralColor
from mpl_toolkits.mplot3d import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

def abL_2_sRGB(a_val,b_val,L_val):
    intermediatecolor = LabColor(lab_l=L_val,lab_a=a_val,lab_b=b_val).convert_to('rgb') 
    normtuple = (float(intermediatecolor.rgb_r)/256,float(intermediatecolor.rgb_g)/256,float(intermediatecolor.rgb_b)/256)
    return normtuple

class CGATScolors(IsDescription):
    SampleID = StringCol(32)
    SAMPLE_NAME = StringCol(32)
    CMYK_C = FloatCol()
    CMYK_M = FloatCol()
    CMYK_Y = FloatCol()
    CMYK_K = FloatCol()
    LAB_L = FloatCol()
    LAB_A = FloatCol()
    LAB_B = FloatCol()
    nm380 = FloatCol()
    nm390 = FloatCol()
    nm400 = FloatCol()
    nm410 = FloatCol()
    nm420 = FloatCol()
    nm430 = FloatCol()
    nm440 = FloatCol()
    nm450 = FloatCol()
    nm460 = FloatCol()
    nm470 = FloatCol()
    nm480 = FloatCol()
    nm490 = FloatCol()
    nm500 = FloatCol()
    nm510 = FloatCol()
    nm520 = FloatCol()
    nm530 = FloatCol()
    nm540 = FloatCol()
    nm550 = FloatCol()
    nm560 = FloatCol()
    nm570 = FloatCol()
    nm580 = FloatCol()
    nm590 = FloatCol()
    nm600 = FloatCol()
    nm610 = FloatCol()
    nm620 = FloatCol()
    nm630 = FloatCol()
    nm640 = FloatCol()
    nm650 = FloatCol()
    nm660 = FloatCol()
    nm670 = FloatCol()
    nm680 = FloatCol()
    nm690 = FloatCol()
    nm700 = FloatCol()
    nm710 = FloatCol()
    nm720 = FloatCol()
    nm730 = FloatCol()


h5file = openFile(h5filename, mode = "r")
tabelle=h5file.getNode('/Tabellen/Patches')

colours=[]

for row in tabelle[:]:
    spc = SpectralColor(observer=2, illuminant='d50', 
                        spec_380nm=row['nm380'], spec_390nm=row['nm390'], spec_400nm=row['nm400'],
                        spec_410nm=row['nm410'], spec_420nm=row['nm420'], spec_430nm=row['nm430'],
                        spec_440nm=row['nm440'], spec_450nm=row['nm450'], spec_460nm=row['nm460'],
                        spec_470nm=row['nm470'], spec_480nm=row['nm480'], spec_490nm=row['nm490'],
                        spec_500nm=row['nm500'], spec_510nm=row['nm510'], spec_520nm=row['nm520'],
                        spec_530nm=row['nm530'], spec_540nm=row['nm540'], spec_550nm=row['nm550'],
                        spec_560nm=row['nm560'], spec_570nm=row['nm570'], spec_580nm=row['nm580'],
                        spec_590nm=row['nm590'], spec_600nm=row['nm600'], spec_610nm=row['nm610'],
                        spec_620nm=row['nm620'], spec_630nm=row['nm630'], spec_640nm=row['nm640'],
                        spec_650nm=row['nm650'], spec_660nm=row['nm660'], spec_670nm=row['nm670'],
                        spec_680nm=row['nm680'], spec_690nm=row['nm690'], spec_700nm=row['nm700'],
                        spec_710nm=row['nm710'], spec_720nm=row['nm720'], spec_730nm=row['nm730'])
    colours.append(spc)
    print spc.convert_to('lab')

