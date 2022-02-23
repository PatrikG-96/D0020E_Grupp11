from .Client import Client
from threading import Thread


class ClientGenerator:
    
    def __init__(self, addr, port, timeout):
        self.addr = addr
        self.port = port
        self.client_timeout = timeout
        
    def sendMessage(self, message):
        
        client = Client(self.addr, self.port, message, self.client_timeout)
        client.start()
        
    
        