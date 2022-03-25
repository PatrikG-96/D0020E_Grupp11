from .Sensor import MQTTSensor

class MqttHandler:
    
    """
    Gathers multiple MQTT sensors to allow for connecting and starting multiple sensors
    in one go.
    
    Attributes
    ----------
    sensor : dict
        dictionary mapping sensor id to sensor object
    monitor : Monitor
        the shared Monitor parent of all sensors
        
    Methods
    -------
    addSensor(sensor : MQTTSensor)
        Adds the sensor to the handler
    registerSensor(args : dict)
        Used as a callback for the MQTT sensor connecting to the broker. Will automatically register
        it with the Monitor
    deregisterSensor(args : dict)
        Used as a callback for the MQTT sensor disconnecting from the broker. Will automatically deregister
        it with the Monitor
    connectSensors()
        Loop through all sensors and connect them
    start()
        Loop through all sensors and start them
    """
        
    def __init__(self, monitor):
        """
        Create the handler
        
        Parameters
        ----------
        monitor : Monitor
            Monitor to be used for all sensors in this handler
        """
        self.sensor = {}
        self.monitor = monitor
        
    def addSensor(self, sensor:MQTTSensor):
        
        """
        Add the sensor to this handler
        
        Parameters
        ----------
        sensor : MQTTSensor
            the sensor to add to the handler
        """
        
        self.sensor[sensor.id] = sensor
        sensor.setConnectCallback(self.registerSensor)
        sensor.setDisonnectCallback(self.deregisterSensor)
        
    def registerSensor(self, args : dict):
        """
        Function that can be used as a callback for a MQTT sensors connectCallback. Will result in the
        sensor registering with the monitor when connected.
        
        Parameters
        ----------
        args : dict
            python dictionary which at least contains key "sensor" with the value being a reference to the sensor
        """
        args['sensor'].setMonitor(self.monitor)
        
    def deregisterSensor(self, args : dict):
        """
        Function that can be used as a callback for a MQTT sensors disconnectCallback. Will result in the
        sensor deregistering with the monitor when disconnected.
        
        Parameters
        ----------
        args : dict
            python dictionary which at least contains key "sensor" with the value being a reference to the sensor
        """
        sensor = args['sensor']
        try:
            sensor.monitor = None
            del self.sensor[sensor.id]
        except Exception as e:
            print(e)
            
    def connectSensors(self):
        """
        Connect all sensors in this handler
        """
        for key, sensor in self.sensor.items():
            sensor.connect()
            
    def start(self):
        """
        Start all sensors in this handler
        """
        for key,sensor in self.sensor.items():
            sensor.start()
            
    def __str__(self):
        s = ""
        for sensor in self.sensor:
            s += str(sensor) + "\n"
            
        return s