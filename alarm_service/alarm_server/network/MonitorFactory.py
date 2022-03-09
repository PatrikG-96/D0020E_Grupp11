from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet.interfaces import IAddress
from typing import Optional
from .MonitorProtocol import MonitorProtocol

class MonitorFactory(ServerFactory):
    
    protocol = MonitorProtocol
    
    def __init__(self, monitor_controller):
        self.monitor_service = monitor_controller
    
    def buildProtocol(self, addr: IAddress) -> "Optional[Protocol]":
        proto = MonitorProtocol(addr, self)
        return proto