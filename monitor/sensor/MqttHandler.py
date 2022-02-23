from .Sensor import MQTTSensor

class MqttHandler:
    
    def __init__(self, monitor):
        self.sensor = {}
        self.monitor = monitor
        
    def registerSensor(self, sensor:MQTTSensor):
        self.sensor[sensor.id] = sensor
        sensor.setMonitor(self.monitor)
        
    def deregisterSensor(self, sensor_id):
        try:
            self.sensor.monitor = None
            del self.sensor[sensor_id]
        except Exception as e:
            print(e)
            
    def connectSensors(self):
        for key, sensor in self.sensor.items():
            sensor.connect()
            
    def start(self):
        for key,sensor in self.sensor.items():
            sensor.start()
            
    def __str__(self):
        s = ""
        for sensor in self.sensor:
            s += str(sensor) + "\n"
            
        return s