from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import reactor
import json

"""
Purpose:
    Send faked/simulated Delehealth API messages to the api_listener instance

Usage:
    Requirements: api_listener instance running, flask api running
    Optional: instance of sse_client.py running
    Start script, which will send 4 messages 1 second apart to api_listener

Expected result:
    API listener recieves messages. Due to the fact that the type is fall_confirmed,
    API listener notifies Flask API by making a POST request to the /alert route.
    The alert API call will trigger events to a connected SSE client. This is either
    the browser or the sse_client script.
"""

class Proto(Protocol):

    def sendMessage(self, msg):
        print("sending message")
        self.transport.write(msg)

def proto_cb(proto):
    msg = str({"type" : "fall_confirmed", "device_id": 1}).replace('\'', '"')
    msg1 = str({"type" : "fall_confirmed", "device_id": 2}).replace('\'', '"')
    msg2 = str({"type" : "fall_confirmed", "device_id": 3}).replace('\'', '"')
    msg3 = str({"type" : "fall_confirmed", "device_id": 4}).replace('\'', '"')
    proto.sendMessage(msg.encode())
    reactor.callLater(1, proto.sendMessage, msg1.encode())
    reactor.callLater(2, proto.sendMessage, msg2.encode())
    reactor.callLater(3, proto.sendMessage, msg3.encode())
    reactor.callLater(4, proto.transport.loseConnection)

point = TCP4ClientEndpoint(reactor, "localhost", 9999)
d = connectProtocol(point, Proto())
d.addCallback(proto_cb)
reactor.run()
