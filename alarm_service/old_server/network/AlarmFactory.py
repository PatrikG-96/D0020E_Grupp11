from .AlarmProtocol import AlarmProtocol
from twisted.internet.protocol import Protocol, Factory
from twisted.python import log

class AlarmFactory(Factory):

    protocol = AlarmProtocol

    def __init__(self, service):
        self.numProtocols = 0
        self.clients = []
        self.service = service
        log.msg(f'Factory set up with service: {type(self.service)!r}')


    def buildProtocol(self, address):
        client = AlarmProtocol(address, self)
        log.msg(f'Client created: {address!r}')
        self.clients.append(client)
        return client

    def sendToAll(self):
        for client in self.clients:
            client.transport.write("hej".encode())
