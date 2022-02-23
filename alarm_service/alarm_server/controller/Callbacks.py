from twisted.python import log
from twisted.python.failure import Failure
from protocol.parse import *
from protocol.exceptions import ProtocolException
from protocol.messages import ErrorCodes
import json
from controller.CallbackExceptions import *
from copy import deepcopy


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
    log.msg(f"Attemping to parse {data} to JSON format")
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
    
    # Verify that token exists in database.
    
    
    success = message.token == "1337"
    if success:
        return TokenAuthResultMessage.success(message.client_id)
    return TokenAuthResultMessage.failure(message.client_id)
    
def __alarmResponse(message : AlarmResponseMessage):
    
    # Update state of alarm, add action
    worked = True
    if worked:
        return AlarmResponseConfirmationMessage.success(message.json)
    return AlarmResponseConfirmationMessage.failure(message.json)
    
    
def __sensorResponse(message : SensorAlertMessage):
    
    # create the new alarm
    worked = True
    args = {'type' : "SensorAlertResponse", 'received' : False}
    if worked:
        args['received'] = True
    res = SensorAlertResponseMessage(args)
    
    # Get monitor id by using sensor id
    # sensor_info, right now just sensor name
    # alarm_id ... push to database then get the alarm again? or UUID?
    alarm_args = {'type' : 'AlarmNotification', 'monitor_id' : 1, 'sensor_id' : message.sensor_id, 'sensor_info' : message.sensor_name,
                  "alarm_type" : message.alarm_type, 'timestamp' : message.timestamp, 'alarm_id' : 1, 'info' : {}}
    
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
    
    return ErrorMessage({'type' : Types.ErrorMessage, 'error_code' : failure.value.code})
    
    
#def msgToJson(message : Message):
#    return parse_MSG(message)


    