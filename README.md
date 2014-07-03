keyfucker
=========

A simple GNU/Linux Keylogger 


Files
-----
```
keyfucker.py  - Main file that catch all keys and take screenshots (optionally) 
keylist.py    - Map key codes (only US keyboards layout).
```

Dependences
-----------
```
Python 2.x and Imagemagick, evdev modules
For Ubuntu the dependences installs automatically running "sudo ./keyfucker.py"
```

Usage
-----
```
Run the script with:
"sudo ./keyfucker.py" or "python keyfucker.py" for basic usage
"sudo ./keyfucker.py -s 10" the script will take screenshots every 10 seconds
All captured information will be saved to "data" folder
```
