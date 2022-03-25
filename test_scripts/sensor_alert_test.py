import socket
import json

###################################################
# Test script for generating a SensorAlert.       #
#-------------------------------------------------#
# This should result in an alarm being generated. #
# Any client should receive an alarm.             #
###################################################

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 8888))

print("hej")

args = {'sensor_id' : "67BA3CF4E0622323", "sensor_name" : "fallsensor", "alarm_type" : "fall_confirmed", 'timestamp' : "2022-03-07 17:02:34", "params" : {"coords": (15,43,100)},
                'type' : "SensorAlert"}

msg = json.dumps(args)

print(sock.getpeername())

sock.send(msg.encode())

data = sock.recv(512)

print(data)


    
