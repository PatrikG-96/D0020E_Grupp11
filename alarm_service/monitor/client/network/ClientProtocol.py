from twisted.internet.protocol import Protocol
from twisted.python import failure
from twisted.internet import reactor

class ClientProtocol(Protocol):
    
    def __init__(self, factory):
        self.factory = factory
    
    def dataReceived(self, data: bytes):
        print(f"Received data: {str(data)}")
        self.transport.loseConnection()
        reactor.stop()
    
    def connectionLost(self, reason: failure.Failure = ...):
        print("Disconnected")
    
    def connectionMade(self):
        print("Connected")
        self.transport.write(self.factory.msg)
        reactor.callLater(self.factory.timeout, self.close())
        
    def close(self):
        reactor.stop()