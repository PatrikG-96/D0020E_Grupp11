from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet.interfaces import IAddress
from typing import Optional
from network.AlarmProtocol import AlarmProtocol
from twisted.python import log
from twisted.internet.defer import Deferred


class AlarmFactory(ServerFactory):
    
    protocol = AlarmProtocol
    
    def __init__(self, controller_service):
        self.controller_service = controller_service
        controller_service.registerFactory(self)
        self.d = self.__makeDeferred()
        self.clients = {}
    
    def buildProtocol(self, addr: IAddress) -> "Optional[Protocol]":
        proto = AlarmProtocol(addr, self)
        return proto
    
    def __makeDeferred(self):
        d = Deferred()
        d.addCallback(self.notifyClients)
        return d
    
    def trigger(self, ids: list, message : str):
        args = (ids, message)
        print("should callback")
        self.d.callback(args)
        self.d = self.__makeDeferred()
    
    def notifyClients(self, args):
        ids = args[0]
        message = args[1]
        for id in ids:
            if id in self.clients:
                self.clients[id].send(message)
    
    def register(self, proto : AlarmProtocol):
        log.msg(f"Client '{proto.client_id}' authorized. Registering.")
        self.clients[proto.client_id] = proto
        
    def deregister(self, proto : AlarmProtocol):
        if proto.client_id in self.clients:
            log.msg(f"Client '{proto.client_id}' deregistering.")
            del self.clients[proto.client_id]