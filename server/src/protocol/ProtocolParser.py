
from .messages.Header import  Header
from .messages.MessageTypes import MessageTypes
from .messages.AlarmMessage import AlarmMessage
from .messages.AlarmResponse import AlarmResponse
from .messages.HistoryRequest import HistoryRequest
from .messages.HistoryResponse import HistoryResponse
from .messages.LoginMessage import LoginMessage
from .messages.LoginResponse import LoginResponse
from .messages.RegisterMessage import RegisterMessage
from .messages.RegisterResponse import RegisterResponse
from .messages.FullMessage import FullMessage




class ProtocolParser:


    @staticmethod
    def parseProtocolString(string):

        substrings = string.split(';')

        header_string = substrings[0]
        message_string = substrings[1]


        head = ProtocolParser.__parseHeaderString(header_string)
        msg = ProtocolParser.__parseMessageString(message_string, head.getType())

        result = FullMessage()
        result.setHeader(head)
        result.setMessage(msg)

        return result

    @staticmethod
    def __parseMessageString(string, type):

        params = ProtocolParser.__parseParameters(string)

        switch_cases = {MessageTypes.LoginMessage : LoginMessage.fromDict,
                        MessageTypes.LoginResponce : LoginResponse.fromDict,
                        MessageTypes.RegisterMessage : RegisterMessage.fromDict,
                        MessageTypes.RegisterResponce : RegisterResponse.fromDict,
                        MessageTypes.AlarmMessage : AlarmMessage.fromDict,
                        MessageTypes.AlarmResponce : AlarmResponse.fromDict,
                        MessageTypes.HistoryRequest : HistoryRequest.fromDict,
                        MessageTypes.HistoryResponce : HistoryResponse.fromDict}
        
        func = switch_cases[type]

        return func(params)
        
    
    @staticmethod
    def __parseHeaderString(string):

        substrings = string.split('/')

        version_string = substrings[0]
        type_string = substrings[1]
        options_string = substrings[2]

        options = ProtocolParser.__parseParameters(options_string)
        
        type = MessageTypes[type_string]

        params_dict = {'version' : version_string, 'type' : type, 'options' : options}

        header = Header.fromDict(params_dict)

        return header


    @staticmethod
    def __parseParameters(params_string):
        
        substrings = params_string.split('[')
        type = substrings[0]
        params = substrings[1][:-1]

        return ProtocolParser.__splitParams(params)

    @staticmethod
    def __splitParams(params):
        
        field_values = params.split(', ')
        result = {}
        for val in field_values:

            field, value = val.split(':')

            result[field] = value

        return result

