from .Client import Client
from threading import Thread
import os,binascii


class ClientGenerator:
    
    def __init__(self, addr, port, timeout):
        self.addr = addr
        self.port = port
        self.client_timeout = timeout
        
    def sendMessage(self, id, message):
        client = Client(id, self.addr, self.port, message, self.client_timeout)
        client.start()
        
    
        