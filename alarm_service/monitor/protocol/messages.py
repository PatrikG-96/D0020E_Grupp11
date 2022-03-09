import enum
from copy import deepcopy

response_types = ['READ', 'RESOLVED']

__message_types = ["RequireToken", "TokenResponse", "TokenAuthResult",
                   "AlarmNotification", "AlarmResponse", "AlarmResponseConfirmation",
                   "SensorAlert", "SensorAlertResponse",
                   "ErrorMessage"]

class Types(enum.Enum):
    
    RequireTokenMessage = 1,
    TokenResponseMessage = 2,
    TokenAuthResultMessage = 3,
    AlarmNotificationMessage = 4,
    AlarmResponseMessage = 5,
    AlarmResponseConfirmation = 6,
    ErrorMessage = 7,
    SensorAlertMessage = 8,
    SensorAlertResponseMessage = 9


class ErrorCodes(enum.Enum):
    
    InvalidJson = 101,
    InvalidEncoding = 102,
    NoSuchAlarm = 201,
    InvalidToken = 301,
    InvalidClient = 302,
    InvalidResponse = 303,
    InvalidType = 304,
    InvalidMessageFormat = 305
    

class Message:
    
    def __init__(self, json):
        self.type = json['type']
        self.json = json

class ErrorMessage(Message):
    
    def __init__(self, json):
        self.error_code = json['error_code']
        super().__init__(json)

class RequireTokenMessage(Message):
    
    def __init__(self, json):
        super().__init__(json)
        
    @staticmethod
    def require_auth():
        return RequireTokenMessage({'type' : "RequireToken"})

class TokenResponseMessage(Message):
    
    def __init__(self, json):
        self.client_id = json['client_id']
        self.token = json['token']
        super().__init__(json)

class TokenAuthResultMessage(Message):
    
    def __init__(self, json):
        self.client_id = json['client_id']
        self.succeeded = json['success']
        super().__init__(json)
        
    @staticmethod
    def success(client_id : int):
        return TokenAuthResultMessage({'type': "TokenAuthResult",'success' : True, 'client_id' : client_id})
    
    @staticmethod
    def failure(client_id : int):
        return TokenAuthResultMessage({'type' : "TokenAuthResult", 'success' : False, 'client_id' : client_id})

class AlarmMessage(Message):
    
    def __init__(self, json):
        self.timestamp = json['timestamp']
        self.alarm_id = json['alarm_id']
        self.info = json['info']
        super().__init__(json)

class AlarmNotificationMessage(AlarmMessage):
    
    def __init__(self, json):
        self.alarm_type = json['alarm_type']
        self.sensor_id = json['sensor_id']
        self.monitor_id = json['monitor_id']
        self.sensor_info = json['sensor_info']
        super().__init__(json)

class AlarmResponseMessage(AlarmMessage):
    
    def __init__(self, json):
        self.json = json
        self.reponse_type = json['response_type']
        self.client_id = json['client_id']
        super().__init__(json)
    
class AlarmResponseConfirmationMessage(AlarmResponseMessage):
    
    def __init__(self, json):
        self.succeeded = json['success']
        super().__init__(json)
        self.type = "AlarmResponseConfirmation"
        
    @staticmethod
    def success(alarmReponseJson):
        args = deepcopy(alarmReponseJson)
        args['success'] = True
        return AlarmResponseConfirmationMessage(args)
    
    @staticmethod
    def failure(alarmReponseJson):
        args = deepcopy(alarmReponseJson)
        args['success'] = False
        return AlarmResponseConfirmationMessage(args)
    
    
class SensorAlertMessage(Message):
    
    def __init__(self, json):
        self.sensor_id = json['sensor_id']
        self.sensor_name = json['sensor_name']
        self.alarm_type = json['alarm_type']
        self.timestamp = json['timestamp']
        self.params = json['params']
        super().__init__(json)
        
    @staticmethod
    def make(id, name, type, timestamp, params):
        args = {'sensor_id' : id, "sensor_name" : name, "alarm_type" : type, 'timestamp' : timestamp, "params" : params,
                'type' : "SensorAlert"}
        return SensorAlertMessage(args)

class SensorAlertResponseMessage(Message):
    
    def __init__(self, json):
        self.received = json['received']
        self.creator = None
        super().__init__(json)
            
    def setCreator(self, msg: SensorAlertMessage):
        self.creator = msg