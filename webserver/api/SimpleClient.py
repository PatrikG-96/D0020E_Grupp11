from twisted.internet.protocol import Protocol, ClientFactory
from twisted.python import log, failure

class Proto(Protocol):
    
    def __init__(self, addr, factory):
        self.addr = addr
        self.factory = factory
        
    def connectionMade(self):
        log.msg(f'Connection made with: {self.addr}')
        
    def dataReceived(self, data: bytes):
        log.msg(f'Data received: {data.decode()}')
    
    def connectionLost(self, reason: failure.Failure = ...):
        log.msg(f'Connection lost from: {self.addr}, reason: {reason}')
        

class Fact(ClientFactory):
    
    protocol = Proto
    
    def __init__(self, service):
        self.service = service
        
    def buildProtocol(self, addr):
        proto = Proto(addr, self)
        return proto
    
