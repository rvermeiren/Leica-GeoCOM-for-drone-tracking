import sys
sys.path.append(r"C:\Python27\Lib")
sys.path.append(r"C:\Python27\Lib\site-packages")
import serial
import time

ser = 0
Debug_Level = 1;
GTrId = 0;

class ResponseClass:
    RC_COM = 0
    TrId = 0
    RC = 0
    parameters = []

    def setResponse(self, response):
        if(Debug_Level==2) :
            print 'response = ',response
        # remove the ' from the string, remove the end-line character and split it up
        words = response.replace('\'','').strip().split(',')
        # print words
        if(len(words)>1) :
            self.RC_COM = int(words[1])
            words2 = words[2].split(':')
            self.TrId = int(words2[0])
            self.RC = int(words2[1])

            self.parameters = words[3:len(words)]


            if(self.RC!=0 and Debug_Level==1) :
                print 'Problem occurred, Error code: ', self.RC

class SerialRequestError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def getTrId(request):
    words = request.replace('\'','').strip().split(',')[2].split(':')
    return int(words[0])

def SerialRequest(request, length = 0, t_timeout = 3): #default 3
    if(Debug_Level==2) :
        print 'request = ', request
    id = getTrId(request)
    response = ResponseClass()
    global ser

    try : # try method for the case that TS is not connected
        ser.read(ser.inWaiting())


        ser.write(request + '\r\n')

        t_start = time.time()
        # do as long as:
        # 1: buffer has specific length
        # 2: if specific length not defined (=0), then until buffer > 0
        # 3: timeout not reached

        while((ser.inWaiting()<length or (length == 0 and ser.inWaiting()==0)) and time.time()-t_start<t_timeout) :
            time.sleep(0.001)

        if(time.time()-t_start>=t_timeout) :
            response.RC = 3077
            return response

        time.sleep(0.025)	# Short break to make sure serial port is not read while stuff is written

        serial_output = ser.read(ser.inWaiting())
        response.setResponse(serial_output)
        if response.TrId != id :
            response.RC = 3077
            return response

        #if(Debug_Level==2) :
            #print 'serial_output: ',serial_output

    except KeyboardInterrupt as e :
        raise KeyboardInterrupt(e)
    except :
        raise SerialRequestError("Leica TS communication error - not connected?")
        response.RC = 1

    return response

def HexToDec(hex_in):

    dec_out = int(hex_in, 16)

    return dec_out


def CreateRequest(cmd, args=None):
    """[<LF>]%R1Q,<RPC>[,<TrId>]:[<P0>][,<P1>,...]<Term> """
    global GTrId
    #\n is LF flag to flush buffer
    request = '\n%R1Q,'
    request = request + str(cmd)+ ',' + str(GTrId)
    request = request + ':'

    GTrId+=1
    if GTrId == 8:
        GTrId=0

    if(args!=None):
	if(len(args)>0):
		for i in range(0,len(args)-1) :
		    request = request + str(args[i])
		    request = request + ','

        	request = request + str(args[-1])
    return request

"""#############################################################################
########################### COM - COMMUNICATION ################################
################################################################################
Communication; functions to access some aspects of TPS1200 control, which are
close to communication.
These functions relate either to the client side or to the server side.
"""

def COM_OpenConnection(ePort, eRate, nRetries=10):

    global ser
    try :
        ser = serial.Serial(
            port=ePort,
            baudrate=eRate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

        while(not ser.isOpen()) :
            ser.open()
            if(not ser.isOpen()) :
                ser.close()

        if(not ser.isOpen() and Debug_Level==1) :
            print 'Problem opening port'

        # 0 = everything ok
        return [not ser.isOpen(),ser,0]

    except Exception as e:
        print "Connection Error - Leica TS not connected?\n"
        print str(e)
        return [1,0,[]]


def COM_CloseConnection():

    global ser
    ser.close()


    if(not ser.isOpen() and Debug_Level==1) :
        print 'Problem closing port'

    return [ser.isOpen(),0,[]]


def COM_SwitchOnTPS(eOnMode=2) :

    request = CreateRequest('111',[eOnMode])

    response = SerialRequest(request,0,60)

    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'Turn on TPS'

    elif(response.RC==5) :
        error = 0
        if(Debug_Level==1) :
            print 'TPS already turned on'

    else :
        error = 1
        if(Debug_Level==1) :
            print 'Problem turning TPS on'

    return [error,response.RC,[]]


def COM_SwitchOffTPS(eOffMode=0) :

    request = CreateRequest('112',[eOffMode])

    response = SerialRequest(request,0,60)


    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'Shut down TPS'

    else :
        error = 1
        if(Debug_Level==1) :
            print 'Error shutting down TPS'

    return [error,response.RC,[]]

"""#############################################################################
########################## CSV - CENTRAL SERVICES ##############################
################################################################################
Central Services; this module provides functions to get or set central/basic
information about the TPS1200 instrument.
"""

def CSV_GetDateTime():
    DateTime = []

    response = SerialRequest('%R1Q,5008:')

    error = 1
    if(response.RC==0) :
        error = 0

        DateTime = [int(response.parameters[0])]
        for i in range(1,len(response.parameters)) :
            DateTime.append(HexToDec(response.parameters[i]))

        if(Debug_Level==1) :
            print 'Date and Time: ', DateTime



    return [error,response.RC,DateTime]


"""#############################################################################
########################## AUT - AUTOMATISATION ################################
################################################################################
Automatisation; a module which provides functions like the control of the
Automatic Target Recognition, Change Face function or Positioning functions.
"""

'''
AUT_NORMAL = 0, // fast positioning mode
AUT_PRECISE = 1 // exact positioning mode
'''
'''
AUT_ATRMODE // Possible modes of the target
// recognition
AUT_POSITION = 0, // Positioning to the hz- and v-angle
AUT_TARGET = 1 // Positioning to a target in the
// environment of the hz- and v-angle.
'''

def AUT_MakePositioning(Hz, V, POSMode=0, ATRMode=0, bDummy=0): #GeoCom manual p41

    request = CreateRequest('9027',[Hz,V,POSMode, ATRMode, bDummy])

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'Going to new position: ', Hz, ',', V


    return [error, response.RC, []]

def AUT_Search(Hz_Area, V_Area, bDummy = 0):

    request = CreateRequest('9029',[Hz_Area, V_Area, bDummy])

    response = SerialRequest(request,0, 120)

    error = 1
    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'Target search successful'
    else :
        if(Debug_Level==1) :
            if(response.RC==8710) :
                print 'No target found'

    return [error, response.RC, []]


# Does not work - connection time out...
# seems to be not needed, when the Leica is directed to the prism
def AUT_FineAdjust(dSrchHz=0.1, dSrchV=0.1):

    request = CreateRequest('9037',[dSrchHz, dSrchV, 0])

    response = SerialRequest(request,0,120)

    error = 1
    if(response.RC==0) :
        error = 0

    return [error, response.RC, []]


def AUT_LockIn() :

    request = CreateRequest('9013',[])

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'Lock successful'


    return [error, response.RC, []]

"""#############################################################################
#################### EDM - Electronic Distance Meter ###########################
################################################################################
Electronic Distance Meter; the module, which measures distances.

"""
def EDM_Laserpointer(eOn = 0):

    request = CreateRequest('1004',[eOn])

    response = SerialRequest(request,0,30)

    error = 1
    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'Laserpointer turned on/off'


    return [error, response.RC, []]

"""#############################################################################
################ TMC - Theodolite Measurement and Calculation ##################
################################################################################
Theodolite Measurement and Calculation; the core module for getting measurement
data.
"""
def TMC_SetOrientation():

    request = CreateRequest('2113',[0])

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0

    return [error, response.RC, []]

def TMC_DoMeasure(cmd=1, mode=1) : #TMC Measurement Modes in geocom manual p.91

    request = CreateRequest('2008',[cmd,mode])

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'Measuring successful'


    return [error, response.RC, []]


def TMC_SetEdmMode(mode=6) :

    request = CreateRequest('2020',[mode])

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'EDM Mode set successfully'

    return [error, response.RC, []]


def TMC_GetCoordinate(WaitTime=100,mode=1) :
    coord = []

    request = CreateRequest('2082',[WaitTime,mode])

    response = SerialRequest(request)

    error = 0

    if(len(response.parameters)==8) :

        coord = [float(response.parameters[0]),float(response.parameters[1]),float(response.parameters[2])]

        if(Debug_Level==1) :
            print 'Coordinates read successfully: ', coord


    return [error, response.RC, coord]

def TMC_GetStation(WaitTime=100):
    coord = []

    request = CreateRequest('2009',[WaitTime])

    response = SerialRequest(request)

    error = 0

    if(len(response.parameters)==4) :

        coord = [float(response.parameters[0]),float(response.parameters[1]),float(response.parameters[2]),float(response.parameters[3])]

        if(Debug_Level==1) :
            print 'Station coordinates received successfully! ',coord


    return [error, response.RC, []]

def TMC_GetSimpleMea(WaitTime=100, mode = 1) : #TMC_GetSimpleMea - Returns angle and distance measurement - geocom manual p.95
    coord = []
    request = CreateRequest('2108',[WaitTime,mode])

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0
        if len(response.parameters) < 3 :
            return [1, 1, []]
        coord = [response.parameters[0],response.parameters[1],response.parameters[2]]
        if(Debug_Level==1) :
            print 'Coordinates read successfully: ', coord
    if(response.RC==1285) :
        error = 1285
        coord = [response.parameters[0],response.parameters[1]]
        if(Debug_Level==1) :
            print 'Angles read successfully: ', coord


    return [error, response.RC, coord]


def TMC_QuickDist() : #TMC_QuickDist - Returns slope-distance and hz-,v-angle - geocom manual p.100
    coord = []
    request = CreateRequest('2117')
    response = SerialRequest(request)
    error = 1
    if(response.RC==0) :
        error = 0
        coord = [response.parameters[0],response.parameters[1],response.parameters[2]]

    return [error, response.RC, coord]


def TMC_GetAngle(mode = 1) : #geocom manual p.98 TMC_GetAngle5
    coord = []
    request = CreateRequest('2107',[mode])

    response = SerialRequest(request)
    error = 1

    if(len(response.parameters)==2) :

        if(response.RC==0):

            error = 0
            coord = [response.parameters[0],response.parameters[1]]

    return [error, response.RC, coord]


def TMC_GetEdmMode():
#
#    EDM_MODE = {0 : 'EDM_MODE_NOT_USED',
#                1 : 'EDM_SINGLE_TAPE',
#                2 : 'EDM_SINGLE_STANDARD',
#                3 : 'EDM_SINGLE_FAST',
#                4 : 'EDM_SINGLE_LRANGE',
#                5 : 'BAP_CONT_REF_FAST',
#                6 : 'BAP_CONT_RLESS_VISIBLE',
#                7 : 'BAP_AVG_REF_STANDARD',
#                8 : 'BAP_AVG_REF_VISIBLE',
#                9 : 'BAP_AVG_RLESS_VISIBLE',
#                10 :'BAP_CONT_REF_SYNCHRO',
#                11 :'BAP_SINGLE_REF_PRECISE'}
##    EDM_MODE :
##        EDM_MODE_NOT_USED       0, // Init value
##                 1, // IR Standard Reflector Tape
##             2, // IR Standard
##                 3, // IR Fast
##               4, // LO Standard
##        EDM_SINGLE_SRANGE       5, // RL Standard
##        EDM_CONT_STANDARD       6, // Standard repeated measurement
##        EDM_CONT_DYNAMIC        7, // IR Tacking
##        EDM_CONT_REFLESS        8, // RL Tracking
##        EDM_CONT_FAST           9, // Fast repeated measurement
##        EDM_AVERAGE_IR          10,// IR Average
##        EDM_AVERAGE_SR          11,// RL Average
##        EDM_AVERAGE_LR          12,// LO Average
##        EDM_PRECISE_IR          13,// IR Precise (TS30, TM30)
##        EDM_PRECISE_TAPE        14,// IR Precise Reflector Tape (TS30, TM30)
#
   request = CreateRequest('2021',[])

   response = SerialRequest(request)

   error = 1
   if(response.RC==0) :
       error = 0
       if(Debug_Level==1) :
           print 'EDM Mode read successfully: '

   return [error, response.RC,response.parameters]

#
#def TMC_SetEdmMode(mode) :
#
##    EDM_MODE :
##        EDM_MODE_NOT_USED       0, // Init value
##        EDM_SINGLE_TAPE         1, // IR Standard Reflector Tape
##        EDM_SINGLE_STANDARD     2, // IR Standard
##        EDM_SINGLE_FAST         3, // IR Fast
##        EDM_SINGLE_LRANGE       4, // LO Standard
##        EDM_SINGLE_SRANGE       5, // RL Standard
##        EDM_CONT_STANDARD       6, // Standard repeated measurement
##        EDM_CONT_DYNAMIC        7, // IR Tacking
##        EDM_CONT_REFLESS        8, // RL Tracking
##        EDM_CONT_FAST           9, // Fast repeated measurement
##        EDM_AVERAGE_IR          10,// IR Average
##        EDM_AVERAGE_SR          11,// RL Average
##        EDM_AVERAGE_LR          12,// LO Average
##        EDM_PRECISE_IR          13,// IR Precise (TS30, TM30)
##        EDM_PRECISE_TAPE        14,// IR Precise Reflector Tape (TS30, TM30)
#
#    request = CreateRequest('2020',[mode])
#
#    response = SerialRequest(request)
#
#    error = 1
#    if(response.RC==0) :
#        error = 0
#        if(Debug_Level==1) :
#            print 'EDM Mode set successfully'
#
#    return [error, response.RC, []]

"""#############################################################################
########################## MOT - Motorization ##################################
################################################################################
Motorization; the part, which can be used to control the movement and the speed
of movements of the instrument.
"""

'''
enum MOT_MODE #GeoCom manual p83
{
MOT_POSIT = 0, // configured for relative postioning
MOT_OCONST = 1, // configured for constant speed
// the only valid mode
// for SetVelocity is MOD_OCONST
MOT_MANUPOS = 2, // configured for manual positioning
// default setting
MOT_LOCK = 3, // configured as "Lock-In"-controller
MOT_BREAK = 4, // configured as "Brake"-controller
// do not use 5 and 6
MOT_TERM = 7 // terminates the controller task

'''

def MOT_StartController(ControlMode=1): #GeoCom manual p83
    request = CreateRequest('6001',[ControlMode])

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'Motor controller started'

    return [error, response.RC, []]

'''
enum MOT_STOPMODE #GeoCom manual p83
{
MOT_NORMAL = 0, // slow down with current acceleration
MOT_SHUTDOWN = 1 // slow down by switch off power supply
'''

def MOT_StopController(Mode=0):

    request = CreateRequest('6000',[Mode])

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'Motor controller stopped'


    return [error, response.RC, []]
'''

'''
def MOT_SetVelocity(Hz_speed,v_speed) : #GeoCom manual p85

    request = CreateRequest('6004',[Hz_speed,v_speed])

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'Velocity set'


    return [error, response.RC, []]

"""#############################################################################
######################## BAP - Basic Applications ##############################
################################################################################
Basic Applications; some functions, which can easily be used to get measuring
data.
"""
def BAP_SetPrismType(PrismType = 7):

    request = CreateRequest('17008',[PrismType])

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0

    return [error, response.RC, []]

BAP_TARGET_TYPE = { 0 : 'BAP_REFL_USE', # with reflector
                    1 : 'BAP_REFL_LESS'} # without reflector

def BAP_GetTargetType() :
    parameter = []
    request = CreateRequest('17022',[])

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0
        parameter = response.parameters[0]

        if(Debug_Level==1) :
            print 'Target type: ', BAP_TARGET_TYPE[int(response.parameters[0])][1]


    return [error, response.RC, parameter]



def BAP_SetTargetType(eTargetType = 0) :

    request = CreateRequest('17021',[eTargetType])

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'Target type set successfully '


    return [error, response.RC, []]

#BAP_TARGET_TYPE
#BAP_REFL_USE = 0 // with reflector
#BAP_REFL_LESS = 1 // without reflector

BAP_PRISMTYPE = {0 : ['BAP_PRISM_ROUND', 'Leica Circular Prism'],
                 1 : ['BAP_PRISM_MINI', 'Leica Mini Prism'],
                 2 : ['BAP_PRISM_TAPE', 'Leica Reflector Tape'],
                 3 : ['BAP_PRISM_360', 'Leica 360 Prism'],
                 4 : ['BAP_PRISM_USER1', 'not supported'],
                 5 : ['BAP_PRISM_USER2', 'not supported'],
                 6 : ['BAP_PRISM_USER3', 'not supported'],
                 7 : ['BAP_PRISM_360_MINI', 'Leica Mini 360 Prism'],
                 8 : ['BAP_PRISM_MINI_ZERO', 'Leica Mini Zero Prism'],
                 9 : ['BAP_PRISM_USE', 'User Defined Prism'],
                 10 :['BAP_PRISM_NDS_TAPE','Leica HDS Target'],
                 11 :['BAP_PRISM_GRZ121_ROUND', 'GRZ121 360 Prism for Machine Guidance'],
                 12 :['BAP_PRISM_MA_MP3122', 'MPR122 360 Prism for Machine Guidance'] }


def BAP_GetPrismType() :
    parameter = []

    request = CreateRequest('17009',[])

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0
        parameter = [response.parameters[0], BAP_PRISMTYPE[int(response.parameters[0])][1]]
        if(Debug_Level==1) :
            print 'Prism type: ', BAP_PRISMTYPE[int(response.parameters[0])][1]


    return [error, response.RC, parameter]

def BAP_SetPrismType(ePrismType) :

    request = CreateRequest('17008',[ePrismType])

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'Prism type set'

    return [error, response.RC, []]

def BAP_SetMeasPrg(eMeasPrg) :

    request = CreateRequest('17019',[eMeasPrg])

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'Measurement program set'


    return [error, response.RC, []]


BAP_USER_MEASPRG = {0 : ['BAP_SINGLE_REF_STANDARD','Reflector, Standard'],
                    1 : ['BAP_SINGLE_REF_FAST', 'Reflector, Fast'],
                    2 : ['BAP_SINGLE_REF_VISIBLE', 'Long Range, Standard'],
                    3 : ['BAP_SINGLE_RLESS_VISIBLE', 'No Reflector, Standard'],
                    4 : ['BAP_CONT_REF_STANDARD', 'Reflector, Tracking'],
                    5 : ['BAP_CONT_REF_FAST', 'not available'],
                    6 : ['BAP_CONT_RLESS_VISIBLE', 'No Reflector, Fast Tracking'],
                    7 : ['BAP_AVG_REF_STANDARD', 'Reflector, Average'],
                    8 : ['BAP_AVG_REF_VISIBLE', 'Long Range, Average'],
                    9 : ['BAP_AVG_RLESS_VISIBLE', 'No Reflector, Average'],
                    10 :['BAP_CONT_REF_SYNCHRO', 'Reflector, Synchro Tracking'],
                    11 :['BAP_SINGLE_REF_PRECISE','not available']}

def BAP_MeasDistanceAngle(mode = 6): #GeoCom manual p62
    coord = []

    request = CreateRequest('17017',[mode])

    response = SerialRequest(request)

    error = None

    if(len(response.parameters)==4) :

        coord = [float(response.parameters[0]),float(response.parameters[1]),float(response.parameters[2]),int(response.parameters[3])]

        if(Debug_Level==1) :
            print 'Got data successfully: ', coord

    return [error, response.RC, coord]

def BAP_GetMeasPrg() :

    parameter = []


    request = CreateRequest('17018',[])

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0
        parameter = [response.parameters[0],BAP_USER_MEASPRG[int(response.parameters[0])][1]]
        if(Debug_Level==1) :
            print 'Measurement program: ', BAP_USER_MEASPRG[int(response.parameters[0])][1]


    return [error, response.RC, parameter]


def BAP_SearchTarget(bDummy = 0) :

    request = CreateRequest('17020',[bDummy])

    response = SerialRequest(request,0,10)

    error = 1
    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'Prism found!'

    else :
        if(Debug_Level==1) :

            if(response.RC == 8710) :
                print 'No prism found!'

            elif(response.RC == 8711) :
                print 'Multiple prism found!'


    return [error, response.RC, []]

"""#############################################################################
############################## AUS - ALT User ##################################
################################################################################
The subsystem "Alt User" mainly contains functions behind the "SHIFT" + "USER"
button.
"""
def AUS_SetUserLockState(on = 0):

    request = CreateRequest('18007',[on])

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'Lock activated or deactivated'


    return [error, response.RC, []]

def AUS_SetUserAtrState(on = 0):

    request = CreateRequest('18005',[on])

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'ATR activated or deactivated'


    return [error, response.RC, []]

def AUS_GetUserLockState():

    request = CreateRequest('18008')

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'Lock activated or deactivated'


    return [error, response.RC, response.parameters]

def AUS_GetUserAtrState():

    request = CreateRequest('18006')

    response = SerialRequest(request)

    error = 1
    if(response.RC==0) :
        error = 0
        if(Debug_Level==1) :
            print 'ATR activated or deactivated'


    return [error, response.RC, response.parameters]
