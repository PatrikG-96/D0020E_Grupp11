from twisted.internet.protocol import Protocol
from twisted.python import log
from twisted.internet.defer import Deferred

class AlarmProtocol(Protocol):


    def __init__(self, address, factory):
        self.addr = address
        self.factory = factory
        self.d = None
        self.resetDeferred()
        
    # Make a recycler or something for this 
    def resetDeferred(self):
        self.d = Deferred()
        self.factory.service.addClientCallbacks(self.d)
        self.d.addCallbacks(self.sendMsg, lambda x: log.msg(f"Error: {x}"))

    def connectionMade(self):
        self.factory.numProtocols = self.factory.numProtocols + 1
        log.msg(f'Connection recieved from: {self.addr}')
        self.transport.write(f'You have connected. There are currently {self.factory.numProtocols} open connections'.encode())

    def connectionLost(self, reason):
        self.factory.numProtocols = self.factory.numProtocols - 1
        log.msg(f"Client: {self.addr!r}, connection lost")

    def dataReceived(self, data):
        log.msg(f"Message recieved on client: {self.addr!r}. Data: {data.decode()!r}")
        self.d.callback(data.decode())
        self.resetDeferred()

    def sendMsg(self, msg):
        log.msg(f"Sending message: {msg!r}")
        self.transport.write(msg.encode())