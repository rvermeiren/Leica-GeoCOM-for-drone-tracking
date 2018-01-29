import sys
import time
import GeoCom_mod
from optparse import OptionParser

# Handling options
usage = "usage: rosrun leica_interface %prog [options]"
parser = OptionParser(usage=usage)
parser.set_defaults(v_r=1.0, h_r=1.0, big_prism=False, port="/dev/ttyUSB0")
parser.add_option("-z", "--horizontale", action="store", dest="h_r", help="horizontale angle")
parser.add_option("-v", "--vertical", action="store", dest="v_r", help="vertical angle")
parser.add_option("-p", "--port", action="store", type="string", dest="port", help="specify used port [default: %default]")
parser.add_option("-b", "--big", action="store_true", dest="big_prism", help="set the big prism as prism type [default: mini prism]")
(options, args) = parser.parse_args()

print "Initializing Leica TS"
if GeoCom_mod.COM_OpenConnection(int(options.port), 115200)[0]:
  sys.exit("Can not open Port... exiting")
prism_type = 7
if options.big_prism:
  prism_type = 3;
  print "Using the big prism"
GeoCom_mod.BAP_SetPrismType(prism_type)
[error, RC, []] = GeoCom_mod.MOT_StartController()
print("StartController "+str(error)+" "+str(RC))
time.sleep(3)
[error, RC, []] = GeoCom_mod.AUT_MakePositioning(options.h_r,options.v_r)
print("Positionning "+str(error)+" "+str(RC))
time.sleep(3)

[error, RC, []] = GeoCom_mod.MOT_StopController()
print("StopController "+str(error)+" "+str(RC))
# print "search ..."
# [error, RC, []] = GeoCom_mod.AUT_Search(options.h_r,options.v_r)
# print("SearchTarget "+str(error)+" "+str(RC))
# [error, RC, []] = GeoCom_mod.BAP_SearchTarget()#(options.h_r,options.v_r)
# print("SearchTarget "+str(error)+" "+str(RC))
# [error, RC, []] = GeoCom_mod.AUT_FineAdjust()
# print("FineAdjust "+str(error)+" "+str(RC))
# [error, RC, []] = GeoCom_mod.AUT_LockIn()
# print("LockIn"+str(error)+" "+str(RC))


print "Leica TS is set up"
#GeoCom_mod.TMC_SetEdmMode(7)
#GeoCom_mod.CSV_GetInstrumentNo()
#GeoCom_mod.AUT_FineAdjust()
#GeoCom_mod.AUT_LockIn()

GeoCom_mod.COM_CloseConnection()
