#!/usr/bin/env python

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


reload(sys)
sys.setdefaultencoding('utf8')
OLD_COORD=[0,0,0]
DEBUG=False


def searchPrism(Hz, V):
    """Search for the prism in the given area
        IN integer Hz : horizontale area in degree
        IN integer V : vertical area in degree
        OUT boolean : true if the prism is locked
    """
    print("Searching for the prism ...")
    if GeoCom.AUT_Search(math.radians(Hz),math.radians(V))[1] == 0:
        [error, RC, parameters] = GeoCom.AUT_FineAdjust(math.radians(Hz/2),math.radians(V/2))
        if RC != 0:
            GeoCom.COM_CloseConnection()
            sys.exit("Can not found prism... exiting")
        else :
            print ("Prism found")
    [error, RC, coord] = GeoCom.AUT_LockIn()
    if RC == 0:
        print("Prism locked")
        return True
    else :
        print("Locked fail")
        print(str(RC))
        print(str(error))
        return False

def usage():
    """
    Define and show usage of the script
        OUT optionsList : contains list of value set for option or default value
    """
    global DEBUG
    usage = "usage: C\:Python27\python.exe %prog [options]"
    parser = OptionParser(usage=usage)
    parser.set_defaults(port="COM4",baudrate=57600, debug=False, big_prism=False)
    parser.add_option("-p", "--port", action="store", type="string", dest="port", help="specify used port [default: %default]")
    parser.add_option("-b", "--baudrate", action="store", type="int", dest="baudrate", help="specify used baudrate [default: %default]")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="print debug information")
    parser.add_option("-B", "--Big", action="store_true", dest="big_prism", help="set the big prism as prism type [default: mini prism]")
    (options, args) = parser.parse_args()
    if options.debug : DEBUG = True
    return options

def connection(options):
    """
    Open serial connection between the computer and the total station
        IN optionsList options: contains the options to configure the connection
        OUT system exit if connection failed
    """
    if GeoCom.COM_OpenConnection(options.port, options.baudrate )[0]:
        sys.exit("Can not open Port... exiting")

    #time.sleep(30)

def set_x_axis():
    """
    Set the orientation of the carthesian plan by fixing x axis
    """
    [error, RC, args] = GeoCom.TMC_SetOrientation()
    print("Carthesian coordinates system set, station is 000 and laser directed on x axis")

def set_prism_type(big_prism):
    """
    Set prism type
    """
    if big_prism:
        prism_type = 3 #big 360 prism
    else:
        prism_type = 7 #small 360 prism
    [error, RC, args] = GeoCom.BAP_SetPrismType(prism_type)

def set_laser(value):
    """
    Turn the laser on/off
        IN integer value: (value=1) or off (value=0)
    """
    [error, RC, args] = GeoCom.EDM_Laserpointer(value)

def setup_station_manual(options):
    """
    Setup the station for the purpose of tracking a prism and make fast reapeated measurements
        IN optionsList options: contains the options to configure the station
        OUT boolean: True if the setup suceed
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
    print("Leica is set up")

def setup_station(options):
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


def compute_carthesian(phi,theta,radius):
    """
    Compute carthesian coordinates using vertical, horizontale angles and distance measurements
        IN double phi : horizontale angle
        IN double theta : vertical angles
        IN double radius : distance
    """
    phi = -phi #TODO check why this is necessary
    point_x = round(sin(theta) * cos(phi) * radius,4)
    point_y = round(sin(theta) * sin(phi) * radius,4)
    point_z = round(cos(theta) * radius,4)

    #print the coordinates
    # print ('x('+str(point_x)+') y('+str(point_y)+') z('+str(point_z)+')')
    return ('0;'+str(point_x)+';'+str(point_y)+';'+str(point_z)+';')

    #write point in file
    #with open("msg.txt", "a") as file:
    #    file.write(str(point_x)+","+str(point_y)+","+str(point_z)+"\n")

def get_measure():
    """
    Ask to the station angles and distance and handling it
    """
    global OLD_COORD
    try:
        [error, RC, coord] = GeoCom.TMC_GetSimpleMea(1, 1)
        # if options.debug: print( 'Error: '+ str(error) )
        # if options.debug: print( 'Return Code: '+ str(RC) )
        if RC==0:
            OLD_COORD = coord
            res = compute_carthesian(-float(coord[0]),float(coord[1]),float(coord[2]))
            # print(res)
            return res

        # elif RC==1284:
        #     print('Accuracy could not be guaranteed \n')
        #     coord = OLD_COORD
        #     compute_carthesian(float(coord[0]),float(coord[1]),float(coord[2]))
        # elif RC==1285:
        #     print('No valid distance measurement! \n')
        else:
            print('\n'+'ERROR, Return code: '+str(RC)+'\n')
            return "1"
    except ValueError:
        #print( "Non numeric value recieved!" )
        return "2"
    except GeoCom.SerialRequestError as e :
        return "3"
        # print(e)

def open():
    # try :
    options = usage()
    connection(options)
    setup_station(options)
    print "cool"
    return 1
    # except as e:
    #     return e

def close():
    j=GeoCom.COM_CloseConnection()
    return j[0]


"""#############################################################################
################################### MAIN #######################################
#############################################################################"""
# options = usage()
# options = usage()
# connection(options)
# setup_station(options)

# open()
#
# try :
#     while True: #while program not interrupted by the user
#         #t_start = time.time()
#         print get_measure()
#         #t_end = time.time()
#         #print(t_end-t_start)
# except KeyboardInterrupt :
#     time.sleep(2)
#     i=GeoCom.COM_SwitchOffTPS()
#
#     j=GeoCom.COM_CloseConnection()
#
#
#
#     sys.exit("Keyboard Interruption by user")
#
# # Closing serial connection, when execution is stopped
# GeoCom.COM_CloseConnection()
