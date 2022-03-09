from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.interfaces import IAddress
from .ClientProtocol import ClientProtocol
from typing import Optional


class CFactory(ClientFactory):
    
    protocol = ClientProtocol
    
    def __init__(self, msg, timeout):
        self.msg = msg.encode()
        self.timeout = timeout
    
    def buildProtocol(self, addr: IAddress) -> "Optional[Protocol]":
        return ClientProtocol(self)