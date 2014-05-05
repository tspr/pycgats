#!/usr/bin/python
# coding=UTF-8
## Bastelkiste für Enthought ipython !

## CGATS /txt (Dappige Version - CGATS.17) importieren und in eine h5-Datenbank speichern
###  Assumes: CGATSfile contains only measurements from one color of inking curve.

# cd /Users/tspr/Desktop/LabPlot

import locale
locale.setlocale(locale.LC_ALL, 'de_DE')

from tables import *

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
    
### Dateinamen hier setzen.
    
    
h5filename = "/Users/tspr/Desktop/spec_convert/Türkis7712-HolmenX60.h5"
cgatsfilename = "/Users/tspr/Desktop/spec_convert/Türkis7712-HolmenX60.txt"



h5file = openFile(h5filename, mode = "w", title = "Farbdaten")
group = h5file.createGroup("/", "Tabellen", "Gruppe_Tabellen")
table = h5file.createTable(group, "Patches", CGATScolors, "Patches_")

Zeile = table.row

lineary = []

cgatsfile = open(cgatsfilename, 'rU')
for line in cgatsfile.xreadlines():
    lineary.append(line.strip().split('\t'))
cgatsfile.close()

for i in range(len(lineary)):
    if(lineary[i][0]=='BEGIN_DATA_FORMAT'):
        def_idx=i+1
    if(lineary[i][0]=='BEGIN_DATA'):
        first_data=i+1
    if(lineary[i][0]=='END_DATA'):
        last_data=i
    


for idx in range(first_data,last_data):
    for name, data in zip(lineary[def_idx], lineary[idx]):
        if name in ['SampleID', 'SAMPLE_NAME']:
            Zeile[name]=data

        elif name in ['LAB_L', 'LAB_A', 'LAB_B']:
            Zeile[name]=locale.atof(data)
        
        elif name in ['nm380',
                         'nm390',    'nm400',    'nm410',    'nm420',    'nm430',    'nm440',    'nm450',
                         'nm460',    'nm470',    'nm480',    'nm490',    'nm500',    'nm510',    'nm520',
                         'nm530',    'nm540',    'nm550',    'nm560',    'nm570',    'nm580',    'nm590',
                         'nm600',    'nm610',    'nm620',    'nm630',    'nm640',    'nm650',    'nm660',
                         'nm670',    'nm680',    'nm690',    'nm700',    'nm710',    'nm720',    'nm730']:
            Zeile[name]=locale.atof(data)
#==============================================================================
# # nun über die Zeile lineary[def_idx] drüber. Wenn in der Indexzeile SPECTRAL_NM drin, dann ist es ein a***file.
#==============================================================================
           
    colidx=0
    while colidx < len(lineary[def_idx]):
        if lineary[def_idx][colidx] == "SPECTRAL_NM":
            nmidx='nm'+lineary[idx][colidx]
            print nmidx
            Zeile[nmidx]=locale.atof(lineary[idx][colidx+1])
            colidx = colidx + 2
        else:
            colidx = colidx + 1

        
    Zeile.append()

table.flush()
h5file.close()



