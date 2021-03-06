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

def help():
    print('scan2PDF:\n usage: >python3 scan2PDF [options] outfile_root_name ')
    print('   Options:')
    print('     -f -F -Flatbed -flatbed    (ADF is default)')
    print('     -bw -Mono                  (Grey level scan: Color is default)')
    print('     -Options                   List device Options')
    print('     -Devices                   List available Scanners')
    print('     -Help                      this!')
#
# Initialize sane
#
ver = sane.init()
print('SANE version:', ver)

nargs = len(sys.argv)
if nargs < 2 or nargs > 3:
    help()
    quit()
    
INFO_ONLY = False
OPTIONS_ONLY = False
outfile_root_name = sys.argv[nargs-1] # last arg is file name root
DocSource = 0  # ADF
ColorBW_Mode = 'Color'
 
# if an option it is arg[1]
argval = sys.argv[1].lower().strip()
print(' I got option: [{:}]'.format(argval))

if argval[0] == '-':
    if argval in ['-bw','-mono']:
        ColorBW_Mode = 'Gray'
    elif argval in ['-f','-flatbed']:
        DocSource = 1
    elif argval == '-options':
        OPTIONS_ONLY = True
    elif argval == '-devices':
        INFO_ONLY = True
    else:
        print('Unknown option X',sys.argv[1],' ... quitting')
        help()
        quit()

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
    dev.mode = ColorBW_Mode
    dev.source = [ 'ADF','Flatbed'][DocSource]
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
print('\n\n Starting {:} scan from {:}'.format(ColorBW_Mode, dev.source))
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
        print('      scan2PDF.py: Scan Complete')
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
    print('Converting/merging pages ...')
    # convert to PDF 
    cat_cmd = 'pdftk '
    for pn in page_series:
        conv_cmd = 'convert {:} {:}'.format(pn,pn.replace('.png','.pdf'))
        #print('Convert cmd: ', conv_cmd)
        os.system(conv_cmd)
        cat_cmd += ' '+pn.replace('.png','.pdf')
    cat_cmd += ' cat output ' + outfile_root_name+'.pdf'
    #print('executing: [{:}]'.format(cat_cmd))
    os.system(cat_cmd)
    # remove single page files
    os.system('rm {:}Page*'.format(outfile_root_name))
else:
    print('No pages were scanned')
    
print('Scan-2-PDF Job completed')

