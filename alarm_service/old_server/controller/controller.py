
from twisted.internet.defer import Deferred
from protocol import *
from twisted.python import log
from twisted.internet.defer import Deferred

class Controller():

    def __init__(self):
        pass
    
    def addClientCallbacks(self, client_deferred):
        client_deferred.addCallback(self.parseMessage)
        client_deferred.addCallbacks(self.decide_action, self.parseError)
        client_deferred.addCallbacks(self.messageToString, self.parseError)

    def parseMessage(self, res):
        log.msg(f'Parsing message: {res}.')
     
        msg = ProtocolParser.parseProtocolString(res)
      
        log.msg(f'Parsed message, type: {type(msg.getMessage())}, {msg}')
        return msg

    def decide_action(self, res):
        log.msg(f'Deciding action on message: {type(res)}.')
        if (res.header.type == MessageTypes.LoginMessage):
            return self.loginResponse(res)
        elif(res.header.type == MessageTypes.RegisterMessage):
            return self.registerResponse(res)
        elif(res.header.type == MessageTypes.HistoryRequest):
            return self.historyResponse(res)
    
    def loginResponse(self, res):
        log.msg(f'Received LoginMessage, parsing response.')
        fields = {'username': res.getMessage().getUsername(), 'password' : res.getMessage().getPassword()}
        response = LoginResponse.fromDict(fields)
        res.getHeader().setType('LoginResponse') ## stupid, fix
        return FullMessage.build(res.getHeader(), response)
    
    # TODO: Database integration
    def registerResponse(self, res):
        log.msg(f'Received RegisterMessage, parsing response.')
        fields = {'user_id' : 123}  # just for testing
        response = RegisterResponse.fromDict(fields)
        res.getHeader().setType('RegisterResponse') ## stupid, fix
        return FullMessage.build(res.getHeader(), response)
    
    def historyResponse(self, res):
        log.msg(f'Received HistoryRequest, parsing response.')
        fields = {'device_id' : 123, 'table_data':'NOTHING'}  # just for testing
        response = HistoryResponse.fromDict(fields)
        res.getHeader().setType('HistoryResponse') ## stupid, fix
        return FullMessage.build(res.getHeader(), response)

    def messageToString(self, res):
        log.msg("Parsing to string")
        return str(res)

    def parseError(self, res):
        log.msg(f"###Error: {res} ")
        return res