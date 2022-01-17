from . import Message

class HistoryRequest(Message.Message):

    _field = ['user_id', 'device_id']

    def __init__(self):
        field = ['user_id', 'device_id']
        super().__init__(field)

    def setUserId(self, uid):
        self.user_id = uid

    def setDeviceId(self, did):
        self.device_id = did

    def getUserId(self):
        return self.user_id

    def getDeviceId(self):
        return self.device_id

    @classmethod
    def isDictValid(self, params):
        return super().isDictValid(self, params)

    @classmethod
    def fromDict(self, params):
        return super().fromDict(self, params, HistoryRequest())