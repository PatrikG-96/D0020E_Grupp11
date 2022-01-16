from . import Message
from .ProtocolException import ProtocolException

class HistoryRequest(Message.Message):

    _field = ['user_id', 'device_id']

    def __init__(self):
        self.user_id = None
        self.device_id = None

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
        if all(key in params for key in self._fields):
            return True

        return False

    @classmethod
    def fromDict(self, params):
        if not self.isDictValid(params):
            raise ProtocolException('Error: Incorrect parameters')
        msg = HistoryRequest()
        msg.setUserId(params['user_id'])
        msg.setDeviceId(params['device_id'])
        return msg