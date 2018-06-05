#!/usr/bin/env python
"""
.. module:: track_without_ps

"""

import sys
sys.path.append(r"C:\Python27\Lib")
# sys.path.append(r"C:\Python27\Lib\site-packages")
sys.path.append(r"src")
import time
import math
import GeoCom
from math import sin,cos
from optparse import OptionParser
from operator import neg
import os


reload(sys)
sys.setdefaultencoding('utf8')
OLD_COORD=[0,0,0]
FAIL_COUNT=0
DEBUG=False


def searchPrism(Hz = 20 , V=20):
    """
    Search for the prism in the given area.

    :param Hz: horizontal area in degrees
    :type Hz: int
    :param V: vertical area in degrees
    :type V: int
    :returns: True if the prism is locked, False otherwise
    :rtype: bool

    """
    print("Searching for the prism ...")
    if GeoCom.AUT_Search(math.radians(Hz),math.radians(V))[1] == 0:
        [error, RC, parameters] = GeoCom.AUT_FineAdjust(math.radians(Hz/2),math.radians(V/2))
        if RC != 0:
            os.system('color 0F')
            GeoCom.COM_CloseConnection()
            sys.exit("Can not found prism... exiting")
        # else :
    print ("Prism found")
    [error, RC, coord] = GeoCom.AUT_LockIn()
    if RC == 0:
        print("Prism locked")
        return True
    else :
        print("Locked fail")
        os.system('color 0F')
        print(str(RC))
        print(str(error))
        sys.exit("Can not lock prism... exiting")
        return False

def usage(COM ="COM3", baud = 57600):
    """
    Define and show usage of the script.

    :param COM: number of the COM port to which the USB cable is connected.
    :type COM: str
    :param baud: baud rate of the communication between the PC and the total station.
    :type baud: int

    A higher baud rate will allow more measurements per second but may cause problems (e.g. lack of precision),
    while a lower one will make less measurements per second but they will be more reliable.

    .. warning::

    	The baud rate HAS to be the same as the one set on the total station! Otherwise the script won't work correctly.

    :returns: list of values set for the options, or default values
    :rtype: Namespace object
    """
    global DEBUG
    usage = "usage: C\:Python27\python.exe %prog [options]"
    parser = OptionParser(usage=usage)
    parser.set_defaults(port=COM,baudrate=baud, debug=False, big_prism=False)
    parser.add_option("-p", "--port", action="store", type="string", dest="port", help="specify used port [default: %default]")
    parser.add_option("-b", "--baudrate", action="store", type="int", dest="baudrate", help="specify used baudrate [default: %default]")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="print debug information")
    parser.add_option("-B", "--Big", action="store_true", dest="big_prism", help="set the big prism as prism type [default: mini prism]")
    (options, args) = parser.parse_args()
    if options.debug : DEBUG = True
    return options

def connection(options):
    """
    | Opens a serial connection between the computer and the total station.
    | Calls **sys.exit** if the connection set up failed.

    :param options: contains the options to configure the connection
    :type options: Namespace
    """
    if GeoCom.COM_OpenConnection(options.port, options.baudrate )[0]:
        os.system('color 0F')
        sys.exit("Can not open Port... exiting")

def set_x_axis():
    """
    Set the orientation of the carthesian plan by fixing **x** axis.
    """
    [error, RC, args] = GeoCom.TMC_SetOrientation()
    print("Carthesian coordinates system set, station is 000 and laser directed on x axis")

def set_prism_type(big_prism):
    """
    Set the prism type as "360 big prism" if *big_prism* is True, or to "360 small prism" if False.

    :param big_prism: Determines if the type of prism if "big" or "small"
    :type big_prism: bool
    """
    if big_prism:
        prism_type = 3 #big 360 prism
    else:
        prism_type = 7 #small 360 prism
    [error, RC, args] = GeoCom.BAP_SetPrismType(prism_type)

def set_laser(value):
    """
    Turn on/off the laser of the total station.

    :param value: on (value=1) or off (value=0)
    :type value: int
    """
    [error, RC, args] = GeoCom.EDM_Laserpointer(value)

def setup_station_manual(options):
    """
    Set up the station for the purpose of tracking a prism and make fast reapeated measurements.

    :param options: contains the options to configure the station
    :type options: Namespace
    :returns: True if the setup succeeded, False otherwise
    :rtype: bool
    """

    set_laser(1)
    raw_input('Put the laser on x axis and press <enter>')
    set_x_axis()
    set_prism_type(options.big_prism)
    raw_input('Direct the station to the prism and press <enter>')
    set_laser(0)
    searchPrism(40,20)

    GeoCom.TMC_SetEdmMode(9) #EDM_CONT_FAST = 9, // Fast repeated measurement (geocom manual p.91)
    GeoCom.TMC_DoMeasure()
    time.sleep(1)
    print("Station is set up")

def setup_station(options):
    print("Script starting ...")
    set_laser(1)
    time.sleep(5)
    set_x_axis()
    set_prism_type(options.big_prism)
    set_laser(0)
    searchPrism(40,20)
    time.sleep(1)

    GeoCom.TMC_SetEdmMode(9) #EDM_CONT_FAST = 9, // Fast repeated measurement (geocom manual p.91)
    GeoCom.TMC_DoMeasure()
    time.sleep(1)
    print("Station is set up")

def compute_carthesian(phi,theta,radius):
    """
    Compute carthesian coordinates using vertical, horizontal angles and distance measurements.

    :param phi: horizontal angle (rad)
    :type phi: float
    :param theta: vertical angle (rad)
    :type theta: float
    :param radius: distance from the station to the prism (m)
    :type radius: float

    :returns: a string with the coordinates, formatted as x;y;z
    :rtype: str
    """
    point_x = round(sin(theta) * cos(phi) * radius,4)
    point_y = round(sin(theta) * sin(phi) * radius,4)
    point_z = round(cos(theta) * radius,4)

    #print the coordinates
    # print ('x('+str(point_x)+') y('+str(point_y)+') z('+str(point_z)+')')
    return ''+str(point_x)+';'+str(point_y)+';'+str(point_z)+';'

def get_measure():
    """
    Request a complete measurement (angles and distance) to the station
    and handles the possible errors returned by the station.

    After 100 failed distance measurements, run a search to try to lock on the prism again.

    :returns:
    * The coordinates of the prism if :
    	* the measurement was successful (RC=0)
    	* the accuracy coudln't be guaranteed by the system of the station, but a complete measurement was still possible (RC==1284)
    * "2" if only the angles could be measured (RC=1285 or RC=1288)
    * "3" if another error occured or if a non-numeric value was received
    * "4" if a GeoCom.SerialRequestError occured

    :rtype: str
    """
    global OLD_COORD, FAIL_COUNT
    if FAIL_COUNT > 100:
        while not searchPrism():
            time.sleep(10)
        FAIL_COUNT = 0
    try:
        [error, RC, coord] = GeoCom.TMC_GetSimpleMea(150, 1)
        if RC==0:
            os.system('color 2F')
            OLD_COORD = coord
            res = '0;'+ compute_carthesian(-float(coord[0]),float(coord[1]),float(coord[2]))
            FAIL_COUNT = 0
            # print res
            return res
        elif RC==1284:
            os.system('color 06')
            OLD_COORD = coord
            res = '1;'+compute_carthesian(float(coord[0]),float(coord[1]),float(coord[2]))
            print('Accuracy could not be guaranteed \n')
            # FAIL_COUNT+=1
            # print res
            return res
        elif RC==1285 or RC==1288:
            os.system('color 04')
            print('Only angle measurement : '+str(RC))
            res = '2'#+compute_carthesian(float(coord[0]),float(coord[1]),float(OLD_COORD[2]))
            coord = OLD_COORD
            FAIL_COUNT+=1
            # print res
            return res
        else:
            os.system('color 4F')
            print('\n'+'ERROR, Return code: '+str(RC)+'\n')
            FAIL_COUNT+=1
            return "3"
    except ValueError:
        os.system('color 4F')
        print( "Non numeric value recieved!" )
        FAIL_COUNT+=1
        return "3"
    except GeoCom.SerialRequestError as e :
        return "4"

def open(port = "COM3", baud = 57600):
    options = usage(port, baud)
    connection(options)
    setup_station(options)
    return 1

def close():
    os.system('color 0F')
    j=GeoCom.COM_CloseConnection()
    return j[0]


"""#############################################################################
################################### MAIN #######################################
#############################################################################"""

if __name__ == '__main__':
    open("COM4", 57600)
    try :
        while True: #while program not interrupted by the user
            t_start = time.time()
            print get_measure()
            t_end = time.time()
            # print(t_end-t_start)
    except KeyboardInterrupt :
        time.sleep(2)
        os.system('color 0F')
        j=GeoCom.COM_CloseConnection()
        sys.exit("Keyboard Interruption by user")
    # Closing serial connection, when execution is stopped
    os.system('color 0F')
    GeoCom.COM_CloseConnection()
