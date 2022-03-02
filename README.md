## scan2PDF
# quick and easy command line scanner tool using python3-sane

```

 usage: >python3 scan2PDF.py [options] outfile_root_name 
   Options:
     -f -F -Flatbed -flatbed    (ADF is default)
     -bw -Mono                  (Grey level scan: Color is default)
     -Options                   List device Options
     -Devices                   List available Scanners
     -Help                      this!
```

# Setup

 1. run `> python3 scan2PDF.py -Devices`  which lists available scanners  (this takes a minute).
 
 2. copy the whole tuple for the device you want into line 64.  For example:
 
 `sc_dev = ('escl:https://192.168.0.56:443', 'HP', 'OfficeJet Pro 9010 series [5F68CC] SSL', 'platen,adf scanner')'`

 3. Usage Examples:
    * `> scan2PDF.py   filename          // scan all pages in ADF into filename.pdf in color`
    * `> scan2PDF.py   -F -bw file2     // scan the flatbed into a grayscale image  file2.pdf`
    
    
