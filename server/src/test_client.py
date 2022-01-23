from twisted.internet.protocol import Protocol, ClientFactory




class EchoProtocol(Protocol):

    def __init__(self, factory):
        self.factory = factory
        self.index = 0

    def dataReceived(self, data):
        print(data.decode())
        if self.index < len(self.factory.messages):
            self.send()

    def connectionLost(self, reason):
        print("Connection lost")

    def connectionMade(self):
        print("Connection made")
        #self.transport.write(self.factory.messages[0].encode())
        #self.index+=1
        #self.transport.loseConnection()
        

    def send(self):
        print("sending to server")
        self.transport.write(self.factory.messages[self.index].encode())
        self.index+=1

class EchoFactory(ClientFactory):

    protocol = EchoProtocol

    def __init__(self):
       self.messages = ["AP1.0/LoginMessage/options[encoding:UTF-8];Message[username:patrik, password:password]",
                        "AP1.0/RegisterMessage/options[encoding:UTF-8];Message[username:patrik, password:password]",
                        "AP1.0/HistoryRequest/options[encoding:UTF-8];Message[user_id:123, device_id:1]"]
        #self.messages = ['hej','det','här','är','ett','test']

    def buildProtocol(self, address):
        return EchoProtocol(self)
    
from twisted.internet import reactor


factory = EchoFactory()
reactor.connectTCP('127.0.0.1', 3456, factory)
reactor.run()
