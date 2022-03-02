#!/usr/bin/env python3

from __future__ import print_function
import sane
import time
import os, sys
#from PIL import Image

#
# Change these for 16bit / grayscale scans
#
depth = 8
mode = 'color'

#
# Initialize sane
#
ver = sane.init()
print('SANE version:', ver)


if len(sys.argv) != 2:
    print('scan2PDF:\n usage: >python3 scan2PDF outfile_root_name ')
    quit()
    
INFO_ONLY = False
OPTIONS_ONLY = False
outfile_root_name = sys.argv[1]

if outfile_root_name == "-info":
    INFO_ONLY = True
if outfile_root_name == '-options':
    OPTIONS_ONLY = True

# negative np means scan everything in ADF
np = -1  # until issue is fixed, just scan all pages in ADF 


# the device is always the same in my office:  

sc_dev = ('escl:https://192.168.0.56:443', 'HP', 'OfficeJet Pro 9010 series [5F68CC] SSL', 'platen,adf scanner')


if INFO_ONLY:
    #
    # Get devices
    #
    print('Scanning for scanners(!) ... please be patient')
    devices = sane.get_devices()
    print('Available devices:', devices)
    for i,d in enumerate(devices):
        print ('Device ',i)
        print (d)
        print ('\n\n')

    print('Using: ', sc_dev)
    quit()
    
    
'''
22-Jan
Available devices: [('escl:https://192.168.0.56:443', 'HP', 'OfficeJet Pro 9010 series [5F68CC] SSL', 'platen,adf scanner'), ('hpaio:/net/hp_officejet_pro_9010_series?ip=192.168.0.56&queue=false', 'Hewlett-Packard', 'hp_officejet_pro_9010_series', 'all-in-one')]
Device  0
('escl:https://192.168.0.56:443', 'HP', 'OfficeJet Pro 9010 series [5F68CC] SSL', 'platen,adf scanner')

Device  1
('hpaio:/net/hp_officejet_pro_9010_series?ip=192.168.0.56&queue=false', 'Hewlett-Packard', 'hp_officejet_pro_9010_series', 'all-in-one')

'''

#
# Open scanner
#
print('Opening Scanner:'+sc_dev[2])
DEV_OPEN = False
try:
    dev = sane.open(sc_dev[0])
    DEV_OPEN = True
except:
    print("Couldn't open scanner ", sc_dev[1])
    quit()
#
# Get or Set some options
#
params = dev.get_parameters()
if OPTIONS_ONLY:
    print('Scanning options:')
    print(dev.optlist)
    print('Scanning options2:')
    OL = dev.get_options()
    for o in OL:
        print(o)
    quit()

#
#  Set standard options 
#
try:
    dev.depth = 8
    dev.mode = 'Color'
    dev.source = [ 'ADF','Flatbed'][0]
    dev.resolution = 200
except:
    print('problem setting Scanner Options: try >scan2PDF -options')
    quit()

#  Not sure what should be correct values!!!
#params = dev.get_parameters()
#print('\n\nDevice parameters:', params)
#quit()
 
#
# perform scans and get a PIL.Image object
#
print('\n\n Starting {:}-page scan from {:}'.format(np, dev.source))
page_series = []
adf_iter = sane._SaneIterator(dev)
#adf_iter = dev.multi_scan()

p = 1 # page counter
while True:
    if np > 0 and p > np:  # we're done (even if docs are still in ADF)
        break    
    pg_num000 = str(p).zfill(3)
    print('  Starting Scan'+pg_num000)
    try:
        im = adf_iter.__next__()
        #im = dev.snap()
    except:
        print('      scan2PDF.py: Scan failed or finished')
        DEV_OPEN = False
        break
    print('  Scan {:} Completed'.format(p))
    fn = '{:}Page{:}.png'.format(outfile_root_name, pg_num000)
    page_series.append(fn)
    im.save(fn)
    p+=1
#
# Close the device
#

if DEV_OPEN:
    dev.close()

##  Convert the pages to PDF and combine them
if len(page_series) > 0:
    pass    # no need to convert
else:
    print('No pages were scanned')
    
print('Scan-2-PDF Job completed')

