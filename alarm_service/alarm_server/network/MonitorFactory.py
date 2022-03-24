from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet.interfaces import IAddress
from typing import Optional
from .MonitorProtocol import MonitorProtocol

class MonitorFactory(ServerFactory):
    """An extension of twisted.internet.protocol.ServerFactory. Creates instances of MonitorProtocol for each client connection.
    
    Attributes
    ----------
    monitor_controller : MonitorController
        Used to get callbacks that are defined in the controller module
    
    Methods
    -------
    buildProtocol(addr : IAddress) -> MonitorProtocol
        Creates an instance of MonitorProtocol. Used in internal twisted processes
    """
    
    
    protocol = MonitorProtocol
    
    def __init__(self, monitor_controller):
        """Creates the factory

        Parameters
        ----------
        controller_service : MonitorController
            Controller for parsing and decision that client connection want access to
        """
        self.monitor_service = monitor_controller
    
    def buildProtocol(self, addr: IAddress) -> "Optional[Protocol]":
        #Default documentation should suffice
        proto = MonitorProtocol(addr, self)
        return proto