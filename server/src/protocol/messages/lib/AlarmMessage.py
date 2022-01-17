from . import Message

class AlarmMessage(Message.Message):

    _fields = ['device_id', 'alarm_id', 'alarm_flag']

    def __init__(self):
        field = ['device_id', 'alarm_id', 'alarm_flag']
        super().__init__(field)

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
        return super().isDictValid(self, params)

    @classmethod
    def fromDict(self, params):
        return super().fromDict(self, params, AlarmMessage())