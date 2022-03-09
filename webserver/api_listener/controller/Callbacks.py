from twisted.internet import reactor
from twisted.python import log
from twisted.python.failure import Failure
from protocol.parse import *
from protocol.exceptions import ProtocolException
from protocol.messages import ErrorCodes
import json
from controller.CallbackExceptions import *
from copy import deepcopy
from database.database import getMonitor, getSubscribers, getUserDeviceSubscriptions

supported_alarms = []

class UnsupportedAlarmException(ProtocolException):
    
    def __init__(self, message: str, code : int):
        super().__init__(message, code)
        
    
    def __repr__(self) -> str:
        return f"Error code: '{self.code}'. Unsupported alarm error: {self.message}"
     


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

def __alarmNotification(message : AlarmNotificationMessage):
    
    if message.alarm_type not in supported_alarms:
        log.msg(f"Received unsupported alarm type: {message.alarm_type}.")
        raise UnsupportedAlarmException(f"Alarm type: {message.alarm_type} is not supported", ErrorCodes.UnsupportedAlarm.value)
    
    return message
    
def __requireToken(message: RequireTokenMessage):
    response = Message({"type" : "TokenResponse"})
    return response

def __tokenAuthResult(message : TokenAuthResultMessage):
    
    if not message.succeeded:
        reactor.stop()
    
    return message

    
decisions = {"AlarmNotification": __alarmNotification,
             "RequireToken" : __requireToken,
             "TokenAuthResult" : __tokenAuthResult}    

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


    