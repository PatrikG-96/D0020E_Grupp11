import abc
import paho.mqtt.client as mqtt
import logging
import json
from datetime import datetime, timedelta
from util.Timer import Timer
from monitor.Monitor import Monitor
from protocol.messages import SensorAlertMessage

log = logging.getLogger()

class Sensor(object):
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, id):
        self.id = id
        self.monitor = None
        
    def setMonitor(self, monitor : Monitor):
        self.monitor = monitor
    
    @abc.abstractmethod
    def start(self):
        raise NotImplementedError
    
    def connect(self):
        self.monitor.registerSensor(self)
        
    def disconnect(self):
        self.monitor.deregisterSensor(self)
    
    @abc.abstractmethod
    def parse(self, client, userdata, msg):
        raise NotImplementedError
    
    def returnData(self, data):
        self.monitor.sendData(data)
    

class MQTTSensor(Sensor):
    
    def __init__(self, id, addr, port, timeout):
        self.client = mqtt.Client()
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.timeout = addr
        self.addr = port
        self.port = timeout
        self.topic = None
        self.name = "MQTT"
        super().__init__(id)
    
    def setTopic(self, topic):
        self.topic = topic
    
    def connected(self, client, userdata, flags, rc):
        log.info(f"MQTT sensor connected with result code: {rc}")
        
    def disconnected(self, userdata, rc):
        log.warning(f"MQTT sensor disconnected with result code: {rc}")
        super().disconnect()
        self.connect()
    
    def connect(self):
        log.info(f"({self.name}:{self.id}) Attempting to connect: '(addr = {self.addr}, port = {self.port}, timeout = {self.timeout})'")
        self.client.connect(self.addr, self.port, self.timeout)
        super().connect()
        
    def start(self):
        self.client.subscribe(self.topic)
        self.client.loop_forever()
        
class WideFind(MQTTSensor):
    
    def __init__(self, id):
        self.name = "WideFind"
        super().__init__(id)
        
    def parse(self, client, userdata, msg):
        
        stringified = msg.payload.decode('utf-8')
        json_data = json.loads(stringified)
        message = json_data['message']
        time = datetime.strptime(json_data['time'][:-10], "%Y-%m-%dT%H:%M:%S.%f")
        
        params = message.split(',')
        type_split = params[0].split(':')
        type = type_split[0]
        id = type_split[1]
        
        if type == "REPORT" and id == self.id:
            
            result = {'id' : id, 'timestamp': time, 'version' : params[1], 
                      'x' : params[2], 'y' : params[3], 'z' : params[4],
                      'velX' : params[5], 'velY' : params[6], 'velZ' : params[7], 
                      'battery' : params[8], 'rssi' : params[9], 'timealive' : params[10]}
            
            return result
    

class FallSensor(WideFind):
    
    def __init__(self, id, detected_limit, resolved_limit, fall_timer):
        super().__init__(id)
        self.client.on_message = self.parse
        self.isFalling = False
        self.detected_limit = detected_limit
        self.fall_timer = fall_timer
        self.resolved_limit = resolved_limit
        self.active = True
        self.timer = None    
    
    def parse(self, client, userdata, msg):
        data = super().parse(client, userdata, msg)
        
        if not self.isFalling and int(data['z']) < self.detected_limit:
            self.timer = Timer(self.fall_timer, self.__fall_confirmed, data)
            self.__fall_detected(data)
            self.isFalling = True
            
        if self.isFalling and int(data['z']) > self.resolved_limit:
            self.timer.stop()
            self.isFalling = False
    
        
    def __fall_detected(self, message):
        coords = (message['x'], message['y'], message['z'])
        msg = SensorAlertMessage.make(self.id, self.name, "fall_detected", message['timestamp'], {'coords' : str(coords)})
        super().returnData(msg.json)
        
        
    def __fall_confirmed(self, message):
        coords = (message['x'], message['y'], message['z'])
        msg = SensorAlertMessage.make(self.id, self.name, "fall_confirmed", message['timestamp'], params={'coords' : str(coords)})
        super().returnData(msg.json)
        
        
    def __str__(self):
        return f"ID:{self.id}, Name:{self.name}"


def load_sensor_json(json):
    sensor_list = []
    for key, value in json.items():
        
        if value['type'] == "FallSensor":
            sensor = FallSensor(value['id'], value['thresh_detect'], value['thresh_confirm'], value['fall_timer'])
            sensor.setConnectionInfo(value['address'], value['port'], value['timeout'])
            sensor.setTopic(value['topic'])
            sensor_list.append(sensor)
    
    return sensor_list
