from asyncio import protocols
from twisted.internet.protocol import Factory
from .ApiProtocol import ApiProtocol
from client.network.AlarmClientFactory import AlarmClientFactory

class ApiFactory(AlarmClientFactory):
    
    protocol = ApiProtocol
    
    def __init__(self, service, api_url):
        self.service = service
        self.api_url = api_url
        
    def buildProtocol(self, addr):
        return ApiProtocol(self, addr)
