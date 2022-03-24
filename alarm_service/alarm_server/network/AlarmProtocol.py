from twisted.internet.protocol import Protocol
from twisted.internet.defer import Deferred
from twisted.python import failure
from twisted.python import log
from protocol.messages import RequireTokenMessage, Message
import json

class AlarmProtocol(Protocol):
    """An extension of twisted.internet.protocol. Represents a single client connection to the server. More specifically,
       an instance of this class represents a client listening to and responding to alarms.
    
    Attributes
    ----------
    client_id : int
        unique ID of the client in the form of an integer
    addr : IAddress
        an instance of twisted.internet.interfaces.IAddress, represent the clients connection information
    factory : AlarmFactory
        the parent factory/creator of this protocol instance
    d : Deferred
        the callback chain to execute on receiving messages from the client, see twisted.internet.defer.Deferred
    
    Methods
    -------
    __resetCallbacks()
        Internal method that resets the local Deferred object, as it can only be triggered once. See twisted documentation for 
        Deferred objects for more information
    send(message : Message)
        Send the message object to the connected client. Converts message to string format.
    dataReceived(data : bytes)
        Extension of twisted.internet.protocol implementation. Triggers the callback chain.
    connectionMade()
        Extension of twisted.internet.protocol implementation. Logs the event and immediately sends a RequireToken message to the client
    connectionLost()
        Extension of twisted.internet.protocol implementation. Registers the client with the parent factory
    """
    
    def __init__(self, addr, factory):
        """Create a protocol instance

        Parameters
        ----------
        addr : IAddress
            An instance of twisted.internet.interfaces.IAddress, represents connection info of this client
        factory : AlarmFactory
            The parent AlarmFactory instance that created this protocol instance
        """
        log.msg(f"Client created: '{addr}'")
        self.client_id = None
        self.addr = addr
        self.factory = factory
        self.d = None
        #self.authorized = False
        self.__resetCallbacks()
    
    def __resetCallbacks(self):
        """Resets the local Deferred object, disregarding the old one. Must be called every time a message is received,
           as Deferred objects can only be triggered once.
        """
        self.d = self.factory.controller_service.getAlarmCallbacks(self.send)
        
    def send(self, message : Message):
        """Send a protocol message to the connected client. If the message is a TokenAuthResult message, checks if authentication
           failed or not. If it did, connection is closed.

        Parameters
        ----------
        message : Message
            An instance of a Protocol message
        """
        msg = message.json
        
        #Should be moved to controller logic - add client information to Deferred trigger argument
        disconnect = False
        if msg['type'] == "TokenAuthResult":
            
            #Client is successfully authenticated, register it with the factory
            if msg['success'] == True:
                self.client_id = msg['client_id']          
                self.factory.register(self)
                self.authorized = True
            #Client is not authenticated, close the connection
            elif msg['success'] == False:
                disconnect = True
        #Send response to client
        log.msg(f"(Client:{self.client_id}) Sending!")
        self.transport.write(json.dumps(msg).encode())    
        
        #Disconnect here to make sure we actually send the TokenAuthResult message before dropping connection
        if disconnect:
            self.transport.loseConnection()
         
    def dataReceived(self, data: bytes):
        """Called every time client sends data to the server. Triggers the Deferred callback chain which performs
           decoding, protocol parsing and response decisions.

        Parameters
        ----------
        data : bytes
            Raw data received from the client
        """
        log.msg(f"Client: '{self.addr}'. Data received: '{data.decode()}'")
        #if not self.authorized:
        #    log.msg(f"Client is not authorized. Ending connection")
        #    self.transport.loseConnection()
        #    return
        self.d.callback(data)
        self.__resetCallbacks()
        
    def connectionMade(self):
        """Called when the connection to the client is established. Immediately sends a RequireToken message to the client.
        """
        log.msg(f"Connection established to: '{self.addr}'")
        msg = RequireTokenMessage.require_auth()
        json_data = msg.json
        self.transport.write(json.dumps(json_data).encode())
    
    def connectionLost(self, reason: failure.Failure = ...):
        """Called when the connection to the client is lost. Deregisters the client from the parent factory.

        Parameters
        ----------
        reason : twisted.python.failure.Failure
            A Failure object wrapping the exception that caused the lost connection
        """
        self.factory.deregister(self)
        log.msg(f"Connection lost from: '{self.addr}'. Exception: '{reason.value}'")
    
    