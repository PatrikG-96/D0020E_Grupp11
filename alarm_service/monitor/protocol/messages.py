import enum
from copy import deepcopy

"""This module contains definitions of all messages in the Alarm Protocol in the form of classes.
   It also contains definitions of response types, a mapping between alarm type and whether or not
   the alarm should be forwarded to clients, a listing of all types and an enumeration of error codes"""

response_types = ['READ', 'RESOLVED']

ALARM_TYPE_ACTION = {'fall_detected' : False, 'fall_confirmed' : True}

__message_types = ["RequireToken", "TokenResponse", "TokenAuthResult",
                   "AlarmNotification", "AlarmResponse", "AlarmResponseConfirmation",
                   "SensorAlert", "SensorAlertResponse",
                   "ErrorMessage"]

class ErrorCodes(enum.Enum):
    
    """Defines protocol error codes.
       Key is the error code name, value is a numerical value usable in actual error messages
    """
    
    InvalidJson = 101,
    InvalidEncoding = 102,
    NoSuchAlarm = 201,
    UnsupportedAlarm = 202,
    InvalidToken = 301,
    InvalidClient = 302,
    InvalidResponse = 303,
    InvalidType = 304,
    InvalidMessageFormat = 305,
    UnknownError = 401
    

class Message:
    """
    The generic parent class of all protocol messages. The only field the message in JSON format.
    This can be used for easily translating between the two forms.
    
    Attributes
    ----------
    json : dict
        The message in JSON format
    """
    def __init__(self, json):
        """
        Create the message

        Parameters
        ----------
        json : dict
            The message in JSON format
        """
        self.type = json['type']
        self.json = json

class ErrorMessage(Message):
    """
    A generic message for communicating protocol errors. Extension of Message

    Attributes
    ----------
    error_code : int
        An error code from the ErrorCodes enum
    """
    def __init__(self, json):
        """
        Create the message

        Parameters
        ----------
        json : dict
            The message in JSON format
        """
        self.error_code = json['error_code']
        super().__init__(json)

class RequireTokenMessage(Message):
    
    """
    Representation of the RequireToken protocol message. A RequireToken message is a server to client message
    that tells the client that it needs to authenticate itself with a secret access token. Contains no unique
    fields, it's a generic message with the type fields set to RequireToken.
    
    Methods
    -------
    require_auth()
        Creates and returns a generic RequireToken message
    """
    
    def __init__(self, json):
        """
        Create the message

        Parameters
        ----------
        json : dict
            The message in JSON format
        """
        
        super().__init__(json)
        
    @staticmethod
    def require_auth():
        """
        Create a generic RequireToken message. This lets you avoid manually creating the dictionary for the message

        Returns
        -------
        A generic RequireToken message
        """
        return RequireTokenMessage({'type' : "RequireToken"})

class TokenResponseMessage(Message):
    
    """
    Representation of a response to a RequireToken message.
    
    Attributes
    ----------
    username : str
        username of the user
    password : str
        password of the user
    token : str
        server access token sent by the user
    """
    
    def __init__(self, json):
        """
        Create the message

        Parameters
        ----------
        json : dict
            The message in JSON format
        """
        
        self.username = json['username']
        self.password = json['password']
        self.token = json['token']
        super().__init__(json)

class TokenAuthResultMessage(Message):
    
    """
    Represents a response to a TokenResponseMessage. Indicates whether or not the authentication process
    was successful or not.
    
    Attributes
    ----------
    client_id : int
        id of the client that sent the TokenResponse
    success : bool
        whether or not authentication was successful
        
    Methods
    -------
    success(client_id : int)
        Creates and returns a TokenAuthResultMessage object for successful authentication given a client_id
    failure(client_id : int)
        Creates and returns a TokenAuthResultMessage object for failed authentication given a client_id
    """
    
    def __init__(self, json):
        self.client_id = json['client_id']
        self.succeeded = json['success']
        super().__init__(json)
        
    @staticmethod
    def success(client_id : int):
        """
        Creates and returns a TokenAuthResultMessage object for successful authentication given a client_id

        Parameters
        ----------
        client_id : int
            id of the client
            
        Returns
        -------
        A TokenAuthResultMessage object for successful authentication given a client_id
        """
        return TokenAuthResultMessage({'type': "TokenAuthResult",'success' : True, 'client_id' : client_id})
    
    @staticmethod
    def failure(client_id : int):
        """
        Creates and returns a TokenAuthResultMessage object for failed authentication given a client_id

        Parameters
        ----------
        client_id : int
            id of the client
            
        Returns
        -------
        A TokenAuthResultMessage object for failed authentication given a client_id
        """
        return TokenAuthResultMessage({'type' : "TokenAuthResult", 'success' : False, 'client_id' : client_id})

class AlarmMessage(Message):
    
    """
    Represents a generic AlarmMessage. This should not be used on its own, see subclasses for more practical
    use cases
    
    Attributes
    ----------
    timestamp : str
        a timestamp in string format, should adhere to format "%Y-%m-%d %H:%M:%S"
    alarm_id : int
        unique ID generated by the database for this alarm
    info : dict
        generic information that could differ for different alarm
    """
    
    def __init__(self, json):
        """
        Create the message

        Parameters
        ----------
        json : dict
            The message in JSON format
        """
        self.timestamp = json['timestamp']
        self.alarm_id = json['alarm_id']
        self.info = json['info']
        super().__init__(json)

class AlarmNotificationMessage(AlarmMessage):
    
    """
    Represents an alarm notification that should be sent to listening clients.
    
    Attributes
    ----------
    alarm_type : str
        string representation of protocol defined alarm types
    sensor_id : str
        unique string identification of the sensor that generated the alarm
    monitor_id : int
        unique identifier of the monitor that sent the SensorAlert, created by the database
    sensor_info : str
        addition information on the sensor, for example "WideFind" for a WideFind sensor
    """
    
    def __init__(self, json):
        """
        Create the message

        Parameters
        ----------
        json : dict
            The message in JSON format
        """
        self.alarm_type = json['alarm_type']
        self.sensor_id = json['sensor_id']
        self.monitor_id = json['monitor_id']
        self.sensor_info = json['sensor_info']
        super().__init__(json)

class AlarmResponseMessage(AlarmMessage):
    
    """
    Represents a response to an AlarmNotificationMessage by a client, marking it as either READ or SOLVED
    
    Attributes
    ----------
    response_type : str
        string representation of protocol response types, like READ or SOLVED
    client_id : int
        unique user ID
    """
    
    def __init__(self, json):
        """
        Create the message

        Parameters
        ----------
        json : dict
            The message in JSON format
        """
        self.json = json
        self.reponse_type = json['response_type']
        self.client_id = json['client_id']
        super().__init__(json)
    
class AlarmResponseConfirmationMessage(AlarmResponseMessage):
    
    """
    Respone to an AlarmResponseMessage. Tells the client whether or not their AlarmResponse was successfully recorded.
    
    Attributes
    ----------
    success : bool
        whether or not the response was successfully processed
        
    Methods
    -------
    success(alarmResponseJson : dict)
        Creates an AlarmResponseConfirmation for the given alarm response, marking it as successful
    failure(alarmResponseJson : dict)
        Creates an AlarmResponseConfirmation for the given alarm response, marking it as failed
    """
    
    def __init__(self, json):
        """
        Create the message

        Parameters
        ----------
        json : dict
            The message in JSON format
        """
        self.succeeded = json['success']
        super().__init__(json)
        self.type = "AlarmResponseConfirmation"
        
    @staticmethod
    def success(alarmReponseJson):
        """
        Creates an AlarmResponseConfirmationMessage for a successfully processed alarm response.

        Parameters
        ----------
        alarmResponseJson : dict
            the AlarmResponseMessage to respond to in JSON format

        Returns
        -------
        A new AlarmResponseConfirmationMessage object with the success field set to true
        """
        args = deepcopy(alarmReponseJson)
        args['success'] = True
        return AlarmResponseConfirmationMessage(args)
    
    @staticmethod
    def failure(alarmReponseJson):
        """
        Creates an AlarmResponseConfirmationMessage for a unsuccessfully processed alarm response.

        Parameters
        ----------
        alarmResponseJson : dict
            the AlarmResponseMessage to respond to in JSON format

        Returns
        -------
        A new AlarmResponseConfirmationMessage object with the success field set to false
        """
        args = deepcopy(alarmReponseJson)
        args['success'] = False
        return AlarmResponseConfirmationMessage(args)
    
    
class SensorAlertMessage(Message):
    
    """
    Represents a protocol SensorAlertMessage sent from a monitor to indicate a situation has occured.
    
    Attributes
    ----------
    sensor_id : str
        identifier for the specific sensor that generated the alert
    sensor_name : str
        name of the sensor, for example "WideFind1"
    alarm_type : str
        string representation of a protocol alarm type
    timestamp : str
        a timestamp in string format, should adhere to format "%Y-%m-%d %H:%M:%S"
    params : dict
        addition information that is specific for the situation, like coordinates
    """
    
    def __init__(self, json):
        self.sensor_id = json['sensor_id']
        self.sensor_name = json['sensor_name']
        self.alarm_type = json['alarm_type']
        self.timestamp = json['timestamp']
        self.params = json['params']
        super().__init__(json)

class SensorAlertResponseMessage(Message):
    
    """
    Representation of a response to a SensorAlertMessage, to tells the monitor whether or not the message
    was successfully parsed and received
    
    Attributes
    ----------
    received : bool
        whether or not the message was successfully parsed and received
    alarm : AlarmNotificationMessage
        if the sensor alert should result in alerting clients, an AlarmNotificationMessage is attached
        
    Methods
    -------
    setAlarm(msg : AlarmNotificationMessage)
        Set the option alarm field to indicate that this alarm should be forwarded to clients
    """
    
    def __init__(self, json):
        self.received = json['received']
        self.alarm = None
        super().__init__(json)
            
    def setAlarm(self, msg: AlarmNotificationMessage):
        self.alarm = msg