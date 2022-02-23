from threading import Thread
import json
from client.ClientGenerator import ClientGenerator
import logging

log = logging.getLogger()

class Monitor:
    
    def __init__(self, client_generator):
        self.client_generator = client_generator
        self.sensors = {}
        
    def registerSensor(self, sensor):
        try:
            self.sensors[sensor.id] = sensor
        except Exception as e:
            log.error(f"(Monitor) Adding sensor '{sensor.id}' failed with error : '{e}'")
        log.info(f"(Monitor) Added sensor '{sensor.id}' to Monitor")
        
    def deregisterSensor(self, sensor):
        try:
            del self.sensors[sensor.id]
        except Exception as e:
            log.error(f"(Monitor) Deleting sensor '{sensor.id}' failed with error: '{e}'")
        log.info(f"(Monitor) Deleted sensor '{sensor.id}'")
    
    def sendData(self, message):
        if type(message) == dict:
            msg = json.dumps(message)
        self.client_generator.sendMessage(msg)
        
    