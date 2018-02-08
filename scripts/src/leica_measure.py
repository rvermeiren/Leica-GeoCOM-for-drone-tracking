#!/usr/bin/env python
# ===========================================================================
#
# Leica - ROS
# This is a bridge for spherical measurements with the Leica Totalstation.
# Spherical measurements allow to take advantage of the fast angular
# measurements. With this node angular measurements will be published with
# about 20Hz and a radial distance with about 7Hz
#
# ===========================================================================
import sys
import time
import GeoCom_mod
from optparse import OptionParser
from math import sin,cos
global first, z_offset
first=True
z_offset = 0

def measure():
  try:
    # GeoCom get simple measurements
    [error, RC, coord] = GeoCom_mod.TMC_GetSimpleMea(5, 1)

    # get angles and distance
    phi = -float(coord[0])
    theta = float(coord[1])
    radius = float(coord[2])

    # compute carthesian coordinates
    x = sin(theta) * cos(phi) * radius
    y = sin(theta) * sin(phi) * radius
    z = cos(theta) * radius

    global first, z_offset
    if first :
      first = False
      z_offset = round(z,4)
    return (round(x,4), round(y,4), round(z-z_offset,4))

    # We do not want the program to crash if the above code causes an error.
    # Possible causes are:
    # - Mistake in line read from serial port due to high request rate
    # - Loss of prism resulting in unexpected return values
    # - ...
  except ValueError:
    print "Non numeric value recieved!"
    return 0
  except:
    print "No measurement or drop."
    # Short break in case the problem was related to the serial connection.
    time.sleep(1)
    # Then restart the measurement
    GeoCom_mod.TMC_DoMeasure()
    if options.verbose:
      print "Restarted measurements"
    return 0

# Handling options
usage = "usage: python27 leica_measure.py [options]"
parser = OptionParser(usage=usage)
parser.set_defaults( big_prism=False, port="/dev/ttyUSB0", verbose=False)
#coordinit=False, carthesian=False,
#parser.add_option("-i", "--init", action="store_true", dest="coordinit", help="initialize the x-axis")
#parser.add_option("-c", "--carth", action="store_true", dest="carthesian", help="activate publishing of carthesian coordinates")
parser.add_option("-b", "--big", action="store_true", dest="big_prism", help="set the big prism as prism type [default: mini prism]")
parser.add_option("-p", "--port", action="store", type="string", dest="port", help="specify used port [default: %default]")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="print more information")
(options, args) = parser.parse_args()


if options.verbose:
  print "Initializing Leica TS"

# open serial connection on windows port are between 0 and 3 for COM1 to COM4
if GeoCom_mod.COM_OpenConnection(int(options.port), 115200)[0]:
  sys.exit("Can not open Port... exiting")

# set prisem type
prism_type = 7
if options.big_prism:
  prism_type = 3;
  if options.verbose:
    print "Using the big prism"
GeoCom_mod.BAP_SetPrismType(prism_type)

# turn the station in lock mode for prism and set edm mode
# for fast reapeated measurements
GeoCom_mod.AUT_LockIn()
GeoCom_mod.TMC_SetEdmMode(9)
# do a first measure for calibration
GeoCom_mod.TMC_DoMeasure()

time.sleep(1)
if options.verbose:
  print "Leica TS is set up"

GeoCom_mod.TMC_SetOrientation()

with open("out.txt", "w") as file:
  print "Publishing spherical and carthesian coordinates"
  try :
    i = 0
    while True:#not rospy.is_shutdown():
      m = measure()
      print(m)
      file.write(str(i)+"   "+str(m))
      i+=1
  except KeyboardInterrupt :
    print 'interupted'

# closing serial connection, when execution is stopped
GeoCom_mod.COM_CloseConnection()
