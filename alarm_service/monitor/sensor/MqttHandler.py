from .Sensor import MQTTSensor

class MqttHandler:
    
    def __init__(self, monitor):
        self.sensor = {}
        self.monitor = monitor
        
    def addSensor(self, sensor:MQTTSensor):
        self.sensor[sensor.id] = sensor
        sensor.setConnectCallback(self.registerSensor)
        sensor.setDisonnectCallback(self.deregisterSensor)
        
    def registerSensor(self, args : dict):
        args['sensor'].setMonitor(self.monitor)
        
    def deregisterSensor(self, args : dict):
        sensor = args['sensor']
        try:
            sensor.monitor = None
            del self.sensor[sensor.id]
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