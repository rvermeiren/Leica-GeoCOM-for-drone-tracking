#!/usr/bin/env python
import sys
import time
import math
import GeoCom_mod
from optparse import OptionParser
from operator import neg

# Handling options
usage = "usage: python27 leica_scan.py %prog [options]"
parser = OptionParser(usage=usage)
parser.set_defaults(port="3",baudrate=115200, debug=False, dHzRes = 0.1, dVRange =  20, dHzRange =  20, motvelV = 0.02)

parser.add_option("-p", "--port", action="store", type="string", dest="port", help="specify used port [default: %default]")
parser.add_option("-b", "--baudrate", action="store", type="int", dest="baudrate", help="specify used baudrate [default: %default]")
parser.add_option("-d", "--debug", action="store_true", dest="debug", help="print debug information")

parser.add_option("-v", "--vrange", action="store", type="int", dest="dVRange", help="vertical scanning range in degree [default: %default]")
parser.add_option("-z", "--hrange", action="store", type="int", dest="dHzRange", help="horizontal scanning range in degrees [default: %default]")
parser.add_option("-r", "--resolution", action="store", type="float", dest="dHzRes", help="specify horizontal resolution in radians [default: %default]")
parser.add_option("-s", "--speed", action="store", type="float", dest="motvelV", help="specify scanning speed [default: %default]")

(options, args) = parser.parse_args()

if GeoCom_mod.COM_OpenConnection(int(options.port), options.baudrate )[0]:
    sys.exit("Can not open Port... exiting")

GeoCom_mod.TMC_SetEdmMode(9)
print 1
GeoCom_mod.BAP_SetMeasPrg(6)
print 2
GeoCom_mod.BAP_SetTargetType(1)
print 3
GeoCom_mod.BAP_MeasDistanceAngle(6)
print 4
GeoCom_mod.MOT_SetVelocity(0,0)
print 5
GeoCom_mod.MOT_StopController()
print 6

GeoCom_mod.TMC_DoMeasure()
time.sleep(2)
print "Leica TS is set up"


status = None #status 1 for moving down, 2,3 for right, 4 for up
loop_count = 0
dV,dHz = 0,0

''' Scanning window'''
dVRange =  options.dVRange #vertical scanning range in degrees
dHzRange = options.dHzRange #horizontal scanning range in degrees

dVRange = math.radians(dVRange)
dHzRange = math.radians(dHzRange)

'''Resolution'''
dHzRes = options.dHzRes #horizontal resolution in radians

'''Scanning speed'''
motvelHz = 0.01 #radians per second (min value 0.01)
motvelV = options.motvelV #radians per second (min value 0.01)



def move_telescope():
    global loop_count,dVRange,dHzRange,dHzStart,dVStart,dHzTgt,dVTgt,motvelHz,motvelV,status,dHzLast
    try:
        if loop_count==1:
            GeoCom_mod.MOT_StartController()
            GeoCom_mod.MOT_SetVelocity(0,motvelV)
            status=1
            print ' \n Scanning started! \n'
            print 'Move down started! \n'
            return 1
        elif loop_count>0:
            try:
                dHz,dV = read_angle()
            except:
                print 'dHz,dV = read_angle() Error!'

            if  status==1: #if moving down
                if dV>dVTgt:
                    print 'Reached vertical target! \n'
                    [error, RC, t] = GeoCom_mod.MOT_SetVelocity(motvelHz,0) #start moving right
                    if RC==0:
                        print 'Move right started! \n'
                        dHzLast,dVLast = dHz,dV  #capture position at the start of the move
                        status = 2
                        return 1

            if  status==2: #if moving to the right at the bottom
                if dHz>dHzLast+dHzRes:
                    print 'Reached horizontal target! \n'
                    [error, RC, t] = GeoCom_mod.MOT_SetVelocity(0,-motvelV) #start moving up
                    if RC==0:
                        print 'Move right started! \n'
                        dHzLast,dVLast = dHz,dV  #capture position at the start of the move
                        status = 3
                        return 1

            if  status==3: #if moving up
                if dV<dVStart:
                    print 'Reached vertical target! \n'
                    [error, RC, t] = GeoCom_mod.MOT_SetVelocity(motvelHz,0) #start moving right
                    if RC==0:
                        print 'Move right started! \n'
                        dHzLast,dVLast = dHz,dV #capture position at the start of the move
                        status = 4
                        return 1

            if  status==4: #if moving right at the top
                if dHz>dHzLast+dHzRes:
                    print 'Reached vertical target! \n'
                    [error, RC, t] = GeoCom_mod.MOT_SetVelocity(0,motvelV) #start moving down
                    if RC==0:
                        print 'Move right started! \n'
                        dHzLast,dVLast = dHz,dV #capture position at the start of the move
                        status = 1
                        return 1

            if dHz>dHzTgt and dV>dVTgt:
                print ' \n SCAN COMPLETE !!! \n'
                return 0
            else:
                return 1
    except:
        print 'move_telescope: Error!'

def read_angle(): # Get current telescope angle
    try:
        [error, RC, angles] = GeoCom_mod.TMC_GetAngle()
        if RC==0:
            #print 'Successfully read angles'
            #print 'angles = ', angles, '\n'
            dHz = float(angles[0])
            dV = float(angles[1])
            return dHz,dV
    except ValueError:
        print "Non numeric value recieved!"
    except:
        print 'READ_ANGLE: Error'

def initialize():
    global loop_count,dVRange,dHzRange,dHzStart,dVStart,dHzTgt,dVTgt,dHzInit,dVInit
    if loop_count==0:

        dHz,dV = read_angle()
        dHzInit,dVInit = dHz, dV
        dHzStart = dHz-(float(dHzRange)/2)
        dVStart = dV - (float(dVRange)/2)
        #print 'DEBUG:', dHzStart,dVStart
        dHzTgt = dHzStart+dHzRange
        dVTgt = dVStart+dVRange

        GeoCom_mod.MOT_StartController()
        [error, RC, t] = GeoCom_mod.AUT_MakePositioning(dHzStart,dVStart)
        if RC==0:
            GeoCom_mod.MOT_StopController()
            loop_count+=1
            time.sleep(1)
            print ' \n Positioning successfull! \n'


def scan_publish(x,y,z):

    #scan_msg.point.x = x
    #scan_msg.point.y = y
    #scan_msg.point.z = z
    #print x,y,z
    pass
    #instrPos_pub.publish(str(coord))

def measure_point():
    global loop_count
    try:
        [error, RC, coord] = GeoCom_mod.TMC_GetCoordinate(100,1)

        #print 'coord = ', coord
        if RC==0:
            #print 'Successfully measured point \n'
            #should be ENU - XYZ
            point_x =   float(coord[0])  #East
            point_y =   float(coord[1])  #North
            point_z =   float(coord[2])  #Up
            scan_publish(point_x,point_y,point_z)
            loop_count+=1
        else:
            print 'measure_point: Failed to receive measurements! '
    except ValueError:
        print "Non numeric value recieved!"
    except:
        print "No measurement or drop."
        time.sleep(0.3) # Short break in case the problem was related to the serial connection.
        GeoCom_mod.TMC_DoMeasure() # Then restart the measurement
        print "Restarted measurements"

while True:

    #print 'status: ',status
    #print 'loop_count: ',loop_count
    initialize()

    if move_telescope():
        measure_point()

    else:
        GeoCom_mod.AUT_MakePositioning(dHzInit,dVInit)
        time.sleep(3)
        GeoCom_mod.MOT_SetVelocity(0,0)
        GeoCom_mod.MOT_StopController()
        print 'END PROGRAM!'
        break
    loop_count+=1

if sys.exit:
    print 'System exit detected'
    GeoCom_mod.MOT_SetVelocity(0,0)
    GeoCom_mod.AUT_MakePositioning(dHzInit,dVInit)
    time.sleep(3)
    GeoCom_mod.MOT_StopController()
# Closing serial connection, when execution is stopped
GeoCom_mod.COM_CloseConnection()
