from twisted.internet.protocol import Protocol
from twisted.python.failure import Failure
from twisted.python import log
import json
from protocol.messages import RequireTokenMessage, SensorAlertResponseMessage

class MonitorProtocol(Protocol):
    """An extension of twisted.internet.protocol. Represents a single client connection to the server. More specifically,
       an instance of this class represents a Monitor sending SensorAlerts to the server.
    
    Attributes
    ----------
    client_id : int
        unique ID of the client in the form of an integer
    addr : IAddress
        an instance of twisted.internet.interfaces.IAddress, represent the clients connection information
    factory : MonitorFactory
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
        Extension of twisted.internet.protocol implementation.
    connectionLost()
        Extension of twisted.internet.protocol implementation. 
    """
    
    def __init__(self, addr, factory):
        """Create a protocol instance

        Parameters
        ----------
        addr : IAddress
            An instance of twisted.internet.interfaces.IAddress, represents connection info of this client
        factory : AlarmFactory
            The parent MonitorFactory instance that created this protocol instance
        """
        log.msg(f"Client created: '{addr}'")
        self.client_id = None
        self.addr = addr
        self.factory = factory
        self.d = None
        self.__resetCallbacks()
    
    def __resetCallbacks(self):
        """Resets the local Deferred object, disregarding the old one. Must be called every time a message is received,
           as Deferred objects can only be triggered once.
        """
        self.d = self.factory.monitor_service.getMonitorCallbacks(self.send)
        
    def send(self, message : SensorAlertResponseMessage):
        """Send a protocol message to the connected client. 

        Parameters
        ----------
        message : Message
            An instance of a Protocol message
        """
        msg = message.json
        
        self.transport.write(json.dumps(msg).encode())
        
        if message.alarm is not None:
            self.factory.monitor_service.triggerAlerts(message.alarm)
    
    def dataReceived(self, data: bytes):
        """Called every time client sends data to the server. Triggers the Deferred callback chain which performs
           decoding, protocol parsing and response decisions.

        Parameters
        ----------
        data : bytes
            Raw data received from the client
        """
        log.msg(f"Client: '{self.addr}'. Data received: '{data.decode()}'")
        self.d.callback(data)
        self.__resetCallbacks()
        
    def connectionMade(self):
        #Default documentation should suffice here
        log.msg(f"Connection established to: '{self.addr}'")
    
    def connectionLost(self, reason: Failure = ...):
        #Default documentation should suffice here
        log.msg(f"Connection lost from: '{self.addr}'. Exception: '{reason.value}'")
    
    