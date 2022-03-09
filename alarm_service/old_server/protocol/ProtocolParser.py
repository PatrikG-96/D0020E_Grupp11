
from .messages import *
from twisted.python import log



class ProtocolParser:


    @staticmethod
    def parseProtocolString(string):
        #log.msg("In parseProtocolString")
        substrings = string.split(';')

        header_string = substrings[0]
        message_string = substrings[1]


        head = ProtocolParser.__parseHeaderString(header_string)
        #log.msg(f"Header parsed, from {header_string} to {head}")

        msg = ProtocolParser.__parseMessageString(message_string, head.getType())

        result = FullMessage()
        result.setHeader(head)
        result.setMessage(msg)

        return result

    @staticmethod
    def __parseMessageString(string, type):
        #log.msg("In parseMessageString")
        params = ProtocolParser.__parseParameters(string)

        switch_cases = {MessageTypes.LoginMessage : LoginMessage.fromDict,
                        MessageTypes.LoginResponse : LoginResponse.fromDict,
                        MessageTypes.RegisterMessage : RegisterMessage.fromDict,
                        MessageTypes.RegisterResponse : RegisterResponse.fromDict,
                        MessageTypes.AlarmMessage : AlarmMessage.fromDict,
                        MessageTypes.AlarmResponse : AlarmResponse.fromDict,
                        MessageTypes.HistoryRequest : HistoryRequest.fromDict,
                        MessageTypes.HistoryResponse : HistoryResponse.fromDict}
        
        func = switch_cases[type]

        return func(params)
        
    
    @staticmethod
    def __parseHeaderString(string):

        substrings = string.split('/')

        version_string = substrings[0]
        type_string = substrings[1]
        options_string = substrings[2]

        options = ProtocolParser.__parseParameters(options_string)
        
        params_dict = {'version' : version_string, 'type' : type_string, 'options' : options}

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
