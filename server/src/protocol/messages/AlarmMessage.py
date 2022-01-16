from . import Message
from .ProtocolException import ProtocolException

class AlarmMessage(Message.Message):

    _field = ['device_id', 'alarm_id', 'alarm_flag']
    

    def __init__(self):
        self.device_id = None
        self.alarm_id = None
        self.alarm_flag = None

    def setDeviceId(self, did):
        self.device_id = did

    def setAlarmId(self, aid):
        self.alarm_id = aid

    def setAlarmFlag(self, flag):
        self.alarm_flag = flag

    def getDeviceId(self):
        return self.device_id

    def getAlarmId(self):
        return self.alarm_id

    def getAlarmFlag(self):
        return self.alarm_flag

    @classmethod
    def isDictValid(self, params):
        if all(key in params for key in self._fields):
            return True

        return False

    @classmethod
    def fromDict(self, params):
        if not self.isDictValid(params):
            raise ProtocolException('Error: Incorrect parameters')
        msg = AlarmMessage()
        msg.setUserId(params['user_id'])
        msg.setDeviceId(params['device_id'])
        msg.setAlarmId(params['alarm_id'])
        msg.setResponseType(params['response_type'])
        return msg

