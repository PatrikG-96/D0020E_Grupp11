from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import reactor
import numpy as np
import datetime
from random import randrange
import json

global num_msgs
global time
global msg

def make_messages(n):
    times = np.random.uniform(0.0, time, n)
    types = np.random.randint(2, size=n)
    print(types)
    devices = np.random.randint(0,10,n)
    dates = random_timestamps(n)
    coords = random_coords(n, 0, 100)

    msg_list = []
    for i in range(0,n):
        msg_list.append(
            (times[i], 
            make_msg(types[i], devices[i], dates[i], coords[i]))
        )        

    return msg_list

def make_msg(mtype, device, date, coords):
    msg_type = "fall_confirmed" if mtype == 1 else "fall_detected"
    return str({"type" : msg_type, "device_id" : device, "timestamp" : str(date), "coords" : str(coords)}).replace('\'', '"')


def random_timestamps(iter):
    start = datetime.datetime.now()
    dates = []
    for i in range(0,iter):
        start = start + datetime.timedelta(minutes=randrange(10))
        dates.append(start)
    return dates

def random_coords(iter, min, max):
    coords = []
    for i in range(0,iter):
        coords.append((randrange(min, max), randrange(min,max)))
    return coords


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
        print(f"sending message: {msg}")
        self.transport.write(msg.encode())

def many_messages(proto):
    
    messages = make_messages(num_msgs)

    for msg in messages:
        reactor.callLater(msg[0], proto.sendMessage, msg[1])
    
    reactor.callLater(time+10, proto.transport.loseConnection)
    
def single_message(proto):
    
    reactor.callLater(1, proto.sendMessage, msg)

choice = int(input("What type of test? \n1 for sending randomized messages, 2 for sending one specified message\nChoice: "))


point = TCP4ClientEndpoint(reactor, "localhost", 9999)
d = connectProtocol(point, Proto())

if choice==1:
    
    num_msgs = int(input("How many messages: "))
    time = int(input("How long should messages be spaced out: "))
    d.addCallback(many_messages)
    
elif choice == 2:
    
    device = input("deviceID: ")
    type = input("type: ")
    print("Making timestamp and random coordinates")
    coords = random_coords(1, 0, 100)[0]
    now = datetime.datetime.now()
    msg = str({'device_id' : device, 'type' : type, 'coords' : str(coords), 'timestamp': str(now)}).replace('\'', '"')
    d.addCallback(single_message)

else:
    raise SystemExit


reactor.run()




