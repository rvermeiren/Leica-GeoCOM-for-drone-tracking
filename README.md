# Development of a guidance and automatic positioning system for builder drones with a total station

## Credit

Authors : [Nicolas Sorensen](https://github.com/nicolassorensen/) & [Rémy Vermeiren](https://github.com/rvermeiren/)

Promotor : [Pierre Latteur](https://uclouvain.be/fr/repertoires/pierre.latteur) & [Ramin Sadre](https://uclouvain.be/fr/repertoires/ramin.sadre)

Assistant : [Sebastien Goessens](https://uclouvain.be/fr/repertoires/sebastien.goessens)

### Repository :

Based on the work of [Maxim Artyom](https://github.com/art-mx/leica_ros_sph) and [Georg Wiedebach](https://github.com/georgwi/leica_ros_sph)

[Trello](https://trello.com/b/cHMLdS54/m%C3%A9moire)

[Slack](https://tfebuildingwithdrones.slack.com/)

### Resources

[Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

[Python documentation convention](https://www.python.org/dev/peps/pep-0258/)

## Installation
### Requirements
* Windows 10
* Leica cable GEV267 for Total station TCRP1203
* Leica cable GEV267 for Total station MS50, MS60
* Total station with GeoCom support (TCRP1203, MS50, MS60)
* [Python2.7](https://www.python.org/download/releases/2.7/)
* pip package manager for Python 2.7 (normally already include in Python installation)
* [pyserial](https://pypi.python.org/pypi/pyserial/2.7)
    *  Install with ```C\:Python27\python.exe -m pip install pyserial ``` in command line
* USB cable drivers for GEV267,GEV268,GEV269 V3.0 available on Leica MyWorld website
    * Install the driver :
        * Download the driver and extract it
        * Plug-in the cable on the Windows computer
        * Go to "Device Manager"
        * Find the device "FT232R"
        * Right click and select "Update Driver"
        * Browse your computer into the extracted folder
        * Select the folder "Windows XP, Server 2003, Server 2008 R2,Vista, 7, 8"
        * Click on next to finish the installation
    * After this process, it's possible you need to redo this with the new device showed in the list call "Serial USB Converter"

## Get the sources codes

You can download the code on this repository:
https://github.com/rvermeiren/Leica-GeoCOM-for-drone-tracking
If the link is dead, contact [Vermeiren Rémy]() or [Sorensen Nicolas]

##Run and Usage
### Run
```
$ C:\Python27\python.exe alx_track.py
-d (verbose for debug)
-b (big prism -- default = mini-prism)
-p "port" (ex: "COM1" -- This can be found in "Device Manager on Windows")

```
### Usage
Use ```-h``` to show usage
```
  Options:
  -h,           --help            show this help message and exit
  -p PORT,      --port=PORT       specify used port [default: /dev/ttyUSB0]
  -b BAUDRATE,  --baudrate=BAUDRATE
                                  specify used baudrate [default: "COM3"]
  -d, --debug                     show debug information
  -B, --Big                       use big 360 prism
  ```
