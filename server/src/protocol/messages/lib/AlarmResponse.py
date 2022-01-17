from . import Message

class AlarmResponse(Message.Message):

    _field = ['user_id', 'device_id', 'alarm_id', 'response_type']

    def __init__(self):
        fields = ['user_id', 'device_id', 'alarm_id', 'response_type']
        super().__init__(fields)

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
        return super().isDictValid(self, params)

    @classmethod
    def fromDict(self, params):
        return super().fromDict(self, params, AlarmResponse())

