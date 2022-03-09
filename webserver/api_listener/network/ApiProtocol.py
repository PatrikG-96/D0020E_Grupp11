from twisted.internet.protocol import Protocol
from twisted.internet.defer import Deferred
from twisted.python import log
from protocol.messages import Message, AlarmNotificationMessage, TokenResponseMessage
from twisted.internet import reactor
import json
import treq

class ApiProtocol(Protocol):
    
    def __init__(self, factory, addr):
        log.msg("In Protocol constructor")
        self.factory = factory
        self.addr = addr
        self.__resetCallbackChain()
        
        
    def __resetCallbackChain(self):
        self.d = self.factory.service.getCallbacks(self.act)
        
    def dataReceived(self, data: bytes):
        super().dataReceived(data)
        
        log.msg(f'Received data: {data.decode()!r}')
        self.d.callback(data)
        self.__resetCallbackChain()
    
    def connectionMade(self):
        log.msg(f'Connection accepted from: {self.addr!r}')
    
    def connectionLost(self, reason):
        log.msg(f'Connection lost from {self.addr!r}')
    
    def act(self, msg : Message):
        
        if msg==None:
            return
        
        if type(msg) == AlarmNotificationMessage: 
            log.msg(f"Alerting flask api: {self.factory.api_url}")
            
            d = treq.post(self.factory.api_url+"/alert", json.dumps(msg.json).encode(), reactor = reactor)
            d.addCallback(treq.text_content)
            d.addCallback(self.print_response)
        elif msg.type == "TokenResponse":
            
            response = TokenResponseMessage({'type' : msg.type, 'token' : self.factory.token, 'username' : self.factory.username,
                                             "password" : self.factory.password})
            self.transport.write(json.dumps(response.json).encode())
            
        elif msg.type == "TokenAuthResult":
            
            new_msg = {'userID' : self.factory.id, "jwt" : self.factory.jwt}
            
            d = treq.post(self.factory.api_url+ "/auth/client/connected", new_msg, reactor = reactor)
            d.addCallback(treq.text_content)
            d.addCallback(self.print_response)
    
    
    def print_response(self, res):
        log.msg(f'API response: {res!r}')