import abc
import paho.mqtt.client as mqtt
import logging
import json
from datetime import datetime, timedelta
from util.Timer import Timer
from monitor.Monitor import Monitor
from protocol.messages import SensorAlertMessage

log = logging.getLogger()

"""
This module contains a general Sensor class, along with some MQTT implementation and a single function
that creates FallSensors given a JSON from a sensor.json file. More sensor types could be supported by 
this function.
"""

class Sensor(object):
    
    """
    An abstract representation of a sensor.
    
    Attributes
    ----------
    id : str
        any type of unique identifier that a sensor may have
    monitor : Monitor
        the parent Monitor of the sensor
    name : str
        a name of the sensor
        
    Methods
    -------
    setMonitor(monitor : Monitor)
        Set the parent monitor of this sensor
    start()
        Start the sensor. After calling start, we should be receiving data from the sensor.
        Abstract method.
    connect()
        Connect to the sensor. After calling connect, there should be an established connection
        to the sensor, or all neccessary setup for starting the sensor should be completed.
        Abstract method.
    disconnect()
        Disconnect the sensor. Abstract method.
    parse(msg : str) -> dict
        Converts the data received from the sensor into a python dictionary. The msg parameter
        does not have to be a string. Abstract method.
    returnData(data : dict)
        Forwards data to the Monitor. The Monitor will pass it along to a client thread.
    """
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, id):
        """
        Create the Sensor
        
        Parameters
        ----------
        id : str
            an unique identifier for the sensor
        monitor : Monitor
            a Monitor instance to set as parent
        name : str
            name of the sensor
        """
        self.id = id
        self.monitor = None
        self.name = "Sensor"
        
    def setMonitor(self, monitor : Monitor):
        """
        Set the parent monitor of this sensor
        
        Parameters
        ----------
        monitor : Monitor
            a Monitor instance
        """
        self.monitor = monitor
    
    @abc.abstractmethod
    def start(self):
        """
        Start the sensor. Calling this method means that we can now receive data from the sensor.
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def connect(self):
        """
        Connect to the sensor. Calling this method means that we should be ready to start the sensor.
        """
        raise NotImplementedError
        
    @abc.abstractmethod
    def disconnect(self):
        """
        Disconnect from the sensor. Calling this method should mean that we no longer receive data from an
        already connected sensor.
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def parse(self, msg : str) -> dict:
        """
        Parse a message into a python dictionary.
        
        Parameters
        ----------
        msg : str
            Message to parse. Does not have to be a string in overloaded subclass methods
            
        Returns
        -------
        A python dictionary containing all fields from the original message.
        """
        raise NotImplementedError
    
    def returnData(self, data : dict):
        """
        Forwards data in the form of a python dictionary to the Monitors sendData method. It's up to the Monitor
        to decide what to do with it.
        
        Parameters
        ----------
        data : dict
            A python dictionary containing the message fields.
        """
        self.monitor.sendData(self.id, data)
    
    def __str__(self):
        return f"({self.name}:{self.id})"

class MQTTSensor(Sensor):
    
    """
    Extension of Sensor. Represents a sensor that uses MQTT. This class is abstract and won't function
    on its own. Subclass this for any type of sensor that uses MQTT. This class is based on paho.mqtt.
    
    Attributes
    ----------
    client : paho.mqtt.client
        a MQTT client instance
    addr : str
        the address of the MQTT broker
    port : int
        the port of the MQTT broker
    timeout : int
        a timeout value for the MQTT connection
    topic : str
        the topic to subscribe to
    connect_cb : function
        a callback to the called when connected to the broker
    disconnect_cb : function
        a callback to the called when disconnected from the broker
    
    Methods
    -------
    setConnectCallback(func : function)
        Set a callback for connecting to the broker
    setDisconnectCallback(func : function)
        Set a callback for disconnecting from the broker
    setTopic(topic : str)
        Set the topic to subscribe to
    """
    
    def __init__(self, id, addr, port, timeout):
        """
        Create the MQTTSensor
        
        Parameters
        ----------
        id : str
            unique ID of the sensor
        addr : str
            IP address of the MQTT broker
        port : int
            port of the MQTT broker
        timeout : int
            timeout value for MQTT connection                
        """
        self.client = mqtt.Client()
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnect
        self.timeout = addr
        self.addr = addr
        self.port = port
        self.timeout = timeout
        self.topic = None
        self.name = "MQTT"
        self.connect_cb = None
        self.disconnect_cb = None
        super().__init__(id)
        
    def setConnectCallback(self, func):
        """
        Set the connection callback function
        
        Parameters
        ----------
        func : function
            callback function to be called on connecting to the broker
        """
        self.connect_cb = func
    
    def setDisonnectCallback(self, func):
        """
        Set the disconnection callback function
        
        Parameters
        ----------
        func : function
            callback function to be called on disconnecting from the broker
        """
        self.disconnect_cb = func
    
    def setTopic(self, topic):
        """
        Set the topic to subscribe to
        
        Parameters
        ----------
        topic : str
            the topic to subscribe to.
        """
        self.topic = topic
    
    def connected(self, client, userdata, flags, rc):
        
        """
        Connection callback used in paho.mqtt.client when connecting
        """
        
        log.info(f"({self.name}:{self.id}) Sensor connected with result code: {rc}")
        if rc == 0:
            
            if self.connect_cb is not None:
        
                self.connect_cb({'sensor' : self})
                
        
    def disconnect(self, client, userdata, rc):
        """
        Disconnect callback used in paho.mqtt.client when disconnecting
        """
        log.warning(f"({self.name}:{self.id}) Sensor disconnected with result code: {rc}")
        
        if self.disconnect_cb is not None:
            self.disconnect_cb({'sensor' : self})
        
        self.connect()
    
    def connect(self):
        log.info(f"({self.name}:{self.id}) Attempting to connect: '(addr = {self.addr}, port = {self.port}, timeout = {self.timeout})'")
        self.client.connect(self.addr, self.port, self.timeout)
        
        
    def start(self):
        """
        Start the MQTT sensor. Subscribes to the topic, then start a new daemon thread for the 
        sensor to run in.
        """
        
        log.info(f"({self.name}:{self.id}) Sensor starting")
        self.client.subscribe(self.topic)
        self.client.loop_start()
        
class WideFind(MQTTSensor):
    
    """
    Extension of MQTTSensor. Represents a connection to WideFind sensor, with an implementation
    of Sensor.parse().
    """
    
    def __init__(self, id, addr, port, timeout):
        """
        Create the WideFind sensor
        
        Parameters
        ----------
        id : str
            unique ID of the sensor
        addr : str
            IP address of the MQTT broker
        port : int
            port of the MQTT broker
        timeout : int
            timeout value for MQTT connection                
        """
        super().__init__(id, addr, port, timeout)
        self.name = "WideFind"
        
    def parse(self, msg):
        
        """
        Parse the data received from WideFind sensors into a python dictionary.
        
        Parameters
        ----------
        msg : str
            A message in WideFind format. See WideFind documentation for more details
            
        Returns
        -------
        A python dictionary containing all fields found in the message string, or None
        if the message was for a sensor without this sensors ID.
        """
        
        stringified = msg.payload.decode('utf-8')
        json_data = json.loads(stringified)
        message = json_data['message']
        
        params = message.split(',')
        type_split = params[0].split(':')
        type = type_split[0]
        id = type_split[1]
        
        if type == "REPORT" and id == self.id:
           # log.info(f"({self.name}:{self.id}) Received report.")
            trimmed_time = json_data['time'].split('.')[0]
            time = str(datetime.strptime(trimmed_time, "%Y-%m-%dT%H:%M:%S"))
        
            result = {'id' : id, 'timestamp': time, 'version' : params[1], 
                      'x' : params[2], 'y' : params[3], 'z' : params[4],
                      'velX' : params[5], 'velY' : params[6], 'velZ' : params[7], 
                      'battery' : params[8], 'rssi' : params[9], 'timealive' : params[10]}
            
            return result
        else:
            return None
    

class FallSensor(WideFind):
    
    """
    Extension of WideFind. Uses data from WideFind to determine whether or not a situation seems to be
    a fall or not.
    
    Attributes
    ----------
    detected_limit : int
        A threshhold for the vertical position that should be interpreted as being a fall. Measured in millimeters.
        For example, a detected_limit of 200 means that a fall is detected when the sensor sends a position below 
        200 mm.
    resolved_limit : int
        Another threshhold for vertical position, but instead for when the fall should be interpreted as being resolved.
        A resolved_limit of 300 means that once we have deteremined that a fall is detected (using detected_limit), we cancel
        the fall before confirming it if at any point before confirmation the sensor sends a position above 300.
    grace_period : int
        A time value in seconds that describes how long we should wait after passing the detected_limit before detecting a fall.
        This value is mainly used to avoid having falls being detected immediatly when the sensor is dropped or anything like 
        that. Having a grace_period of 5 would mean that we wait for 5 seconds after passing the detected_limit before drawing
        the conclusion that a fall has been detected. 
    fall_timer : int
        A time value in seconds that defines how long we wait between detecting a fall and confirming it. A fall_timer of 
        60 seconds means that after a fall has been detected, we wait for 60 seconds before confirming the fall.
    active : bool
        Indicates whether or not the sensor is actively looking for falls. This is True until we detect a fall, where it 
        becomes False until the fall is resolved, where it is set to True again.
    timer : Timer
        A Timer object to trigger a callback function after a given time. Alternative to python signal library
        to support Windows        
        
    Methods
    -------
    __fall_detected(message : dict)
        Triggered by self.timer when a fall is detected, sends a message to server via the Monitor and starts
        a new Timer for fall confirmation
    __fall_confirmed(message : dict)
        Triggered by self.time when a fall is confirmed, sends a message to server via the Monitor and marks the 
        fall as resolved to allow for detecting new falls.
    """
    
    def __init__(self, id,addr, port, timeout, detected_limit, resolved_limit, grace_period, fall_timer):
        super().__init__(id, addr, port, timeout)
        self.name = "WideFind_FallSensor"
        self.client.on_message = self.__on_message
        self.detected_limit = detected_limit
        self.fall_timer = fall_timer
        print(f"falltimer: {self.fall_timer}")
        self.grace_period = grace_period
        self.resolved_limit = resolved_limit
        self.active = True
        self.timer = None    
    
    def __on_message(self, client, userdata, msg):
        data = super().parse(msg)
        
        if data is None:
            return
        print(f"{str(self)} : {(data['x'], data['y'], data['z'])}")
        
        if self.active and int(data['z']) < self.detected_limit:
            self.timer = Timer(str(self), self.grace_period, self.__fall_detected, data)
            self.timer.start()
            self.active = False
            
        if not self.active and int(data['z']) > self.resolved_limit:
            log.info(f"({self.name}:{self.id}) Fall resolved")
            self.timer.stop()
            self.active = True
    
        
    def __fall_detected(self, message):
        
        """
        Callback for when a fall is detected. Sends the a message to the server and starts a Timer for 
        confirming the fall.
        
        Parameters
        ----------
        message : dict
            the message in dictionary form
        """
        
        log.info(f"({self.name}:{self.id}) Fall detected")
        coords = (message['x'], message['y'], message['z'])
        msg = SensorAlertMessage.make(self.id, self.name, "fall_detected", message['timestamp'], {'coords' : str(coords)})
        super().returnData(msg.json)
        self.timer = Timer(str(self), self.fall_timer, self.__fall_confirmed, message)
        self.timer.start()
        
        
    def __fall_confirmed(self, message):
        """
        Callback for confirming the fall. Sends a message to the server.
        
        Parameters
        ----------
        message : dict
            the message in dictionary form
        """
        log.info(f"({self.name}:{self.id}) Fall confirmed")
        coords = (message['x'], message['y'], message['z'])
        msg = SensorAlertMessage.make(self.id, self.name, "fall_confirmed", message['timestamp'], params={'coords' : str(coords)})
        super().returnData(msg.json)
        
    

def load_sensor_json(json):
    """
    Loads the content of a sensor.json file and creates the respective sensor objects

    Parameters
    ----------
    json : dict
        JSON loaded from sensor.json

    Returns
    -------
    A list of all created sensors.    
    """
    sensor_list = []
    for id, value in json.items():
        
        if value['type'] == "FallSensor":
            sensor = FallSensor(id, value['address'], int(value['port']), int(value['timeout']), 
                                int(value['thresh_detect']), int(value['thresh_confirm']), int(value['fall_grace_period']),
                                int(value['fall_timer']))
            sensor.setTopic(value['topic'])
            sensor_list.append(sensor)
    
    return sensor_list
