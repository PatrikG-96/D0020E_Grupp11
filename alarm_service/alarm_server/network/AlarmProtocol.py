from twisted.internet.protocol import Protocol
from twisted.internet.defer import Deferred
from twisted.python import failure
from twisted.python import log
from protocol.messages import RequireTokenMessage, Message
import json

class AlarmProtocol(Protocol):
    
    def __init__(self, addr, factory):
        log.msg(f"Client created: '{addr}'")
        self.client_id = None
        self.addr = addr
        self.factory = factory
        self.d = None
        self.__resetCallbacks()
    
    def __resetCallbacks(self):
        self.d = self.factory.controller_service.getAlarmCallbacks(self.send)
        
    def send(self, message : Message):
        
        msg = message.json
        disconnect = False
        if msg['type'] == "TokenAuthResult":
            
            if msg['success'] == True:
                self.client_id = msg['client_id']          
                self.factory.register(self)
        
            if msg['success'] == False:
                
                disconnect = True
        log.msg(f"(Client:{self.client_id}) Sending!")
        self.transport.write(json.dumps(msg).encode())    
        
        if disconnect:
            self.transport.loseConnection()
        
    
    def dataReceived(self, data: bytes):
        log.msg(f"Client: '{self.addr}'. Data received: '{data.decode()}'")
        self.d.callback(data)
        self.__resetCallbacks()
        
    def connectionMade(self):
        log.msg(f"Connection established to: '{self.addr}'")
        msg = RequireTokenMessage.require_auth()
        json_data = msg.json
        self.transport.write(json.dumps(json_data).encode())
    
    def connectionLost(self, reason: failure.Failure = ...):
        self.factory.deregister(self)
        log.msg(f"Connection lost from: '{self.addr}'. Exception: '{reason.value}'")
    
    