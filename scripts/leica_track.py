#!/usr/bin/env python

import sys
import time
import math
import GeoCom_mod
from math import sin,cos
from optparse import OptionParser
from operator import neg

def searchPrism(Hz, V):
    print("Searching for the prism ...")
    if GeoCom_mod.AUT_Search(math.radians(Hz),math.radians(V))[1] == 0:
        [error, RC, parameters] = GeoCom_mod.AUT_FineAdjust(math.radians(Hz/2),math.radians(V/2))
        if RC != 0:
            GeoCom_mod.COM_CloseConnection()
            sys.exit("Can not found prism... exiting")
        else :
            print ("Prism found")
    [error, RC, coord] =GeoCom_mod.AUT_LockIn()
    if RC == 0:
        print("Prism locked")
    else :
        print("Locked fail")
        print(str(RC))
        print(str(error))

def usage():
    # Handling options
    usage = "usage: rosrun leica_interface %prog [options]"
    parser = OptionParser(usage=usage)
    parser.set_defaults(port="/dev/ttyUSB0",baudrate=115200, debug=False)
    parser.add_option("-p", "--port", action="store", type="string", dest="port", help="specify used port [default: %default]")
    parser.add_option("-b", "--baudrate", action="store", type="int", dest="baudrate", help="specify used baudrate [default: %default]")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="print debug information")
    (options, args) = parser.parse_args()
    return options

def connection(options):
    if GeoCom_mod.COM_OpenConnection(int(options.port), options.baudrate )[0]:
        sys.exit("Can not open Port... exiting")

    GeoCom_mod.EDM_Laserpointer(1)
    raw_input('Put the laser on x axis and press <enter>')

    GeoCom_mod.TMC_SetOrientation()
    print("Carthesian coordinates system set, station is 000 and laser directed on x axis")

    prism_type = 7
    GeoCom_mod.BAP_SetPrismType(prism_type)

    raw_input(' Direct the station to the prism and press <enter>')
    GeoCom_mod.EDM_Laserpointer(0)

    searchPrism(20,10)

    GeoCom_mod.TMC_SetEdmMode(9) #EDM_CONT_FAST = 9, // Fast repeated measurement (geocom manual p.91)
    GeoCom_mod.TMC_DoMeasure()
    time.sleep(2)
    print "Leica is set up"

def compute_carthesian(coord):
    phi = -float(coord[0])
    theta = float(coord[1])
    radius = float(coord[2])

    # compute carthesian coordinates
    point_x = round(sin(theta) * cos(phi) * radius,4)
    point_y = round(sin(theta) * sin(phi) * radius,4)
    point_z = round(cos(theta) * radius,4)
    print ('x('+str(point_x)+') y('+str(point_y)+') z('+str(point_z)+')')
    with open("msg.txt", "a") as file:
        file.write(str(point_x)+","+str(point_y)+","+str(point_z)+"\n")


def get_measure(options):
    old_coord = [0,0,0]
    try:
        # GeoCom get simple measurements
        [error, RC, coord] = GeoCom_mod.TMC_GetSimpleMea(5, 1)

        if options.debug: print( 'Error: '+ str(error) )
        if options.debug: print( 'Return Code: '+ str(RC) )

        if RC==0:
            compute_carthesian(coord)
            old_coord = coord

        elif RC==1284:
            print( 'Accuracy could not be guaranteed \n' )
            compute_carthesian(old_coord)

        elif RC==1285:
            print('No valid distance measurement! \n')

        else:
            print( '\n'+'ERROR, Return code: '+str(RC)+'\n')

    except ValueError:
        print( "Non numeric value recieved!" )

    except GeoCom_mod.SerialRequestError as e :
        print(e)

################################################################################
################################### MAIN #######################################
################################################################################

options = usage()
connection(options)
try :
    i = 0
    while True:
        i+=1
        get_measure(options)
except KeyboardInterrupt :
    #GeoCom_mod.AUS_SetUserLockState(0)
    GeoCom_mod.TMC_SetEdmMode(0)
    GeoCom_mod.COM_CloseConnection()
    sys.exit("KeyboardInterrupt")

# Closing serial connection, when execution is stopped
GeoCom_mod.TMC_SetEdmMode(0)
GeoCom_mod.COM_CloseConnection()
