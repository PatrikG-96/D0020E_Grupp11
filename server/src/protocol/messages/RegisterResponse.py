from . import Message
from .ProtocolException import ProtocolException

class RegisterResponse(Message.Message):

    _fields = ['user_id']

    def __init__(self):
        self.username = None


    def setUserId(self, uid):
        self.user_id = uid


    def getUserId(self):
        return self.user_id


    @classmethod
    def isDictValid(self, params):
        if all(key in params for key in self._fields):
            return True

        return False

    @classmethod
    def fromDict(self, params):
        if not self.isDictValid(params):
            raise ProtocolException('Error: Incorrect parameters')
        msg = RegisterResponse()
        msg.setUserId(params['user_id'])
        return msg