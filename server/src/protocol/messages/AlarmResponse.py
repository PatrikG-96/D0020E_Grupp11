from . import Message
from .ProtocolException import ProtocolException

class AlarmResponse(Message.Message):

    _field = ['user_id', 'device_id', 'alarm_id', 'response_type']
    

    def __init__(self):
        self.user_id = None
        self.device_id = None
        self.alarm_id = None
        self.response_type = None

    def setUserId(self, uid):
        self.user_id = uid

    def setDeviceId(self, did):
        self.device_id = did

    def setAlarmId(self, aid):
        self.alarm_id = aid

    def setResponseType(self, type):
        self.response_type = type

    def getUserId(self):
        return self.user_id

    def getDeviceId(self):
        return self.device_id

    def getAlarmId(self):
        return self.alarm_id

    def getResponseType(self):
        return self.response_type

    @classmethod
    def isDictValid(self, params):
        if all(key in params for key in self._fields):
            return True

        return False

    @classmethod
    def fromDict(self, params):
        if not self.isDictValid(params):
            raise ProtocolException('Error: Incorrect parameters')
        msg = AlarmResponse()
        msg.setUserId(params['user_id'])
        msg.setDeviceId(params['device_id'])
        msg.setAlarmId(params['alarm_id'])
        msg.setResponseType(params['response_type'])
        return msg

