GeoCOM
*******

All functions specified here are specified as in the TPS1200 GeoCOM reference manual, **V1.20**.
Not all of them are specified: the ones used in the main script are described in details, while the others simply redirect to the page of the reference manual where they are described.

Not all functions available in GeoCOM are implemented in this script.

In the specification of some GeoCOM functions, not all RC codes possibly returned by the function are given and described.
You can easily check them in the GeoCOM reference manual.

Classes
--------

.. automodule:: GeoCom
	:members: getTrId, HexToDec, SerialRequest, CreateRequest
	
	.. autoclass :: ResponseClass
		:members:

.. exception:: SerialRequestError

COM -- Communication
---------------------
.. automodule:: GeoCom
	:members: COM_CloseConnection, COM_OpenConnection, COM_SwitchOnTPS, COM_SwitchOffTPS, COM_GetSWVersion

AUT -- Automation
------------------
.. automodule:: GeoCom
	:members: AUT_MakePositioning, AUT_Search, AUT_FineAdjust, AUT_LockIn, AUT_GetSearchArea, AUT_SetSearchArea, AUT_PS_EnableRange, AUT_PS_SetRange, AUT_PS_SearchWindow

CSV -- Central services
------------------------
.. automodule:: GeoCom
	:members: CSV_GetDateTime

EDM -- Electronic Distance Measurement
---------------------------------------
.. automodule:: GeoCom
	:members: EDM_Laserpointer

TMC -- Theodolite Measurement and Calculation
----------------------------------------------
.. automodule:: GeoCom
	:members: TMC_SetOrientation, TMC_DoMeasure, TMC_SetEdmMode, TMC_GetCoordinate, TMC_GetStation, TMC_GetSimpleMea, TMC_QuickDist, TMC_GetAngle, TMC_GetEdmMode

MOT -- Motorization
--------------------
.. automodule:: GeoCom
	:members: MOT_StartController, MOT_StopController, MOT_SetVelocity

BAP -- Basic Applications
--------------------------
.. automodule:: GeoCom
	:members: BAP_GetTargetType, BAP_SetTargetType, BAP_SetPrismType, BAP_GetPrismType, BAP_SetMeasPrg, BAP_MeasDistanceAngle, BAP_GetMeasPrg, BAP_SearchTarget

AUS -- ALT User
----------------
.. automodule:: GeoCom
	:members: AUS_SetUserLockState, AUS_SetUserAtrState, AUS_GetUserLockState, AUS_GetUserAtrState, AUS_GetUserLockState, AUS_GetUserAtrState
