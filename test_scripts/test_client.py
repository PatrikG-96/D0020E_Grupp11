from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor, defer, task
import requests
import treq
import json


######################################################
# Test script for connection process to alarm server #
#----------------------------------------------------#
# Will start a client, prompt for username and pass- #
# word, then perform the connection process.         #
######################################################

global username 
global password 

class TestProtocol(Protocol):
    
    def __init__(self, factory):
        self.factory = factory
    
    def dataReceived(self, data: bytes):
        print(data.decode())
        msg = json.loads(data.decode())
        
        if msg['type'] == "RequireToken":
            
            token_response = response = {'username' : self.factory.username, 'password': self.factory.password, 'type' : "TokenResponse", 
                        'token' : self.factory.token}
            self.transport.write(json.dumps(response).encode())

    
    def connectionMade(self):
        print("connected")
        return super().connectionMade()
    
    def connectionLost(self, reason):
        print("disconnected")
        return super().connectionLost(reason)
    
class TestFactory(ClientFactory):
    
    protocol = TestProtocol
    
    def __init__(self, username, password, token):
        self.username = username
        self.password = password
        self.token = token
    
    def buildProtocol(self, addr):
        return TestProtocol(self)

def connectToServer(arg):
    data = json.loads(arg)
    
    print(data["token"])
    print(data["ip"])
    print(data["port"])

    reactor.connectTCP(data['ip'], int(data['port']), TestFactory(username, password, data['token']))

username = input("username: ")    
password = input("password: ")

res = requests.post("http://localhost:5000/auth/user/login", {'username' : username, 'password' : password})

jwt = res.json()['accessToken']
uid = int(res.json()['userID'])

header = {'x-auth-token' : jwt}
post = {'user_id' : uid, "timestamp" : "2022-03-03 15:25:43"}
route = "/server/access/request"

d = treq.post("http://localhost:5000"+route, post, headers= header)
d.addCallback(treq.text_content)
d.addCallback(connectToServer)

reactor.run()
