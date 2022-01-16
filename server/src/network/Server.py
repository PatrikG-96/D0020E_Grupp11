import asyncio
import Handler

class Server:


    def __init__(self, bind_address, bind_port):
        self.address = bind_address
        self.port = bind_port
        self.handler = Handler()

    def setAddress(self, address):
        self.address = address

    def setPort(self, port):
        self.port = port

    def start_server(self):
        asyncio.start_server(self.handler.handle_clients(), self.address, self.port)

    

