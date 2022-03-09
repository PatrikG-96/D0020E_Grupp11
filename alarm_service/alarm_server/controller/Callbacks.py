from twisted.python import log
from twisted.python.failure import Failure
from protocol.parse import *
from protocol.exceptions import ProtocolException
from protocol.messages import ErrorCodes
import json
from controller.CallbackExceptions import *
from copy import deepcopy
from database.database import setNewAlarm, getSensorMonitor, getSensor, readAlarm, resolveAlarm, getUser, getServerAccess
import bcrypt

def decode(bytes):
    try:
        return bytes.decode()
    except Exception as e:
         raise DecodeException(str(e), ErrorCodes.InvalidEncoding)
        
def decodeErr(failure : Failure):
     log.msg(f"In decodeErr: {failure.value}")
     if type(failure.value) == DecodeException:
         log.msg(failure.value.__repr__())

def toJson(data : str):
    log.msg(f"Attempting to parse {data} to JSON format")
    try:
        return json.loads(data)
    except Exception as e:
        raise JsonException(f"Failed at parsing JSON with error {e}", ErrorCodes.InvalidJson, data)

def jsonErr(failure: Failure):
    log.msg(f"In jsonErr: {failure.value}")
    # If the error is supposed to be handled by this errback, log it
    if type(failure.value) == JsonException:
        log.msg(failure.value.__repr__())
    # If parsing to JSON failed, this needs to propagate through the callback chain
    failure.raiseException()

def parseJson(json: dict):
    log.msg(f"Attempting to parse {str(json)} into a Message object")
    return parse_JSON(json)

def parseErr(failure : Failure):
    log.msg(f"In parseErr: {failure.value}")
    # If the error is a FormatError raised by parse(), log it
    if type(failure.value) == FormatException:
        log.msg(failure.value.__repr__())            
    # Here, we either have a FormatException which is logged or a JsonException which is logged before
    # Both of these need to propagate, so we need to respond with an error message
    failure.raiseException()
    
# # # # # # # ## # # # # # # # # # # # # 

def __tokenResponse(message : TokenResponseMessage):
    
    log.msg(f"Parsing token response")
    success = True
    user = getUser(message.username)
    
    if user is None:
        log.msg(f"Did not find user")
        success = False
    
    access = getServerAccess(user.userID)
    
    if access is None:
        log.msg("did not find access")
        success = False
    else:
        # Do we need to verify password here? super slow with bcrypt
        if bcrypt.checkpw(message.password.encode(), user.password.encode()):
            log.msg("password verified")
            success = (message.token == access.token)
            log.msg(f"Message token: {message.token}, access token: {access.token}")
        else:
            log.msg(f"password {message.password} was incorrect")
    if success:
        return TokenAuthResultMessage.success(user.userID)
    return TokenAuthResultMessage.failure(user.userID)
    
def __alarmResponse(message : AlarmResponseMessage):
    
    if message.reponse_type == "READ":
        readAlarm(int(message.alarm_id), int(message.client_id), message.timestamp)
    if message.reponse_type == "RESOLVED":
        resolveAlarm(int(message.alarm_id), int(message.client_id), message.timestamp)
    
    worked = True
    if worked:
        return AlarmResponseConfirmationMessage.success(message.json)
    return AlarmResponseConfirmationMessage.failure(message.json)
    
    
def __sensorResponse(message : SensorAlertMessage):
    
    sensor = getSensor(message.sensor_id)
    print(f"Sensor: {sensor.sensorID}")
    monitor = getSensorMonitor(sensor.sensorID)
    print(f"Monitor: {monitor.monitorID}") 
    
    alarm = setNewAlarm(monitor.monitorID, message.alarm_type, message.timestamp)
    
    args = {'type' : "SensorAlertResponse", 'received' : False}
    
    # Do I need to check for errors here?
    if True:
        args['received'] = True
    res = SensorAlertResponseMessage(args)
    
    if ALARM_TYPE_ACTION[message.alarm_type]:
        
        alarm_args = {'type' : 'AlarmNotification', 'monitor_id' : monitor.monitorID, 'sensor_id' : message.sensor_id, 'sensor_info' : message.sensor_name,
                  "alarm_type" : message.alarm_type, 'timestamp' : message.timestamp, 'alarm_id' : alarm.alarmID, 'info' : message.params}
        msg = AlarmNotificationMessage(alarm_args)
        res.setAlarm(msg)
        
    return res
    
    
decisions = {"AlarmResponse": __alarmResponse,
             "TokenResponse": __tokenResponse,
             "SensorAlert": __sensorResponse}    

def decideAction(message : Message):
    try:
        log.msg(f"Deciding on action for message: {message.type}.")
        return decisions[message.type](message)
    except KeyError as e:
        raise DecisionException(str(e), ErrorCodes.InvalidType.value, f"Message type: '{message.type}' is not supported")
    
    
def decideErr(failure : Failure):
    log.msg(f"In decideErr: {failure.value}")
    if type(failure.value) == DecisionException:
        log.msg(failure.value.__repr__())
    else:
        log.msg(str(failure.value))
    
    return ErrorMessage({'type' : "ErrorMessage", 'error_code' : failure.value.code})
    
    
#def msgToJson(message : Message):
#    return parse_MSG(message)


    