from twisted.internet.protocol import Protocol
from twisted.python.failure import Failure
from twisted.python import log
import json
from protocol.messages import RequireTokenMessage, SensorAlertResponseMessage

class MonitorProtocol(Protocol):
    
    def __init__(self, addr, factory):
        log.msg(f"Client created: '{addr}'")
        self.client_id = None
        self.addr = addr
        self.factory = factory
        self.d = None
        self.__resetCallbacks()
    
    def __resetCallbacks(self):
        self.d = self.factory.monitor_service.getMonitorCallbacks(self.send)
        
    def send(self, message : SensorAlertResponseMessage):
        
        msg = message.json
        
        self.transport.write(json.dumps(msg).encode())
        
        if message.alarm is not None:
            self.factory.monitor_service.triggerAlerts(message.alarm)
    
    def dataReceived(self, data: bytes):
        
        log.msg(f"Client: '{self.addr}'. Data received: '{data.decode()}'")
        self.d.callback(data)
        self.__resetCallbacks()
        
    def connectionMade(self):
        log.msg(f"Connection established to: '{self.addr}'")
        
    
    def connectionLost(self, reason: Failure = ...):
        log.msg(f"Connection lost from: '{self.addr}'. Exception: '{reason.value}'")
    
    