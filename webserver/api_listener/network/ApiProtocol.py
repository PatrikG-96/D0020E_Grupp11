from twisted.internet.protocol import Protocol
from twisted.internet.defer import Deferred
from twisted.python import log
import treq

class ApiProtocol(Protocol):
    
    def __init__(self, addr, factory):
        log.msg("In Protocol constructor")
        self.addr = addr
        self.factory = factory
        self.d = self.makeCallbackChain()
        
        
    def makeCallbackChain(self):
        log.msg("Adding callbacks to Protocol deferred")
        d = Deferred()
        self.factory.service.setParsingCallbacks(d)
        d.addCallback(self.alert)
        return d
        
    def dataReceived(self, data: bytes):
        log.msg(f'Received data: {data.decode()!r}')
        self.d.callback(data)
        self.d = self.makeCallbackChain()
    
    def connectionMade(self):
        log.msg(f'Connection accepted from: {self.addr!r}')
    
    def connectionLost(self, reason):
        log.msg(f'Connection lost from {self.addr!r}')
    
    def alert(self, msg):
        log.msg("Alerting flask api")
        if msg != None: 
            d = treq.post(self.factory.api_url, msg)
            d.addCallback(self.print_response)
    
    def print_response(self, res):
        log.msg(f'API response: {res!r}')