from twisted.internet.protocol import Protocol
from twisted.internet.defer import Deferred
from twisted.python import log
from protocol.messages import Message, AlarmNotificationMessage, TokenResponseMessage
from twisted.internet import reactor
import json
import treq

class ApiProtocol(Protocol):
    
    """Extension of twisted.internet.protocol.Protocol. Representation of a single client - server connection.
    
    Attributes
    ----------
    factory : ApiFactory
        parent factory of this protocol instance
    addr : IAddress
        representation of the connection information
    """
    
    def __init__(self, factory, addr):
        self.factory = factory
        self.addr = addr
        self.__resetCallbackChain()
        
        
    def __resetCallbackChain(self):
        """Reset the local twisted deferred object to reset the callback chain. Must be 
        called every time data is received for the callback chain to be triggerable again.
        """
        self.d = self.factory.service.getCallbacks(self.act)
        
    def dataReceived(self, data: bytes):
        """Called internally by twisted when data is received. Triggers the local deferred
        object.
        
        Parameters
        ----------
        data : bytes
            raw bytes received from the tcp connection
        """
        super().dataReceived(data)
        
        log.msg(f'Received data: {data.decode()!r}')
        self.d.callback(data)
        self.__resetCallbackChain()
    
    def connectionMade(self):
        #default docstrings should suffice
        log.msg(f'Connection accepted from: {self.addr!r}')
    
    def connectionLost(self, reason):
        #default docstrings should suffice
        log.msg(f'Connection lost from {self.addr!r}')
    
    def act(self, msg : Message):
        """Act on the parsed protocol message. Handles the alarm server authentication process and 
        forwards alarm to the web API.
        
        Parameters
        ----------
        msg : Message
            The message to act on
        """
        if msg==None:
            return
        
        # Forward the alarm to the web API
        if type(msg) == AlarmNotificationMessage: 
            log.msg(f"Alerting flask api: {self.factory.api_url}")
            
            d = treq.post(self.factory.api_url+"/alert", json.dumps(msg.json).encode(), reactor = reactor)
            d.addCallback(treq.text_content)
            d.addCallback(self.print_response)
        # Response to server with access token   
        elif msg.type == "TokenResponse":
            
            response = TokenResponseMessage({'type' : msg.type, 'token' : self.factory.token, 'username' : self.factory.username,
                                             "password" : self.factory.password})
            self.transport.write(json.dumps(response.json).encode())
        
        # If we received a successful token auth result, alert web api that we are connected to server
        elif msg.type == "TokenAuthResult":
            
            if msg.success:
                new_msg = {'userID' : self.factory.id, "jwt" : self.factory.jwt}
            
                d = treq.post(self.factory.api_url+ "/auth/client/connected", new_msg, reactor = reactor)
                d.addCallback(treq.text_content)
                d.addCallback(self.print_response)
    
    # nothing...
    def print_response(self, res):
        log.msg(f'API response: {res!r}')