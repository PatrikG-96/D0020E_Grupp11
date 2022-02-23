from http import client
from sensor.MqttHandler import MqttHandler
from sensor.Sensor import load_sensor_json
from monitor.Monitor import Monitor
from client.ClientGenerator import ClientGenerator
from protocol.messages import SensorAlertMessage
from dotenv import load_dotenv, find_dotenv
import os
import json

def main():
    
    load_dotenv(find_dotenv())
    
    addr = os.getenv("HOST")
    port = int(os.getenv('PORT'))
    timeout = int(os.getenv("TIMEOUT"))
    
    client_gen = ClientGenerator(addr, port, timeout)
    
    msg = SensorAlertMessage.make("1", "Test", "fall_detected", "2022-02-22 02:45:56",{'coords' : str((1,2,3))})
    stringified = json.dumps(msg.json)
    
    client_gen.sendMessage(stringified)
    
    #monitor = Monitor(client_gen)
    
    #file = open("data/sensor.json", 'r')
    #data = json.loads(file.read())    
    
    #sensor_list = load_sensor_json(data)
    
    #handler = MqttHandler(monitor)
    
    #for sensor in sensor_list:
    #    handler.registerSensor(sensor)
        
    #print(handler)
    
if __name__ == "__main__":
    main()