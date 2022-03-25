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
    """Extension of ProtocolException. Exception that indicates that the alarm received has an
    unsupported alarm type.
    """    
    def __init__(self, message: str, code : int):
        """Creates the exception.
        
        Parameters
        ----------
        message : str
            the error message
        code : int
            the error code, found in protocol
        """
        super().__init__(message, code)
        
    
    def __repr__(self) -> str:
        return f"Error code: '{self.code}'. Unsupported alarm error: {self.message}"
     

"""
This module contains all callbacks used in controller logics. These are defined to adhere to twisted Deferred callback chains,
and therefore are suited for use in that context. Each callback also has an appropriate errback defined. These should be added
in the following step after adding its respective callback. For example, using callback decode() with twisted Deferred should look 
something like this:

d = Deferred()
d.addCallbacks(decode, arbitrary_errback)
d.addCallbacks(next_step, decodeErr) 

where arbitrary_errback is any errback that may be needed at that point, and next_step refers to the next callback that should be
executed after decode().
ErrBacks in this module do not resolve anything, they propagate the error to the next step all the way through the callback chain.
Using these callbacks in a logical order will result in a protocol ErrorMessage object containing an appropriate error code if an
exception occurs at any step. The exception will also be logged using twisted.python.log.
"""

def decode(bytes):
    """Decodes bytes into a string

    Parameters
    ----------
    bytes : bytes
        Raw bytes to be decoded
        
    Returns
    -------
    String result from decoding argument bytes
    
    Raises
    ------
    DecodeException
        Raised when decoding failed for any reason. 
    """
    try:
        return bytes.decode()
    except Exception as e:
         raise DecodeException(str(e), ErrorCodes.InvalidEncoding)
        
def decodeErr(failure : Failure):
    """errBack for decode() function, to be used in twisted Deferred context
       Does not resolve the error, simply logs it and triggers the next errBack.

    Parameters
    ----------
    failure : Failure
        Twisted Failure object wrapping an exception that occured
        
    Raises
    ------
    Exception
        The exception that the twisted Failure object is wrapping will be raised again, whatever it is
    """
    log.msg(f"In decodeErr: {failure.value}")
    if type(failure.value) == DecodeException:
        log.msg(failure.value.__repr__())
    failure.raiseException()

def toJson(data : str):
    """Parses a string into a JSON object, or in other words a python dictionary

    Parameters
    ----------
    data : str
        A utf-8 string to be parsed into JSON format
        
    Returns
    -------
    A python dictionary representing the JSON object
    
    Raises
    ------
    JsonException
        Raised when parsing failed, whatever the reason may be
    """
    log.msg(f"Attempting to parse {data} to JSON format")
    try:
        return json.loads(data)
    except Exception as e:
        raise JsonException(f"Failed at parsing JSON with error {e}", ErrorCodes.InvalidJson, data)

def jsonErr(failure: Failure):
    """errBack for toJson() function, to be used in twisted Deferred context
       Does not resolve the error, simply logs it and triggers the next errBack.

    Parameters
    ----------
    failure : Failure
        Twisted Failure object wrapping an exception that occured
        
    Raises
    ------
    Exception
        The exception that the twisted Failure object is wrapping will be raised again, whatever it is
    """
    log.msg(f"In jsonErr: {failure.value}")
    # If the error is supposed to be handled by this errback, log it
    if type(failure.value) == JsonException:
        log.msg(failure.value.__repr__())
    # If parsing to JSON failed, this needs to propagate through the callback chain
    failure.raiseException()

def parseJson(json: dict):
    """Parses a JSON object into a protocol message object.

    Parameters
    ----------
    json : dict
        JSON object to parse
        
    Returns
    -------
    A protocol message instance, any class inhereting protocol.messages.Message
    
    Raises
    ------
    FormatException
        Raised when the message does not comply with protocol specification
    UnknownException
        Raised when an unexpected exception occurs
    """
    log.msg(f"Attempting to parse {str(json)} into a Message object")
    return parse_JSON(json)

def parseErr(failure : Failure):
    """errBack for parseJson() function, to be used in twisted Deferred context
       Does not resolve the error, simply logs it and triggers the next errBack.

    Parameters
    ----------
    failure : Failure
        Twisted Failure object wrapping an exception that occured
        
    Raises
    ------
    Exception
        The exception that the twisted Failure object is wrapping will be raised again, whatever it is
    """
    
    log.msg(f"In parseErr: {failure.value}")
    # If the error is a FormatError raised by parse(), log it
    if type(failure.value) == FormatException:
        log.msg(failure.value.__repr__())            
    # Here, we either have a FormatException which is logged or a JsonException which is logged before
    # Both of these need to propagate, so we need to respond with an error message
    failure.raiseException()
    
# # # # # # # ## # # # # # # # # # # # # 


def __alarmNotification(message : AlarmNotificationMessage):
    
    """Parses a response to an AlarmNotificationMessage. If the alarm type is not supported, an exception occurs.
    Otherwise, the AlarmNotificationMessage is simply passed along.
    
    Parameters
    ----------
    message : AlarmNotificationMessage
        the alarm notification message received
        
    Returns
    -------
    If successful, the original AlarmNotificationMessage
    
    Raises
    ------
    UnsupportedAlarmException
        If the alarm type is not supported
    """
    
    if message.alarm_type not in supported_alarms:
        log.msg(f"Received unsupported alarm type: {message.alarm_type}.")
        raise UnsupportedAlarmException(f"Alarm type: {message.alarm_type} is not supported", ErrorCodes.UnsupportedAlarm.value)
    
    return message
    
def __requireToken(message: RequireTokenMessage):
    """Ugly solution, should be revised. When receiving a RequireToken message, simply
    create a generic message to indicate to the protocol that it needs to present a 
    TokenResponseMessage back.
    
    Parameters
    ----------
    message : RequireTokenMessage
        the RequireToken message received, unused as of now
        
    Returns
    -------
    A generic Message with type set to TokenResponse to tell the protocol that it needs to
    generate a real TokenResponse.
    """
    response = Message({"type" : "TokenResponse"})
    return response

def __tokenAuthResult(message : TokenAuthResultMessage):
    
    """Decides on action for a TokenAuthResult message. If the message indicates that connection
    was denied, program is shut down. Otherwise, the message is simply passed through
    
    Parameters
    ----------
    message : TokenAuthResultMessage
        the TokenAuthResult message to decide action for
    """
    
    if not message.succeeded:
        reactor.stop()
    
    return message

    
decisions = {"AlarmNotification": __alarmNotification,
             "RequireToken" : __requireToken,
             "TokenAuthResult" : __tokenAuthResult}    

def decideAction(message : Message):
    """Takes a protocol message and determines the appropriate action, resulting in a protocol
       response message.

    Parameters
    ----------
    message : Message
        The protocol message to decide action for
        
    Returns
    -------
    A protocol message that is a response for the parameter message
    
    Raises
    ------
    DecisionException
        Raised for any exception that may occur during the decision process. 
    """
    try:
        log.msg(f"Deciding on action for message: {message.type}.")
        return decisions[message.type](message)
    except KeyError as e:
        raise DecisionException(str(e), ErrorCodes.InvalidType.value, f"Message type: '{message.type}' is not supported")
    
    
def decideErr(failure : Failure):
    """errBack for decideAction() function, to be used in twisted Deferred context
       Does not resolve the error, simply logs it and triggers the next errBack.

    Parameters
    ----------
    failure : Failure
        Twisted Failure object wrapping an exception that occured
        
    Raises
    ------
    Exception
        The exception that the twisted Failure object is wrapping will be raised again, whatever it is
    """
    log.msg(f"In decideErr: {failure.value}")
    if type(failure.value) == DecisionException:
        log.msg(failure.value.__repr__())
    else:
        log.msg(str(failure.value))
    
    return ErrorMessage({'type' : "ErrorMessage", 'error_code' : failure.value.code})
    
    

    