# Development of a guidance and automatic positioning system for builder drones with a total station

## Credit

Authors : [Nicolas Sorensen](@nicolassorensen) & [Rémy Vermeiren](@rvermeiren)

Promotor : [Pierre Latteur](https://uclouvain.be/fr/repertoires/pierre.latteur) & [Ramin Sadre](https://uclouvain.be/fr/repertoires/ramin.sadre)

Assistant : [Sebastien Goessens](https://uclouvain.be/fr/repertoires/sebastien.goessens)

### Repository :

Based on the work of [Maxim Artyom](@art-mx) on this [repository](https://github.com/art-mx/leica_ros_sph)

[Trello](https://trello.com/b/cHMLdS54/m%C3%A9moire)

[Slack](https://tfebuildingwithdrones.slack.com/)

### Resources

[Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

[Python documentation convention](https://www.python.org/dev/peps/pep-0258/)

## Requirements
- Windows 10
- Leica cable GEV267
- Total station with GeoCom support
- [python27](https://www.python.org/download/releases/2.7/)
- [pyserial](https://pypi.python.org/pypi/pyserial/2.7)

## Run
```
$ python27.exe leica_track.py
-d (verbose)
-b (big prism -- default = mini-prism)
-p "#port" (on windows if port is COM4, number is 3)

```
## Usage
Use ```-h``` to show usage
```
  Options:
  -h,           --help            show this help message and exit
  -p PORT,      --port=PORT       specify used port [default: /dev/ttyUSB0]
  -b BAUDRATE,  --baudrate=BAUDRATE
                                  specify used baudrate [default: 115200]
  -d, --debug                     show debug information
  ```
