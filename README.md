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

# How it works (this may only work for HP scanners)

1. Get the IP address of your scanner hardware

2. run >scan2PDF.py -id xxx.xxx.xxx.xxx

This will automatically generate the correct URI for your HP scanner. 

3. You only need to do steps 1 and 2 the first time.   Your scanner URI is stored in 
your home directory: .scannerURI

4. For a non-HP scanner if you no the correct URI you could edit it into ~/.scannerURI (not tested). 

