# Development of a guidance and automatic positioning system for builder drones with a total station

## Credit

Authors : [Nicolas Sorensen](https://github.com/nicolassorensen/) & [Rémy Vermeiren](https://github.com/rvermeiren/)

Promotors : [Pierre Latteur](https://uclouvain.be/fr/repertoires/pierre.latteur) & [Ramin Sadre](https://uclouvain.be/fr/repertoires/ramin.sadre)

Assistant : [Sebastien Goessens](https://uclouvain.be/fr/repertoires/sebastien.goessens)

### Repository :

Based on the work of [Maxim Artyom](https://github.com/art-mx/leica_ros_sph) and [Georg Wiedebach](https://github.com/georgwi/leica_ros_sph)

[Trello](https://trello.com/b/cHMLdS54/m%C3%A9moire) and [Slack](https://tfebuildingwithdrones.slack.com/)

### Resources

[Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

[Python documentation convention](https://www.python.org/dev/peps/pep-0258/)

### Documentation

The documentation generation is automated using [Sphinx](http://www.sphinx-doc.org/en/master/).
The scripts generating the documentation for ```alx_track.py``` and ```GeoCom.py``` are available in the folder ```scripts\source```.  
To generate it on a Windows system : see ```scripts\make.bat```.  
To generate it on a Unix system:

* Open a terminal
* Go into the ```scripts```folder
* Type ```make html``` to generate it in HTML
* Type ```make latexpdf``` to generate a PDF

Further information is available in ```scripts\Makefile```.

## Installation
### Requirements
* Windows 10
* Leica cable GEV267 for Total station TCRP1203
* Leica cable GEV269 for Total station MS50, MS60
* Total station with GeoCom support (TCRP1203, MS50, MS60)
* [Python2.7](https://www.python.org/download/releases/2.7/)
* pip package manager for Python 2.7 (normally already included in Python installation)
* [pyserial](https://pypi.python.org/pypi/pyserial/2.7)
    *  Install with ```C\:Python27\python.exe -m pip install pyserial ``` in the command line
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
    * After this process, it's possible you need to redo this with the new device showed in the list called "Serial USB Converter"

### Get the source codes

You can download the code on this repository:
https://github.com/rvermeiren/Leica-GeoCOM-for-drone-tracking
If the link is dead, contact [Nicolas Sorensen](https://github.com/nicolassorensen/) or [Rémy Vermeiren](https://github.com/rvermeiren/)

##Run and Usage
### Run
```
$ C:\Python27\python.exe alx_track.py
-d (verbose for debug)
-b (big prism -- default = mini-prism)
-p "port" (ex: "COM1" -- This can be found in "Device Manager" on Windows)

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
  -B, --Big                       use 360 big prism
  ```
## Licenses

The original work was under the following copyright :

```
#Copyright (c) 2013, Marcel Schoch, ASL, ETH Zurich, Switzerland
#You can contact the author at <slynen at ethz dot ch>
#
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
#notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#notice, this list of conditions and the following disclaimer in the
#documentation and/or other materials provided with the distribution.
# * Neither the name of ETHZ-ASL nor the
#names of its contributors may be used to endorse or promote products
#derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL ETHZ-ASL BE LIABLE FOR ANY
#DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
