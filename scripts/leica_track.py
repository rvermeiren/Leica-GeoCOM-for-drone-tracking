#!/usr/bin/env python

# import roslib; roslib.load_manifest('leica_ros_sph')
# import rospy
import sys
import time
import math
import GeoCom_mod
from math import sin,cos
#
# from geometry_msgs.msg import PointStamped
from optparse import OptionParser
from operator import neg

# Handling options
usage = "usage: rosrun leica_interface %prog [options]"
parser = OptionParser(usage=usage)
parser.set_defaults(port="/dev/ttyUSB0",baudrate=115200, debug=False)
parser.add_option("-p", "--port", action="store", type="string", dest="port", help="specify used port [default: %default]")
parser.add_option("-b", "--baudrate", action="store", type="int", dest="baudrate", help="specify used baudrate [default: %default]")
parser.add_option("-d", "--debug", action="store_true", dest="debug", help="print debug information")
(options, args) = parser.parse_args()

if GeoCom_mod.COM_OpenConnection(int(options.port), options.baudrate )[0]:
    sys.exit("Can not open Port... exiting")

GeoCom_mod.EDM_Laserpointer(0)

GeoCom_mod.TMC_SetOrientation()
print("Carthesian coordinates system set, station is 000 and laser directed on x axis")

prism_type = 7
GeoCom_mod.BAP_SetPrismType(prism_type)


if GeoCom_mod.AUT_Search(math.radians(20),math.radians(10))[1] == 0:
    if GeoCom_mod.AUT_FineAdjust(math.radians(2),math.radians(2))[1] != 0:
        print ("prism not found")
        sys.exit("Can not found prism... exiting")
    else :
        print ("prism found")

GeoCom_mod.AUT_LockIn()
GeoCom_mod.TMC_SetEdmMode(9) #EDM_CONT_FAST = 9, // Fast repeated measurement (geocom manual p.91)
GeoCom_mod.TMC_DoMeasure()
time.sleep(2)
print "Leica is set up"

# Set up ROS:
# rospy.init_node('leica_node')
# point_pub = rospy.Publisher('/leica/worldposition',PointStamped, queue_size=1) #prism location in original total station world frame
# point_msg = PointStamped()
# print "ROS-node is set up"

loop_count = 1
try :
    while True:

        try:
            #[error, RC, coord] = GeoCom_mod.TMC_GetCoordinate()
            # GeoCom get simple measurements
            [error, RC, coord] = GeoCom_mod.TMC_GetSimpleMea(5, 1)


            if options.debug: print( 'Error: '+ str(error) )
            if options.debug: print( 'Return Code: '+ str(RC) )
            # if options.debug: print( 'Received: '+ str(coord) )

            if RC==0:

                #should be ENU - XYZ
                # point_x =   float(coord[0])  #East
                # point_y =   float(coord[1])  #North
                # point_z =  float(coord[2])   #Up
                # get angles and distance
                phi = -float(coord[0])
                theta = float(coord[1])
                radius = float(coord[2])

                # compute carthesian coordinates
                point_x = round(sin(theta) * cos(phi) * radius,4)
                point_y = round(sin(theta) * sin(phi) * radius,4)
                point_z = round(cos(theta) * radius,4)

                print ('x('+str(point_x)+') y('+str(point_y)+') z('+str(point_z)+')')

            elif RC==1284:
                print( 'Accuracy could not be guaranteed \n' )
                #print ('Still sending data:'+str(coord))
                # point_x =   float(coord[0])  #East
                # point_y =   float(coord[1])  #North
                # point_z =  float(coord[2])   #Up

                point_x = sin(theta) * cos(phi) * radius
                point_y = sin(theta) * sin(phi) * radius
                point_z = cos(theta) * radius
                print ('x('+str(point_x)+') y('+str(point_y)+') z('+str(point_z)+')')

            elif RC==1285:
                print('No valid distance measurement! \n')

            else:
                print( '\n'+'ERROR, Return code: '+str(RC)+'\n')

            # point_msg.header.seq = loop_count
            # point_msg.header.stamp = rospy.Time.now()
            # point_msg.header.frame_id = 'world'
            # point_msg.point.x = point_x
            # point_msg.point.y = point_y
            # point_msg.point.z = point_z
            # point_pub.publish(point_msg)

            loop_count = loop_count + 1
        except ValueError:
            print( "Non numeric value recieved!" )

        # except:
        #     print( "No measurement or drop." )
        #     # Short break in case the problem was related to the serial connection.
        #     time.sleep(0.2)
        #     # Then restart the measurement
        #     GeoCom_mod.TMC_DoMeasure()
        #     print( "Restarted measurements" )
except KeyboardInterrupt :
    GeoCom_mod.COM_CloseConnection()
    sys.exit("KeyboardInterrupt")

# Closing serial connection, when execution is stopped
GeoCom_mod.COM_CloseConnection()
