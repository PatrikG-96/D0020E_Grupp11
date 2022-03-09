from http import client
from sensor.MqttHandler import MqttHandler
from sensor.Sensor import load_sensor_json
from monitor.Monitor import Monitor
from client.ClientGenerator import ClientGenerator
from protocol.messages import SensorAlertMessage
from dotenv import load_dotenv, find_dotenv
import os
import logging
import json

def main():
    
    load_dotenv(find_dotenv())
    
    open('logs.txt', 'w').close()

#    logging.basicConfig(filename = "logs.txt", level=logging.INFO)
    
    logging.basicConfig(level=logging.INFO)
    
    addr = os.getenv("HOST")
    port = int(os.getenv('PORT'))
    timeout = int(os.getenv("TIMEOUT"))
    
    client_gen = ClientGenerator(addr, port, timeout)
    
    
    monitor = Monitor(client_gen)
    
    file = open("data/sensor.json", 'r')
    data = json.loads(file.read())    
    
    sensor_list = load_sensor_json(data)
    
    handler = MqttHandler(monitor)
    
    for sensor in sensor_list:
        handler.addSensor(sensor)
        
    handler.connectSensors()
    handler.start()
    
    monitor.start()
    
if __name__ == "__main__":
    main()