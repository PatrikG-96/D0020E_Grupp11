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

def __tokenResponse(message : TokenResponseMessage):
    
    """Defines actions taken when receiving a TokenResponseMessage from a client
       Will verify the user credentials along with the serveraccess token, if successful
       the user is authenticated, if not the user will eventually be disconnected.

    Parameters
    ----------
    message : TokenResponseMessage
        The TokenResponse message to act on
        
    Returns
    -------
    A TokenAuthResultMessage object, with the success field set to True if authentication succeeded,
    or false if it failed
    """
    
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
    
    """Defines actions taken when receiving an AlarmResponse message from a client. Will update the
       database accordingly if the message is valid.

    Parameters
    ----------
    message : AlarmResponseMessage
        The protocol AlarmResponseMessage to decide the response for
        
    Returns
    -------
    An AlarmResponseConfirmationMessage object, that can be used to let the client know the response was successful
    """
    success = False
    try:
        if message.reponse_type == "READ":
            readAlarm(int(message.alarm_id), int(message.client_id), message.timestamp)
        if message.reponse_type == "RESOLVED":
            resolveAlarm(int(message.alarm_id), int(message.client_id), message.timestamp)
        success = True
    except Exception as e:
        log.msg(f"Responding to message failed with error: " + str(e))
        
    if success:
        return AlarmResponseConfirmationMessage.success(message.json)
    return AlarmResponseConfirmationMessage.failure(message.json)
    
    
def __sensorResponse(message : SensorAlertMessage):
    
    """Defines actions taken when receiving an SensorAlert message from a client. Will update the
       database with a new accordingly if the message is valid. If the alarm type is severe enough
       (defined in protocol), an AlarmNotificationMessage object is created.

    Parameters
    ----------
    message : SensorAlertMessage
        The protocol SensorAlertMessage to decide the response for
        
    Returns
    -------
    A SensorAlertResponseMessage object. If the alarm needs to be sent out to client, the "alarm" field is set.
    """

    #Get the sensor ID, then the monitor ID of the sensor
    sensor = getSensor(message.sensor_id)
    monitor = getSensorMonitor(sensor.sensorID)
    
    #Create a new alarm in the database using the message and the monitor ID
    alarm = setNewAlarm(monitor.monitorID, message.alarm_type, message.timestamp)
    
    #JSON for a response message
    args = {'type' : "SensorAlertResponse", 'received' : False}
    
    #This may be redundant. Might have a use for a more complex system?
    args['received'] = True
    
    #Create the message objet
    res = SensorAlertResponseMessage(args)
    
    # Check if this alarm type means we need to alert
    if ALARM_TYPE_ACTION[message.alarm_type]:
        
        #Create the alarm notification manually by defining the JSON
        alarm_args = {'type' : 'AlarmNotification', 'monitor_id' : monitor.monitorID, 'sensor_id' : message.sensor_id, 'sensor_info' : message.sensor_name,
                  "alarm_type" : message.alarm_type, 'timestamp' : message.timestamp, 'alarm_id' : alarm.alarmID, 'info' : message.params}
        msg = AlarmNotificationMessage(alarm_args)
        res.setAlarm(msg) # The way protocols know that alerts need to be triggered
        
    return res
    

# Maps message type to its corresponding function
decisions = {"AlarmResponse": __alarmResponse,
             "TokenResponse": __tokenResponse,
             "SensorAlert": __sensorResponse}    

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
    


    