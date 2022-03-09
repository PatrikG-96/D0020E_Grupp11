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
        self.name = "Sensor"
        
    def setMonitor(self, monitor : Monitor):
        self.monitor = monitor
    
    @abc.abstractmethod
    def start(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def connect(self):
        raise NotImplementedError
        
    @abc.abstractmethod
    def disconnect(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def parse(self, msg : str) -> dict:
        raise NotImplementedError
    
    def returnData(self, data : dict):
        self.monitor.sendData(self.id, data)
    
    def __str__(self):
        return f"({self.name}:{self.id})"

class MQTTSensor(Sensor):
    
    def __init__(self, id, addr, port, timeout):
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
        self.connect_cb = func
    
    
    def setDisonnectCallback(self, func):
        self.disconnect_cb = func
    
    
    def setTopic(self, topic):
        self.topic = topic
    
    def connected(self, client, userdata, flags, rc):
        
        log.info(f"({self.name}:{self.id}) Sensor connected with result code: {rc}")
        if rc == 0:
            
            if self.connect_cb is not None:
        
                self.connect_cb({'sensor' : self})
                
        
    def disconnect(self, client, userdata, rc):
        log.warning(f"({self.name}:{self.id}) Sensor disconnected with result code: {rc}")
        
        if self.disconnect_cb is not None:
            self.disconnect_cb({'sensor' : self})
        
        self.connect()
    
    def connect(self):
        log.info(f"({self.name}:{self.id}) Attempting to connect: '(addr = {self.addr}, port = {self.port}, timeout = {self.timeout})'")
        self.client.connect(self.addr, self.port, self.timeout)
        
        
    def start(self):
        log.info(f"({self.name}:{self.id}) Sensor starting")
        self.client.subscribe(self.topic)
        self.client.loop_start()
        
class WideFind(MQTTSensor):
    
    def __init__(self, id, addr, port, timeout):
        super().__init__(id, addr, port, timeout)
        self.name = "WideFind"
        
    def parse(self, msg):
        
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
    
    def __init__(self, id,addr, port, timeout, detected_limit, resolved_limit, grace_period, fall_timer):
        super().__init__(id, addr, port, timeout)
        self.name = "WideFind_FallSensor"
        self.client.on_message = self.on_message
        self.isFalling = False
        self.detected_limit = detected_limit
        self.fall_timer = fall_timer
        print(f"falltimer: {self.fall_timer}")
        self.grace_period = grace_period
        self.resolved_limit = resolved_limit
        self.active = True
        self.timer = None    
    
    def on_message(self, client, userdata, msg):
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
            self.isFalling = False
            self.active = True
    
        
    def __fall_detected(self, message):
        
        log.info(f"({self.name}:{self.id}) Fall detected")
        self.isFalling = True
        coords = (message['x'], message['y'], message['z'])
        msg = SensorAlertMessage.make(self.id, self.name, "fall_detected", message['timestamp'], {'coords' : str(coords)})
        super().returnData(msg.json)
        self.timer = Timer(str(self), self.fall_timer, self.__fall_confirmed, message)
        self.timer.start()
        
        
    def __fall_confirmed(self, message):
        log.info(f"({self.name}:{self.id}) Fall confirmed")
        coords = (message['x'], message['y'], message['z'])
        msg = SensorAlertMessage.make(self.id, self.name, "fall_confirmed", message['timestamp'], params={'coords' : str(coords)})
        super().returnData(msg.json)
        
    

def load_sensor_json(json):
    sensor_list = []
    for id, value in json.items():
        
        if value['type'] == "FallSensor":
            sensor = FallSensor(id, value['address'], int(value['port']), int(value['timeout']), 
                                int(value['thresh_detect']), int(value['thresh_confirm']), int(value['fall_grace_period']),
                                int(value['fall_timer']))
            sensor.setTopic(value['topic'])
            sensor_list.append(sensor)
    
    return sensor_list
