from protocol.exceptions import FormatException, UnknownException
from protocol.messages import *
from protocol.schemas import *
from twisted.python import log
import traceback
#from exceptions import FormatException
#from messages import *
#from schemas import *

# TODO Move exception to its own file

def __require_token(msg_json):
    errors = require_token_schema.validate(msg_json)
    if errors:
        raise FormatException(f"Errors: {str(errors)}", ErrorCodes.InvalidMessageFormat.value, "RequireToken",  msg_json) 
    return RequireTokenMessage({"type" : "RequireToken"})

def __token_response(msg_json):
    print("Token res")
    errors = token_response_schema.validate(msg_json)
    if errors:
        raise FormatException(f"Error: {str(errors)}", ErrorCodes.InvalidMessageFormat.value, "TokenResponse",  msg_json)
    return TokenResponseMessage(msg_json) 
    
def __token_result(msg_json):
    
    errors = token_result_schema.validate(msg_json)
    if errors:
        raise FormatException(f"Error: {str(errors)}", ErrorCodes.InvalidMessageFormat.value, "TokenResult",  msg_json)
    return TokenAuthResultMessage(msg_json)

def __alarm_notification(msg_json):
    errors = alarm_notification_schema.validate(msg_json)
    if errors:
        raise FormatException(f"Error: {str(errors)}", ErrorCodes.InvalidMessageFormat.value, "AlarmNotification", msg_json)
    return AlarmNotificationMessage(msg_json)

def __alarm_response(msg_json):
    errors = alarm_response_schema.validate(msg_json)
    if errors:
        raise FormatException(f"Error: {str(errors)}", ErrorCodes.InvalidMessageFormat.value, "AlarmResponse", msg_json)
    return AlarmResponseMessage(msg_json)

def __sensor_alert(msg_json):
    errors = sensor_alert_schema.validate(msg_json)
    if errors:
        raise FormatException(f"Error: {str(errors)}", ErrorCodes.InvalidMessageFormat.value, "SensorAlert", msg_json)
    return SensorAlertMessage(msg_json)

__type_actions = {"RequireToken" : __require_token,
                  "TokenResponse" : __token_response,
                  "TokenAuthResult" : __token_result,
                  "AlarmNotification" : __alarm_notification,
                  "AlarmResponse" : __alarm_response,
                  "SensorAlert" : __sensor_alert}
    
    
def parse_JSON(msg_json : dict) -> Message:
    
    errors = message_schema.validate(msg_json)
    
    if errors:
        log.msg("Found format errors")
        raise FormatException(f"Errors: {str(errors)}", ErrorCodes.InvalidType.value,"Message", msg_json)
    
    func = __type_actions[msg_json['type']]
    try:
        res = func(msg_json)
        return res
    except Exception as e:
        #traceback.print_exc()
        raise UnknownException(e.__traceback__, ErrorCodes.UnknownError.value)
    

