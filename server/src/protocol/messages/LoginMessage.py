from . import Message
from .ProtocolException import ProtocolException

class LoginMessage(Message.Message):

    _fields = ['username', 'password']

    def __init__(self):
        self.username = None
        self.password = None
        

    def setUsername(self, username):
        self.username = username

    def setPassword(self, password):
        self.password = password

    def getPassword(self):
        return self.password

    def getUsername(self):
        return self.username

    @classmethod
    def isDictValid(self, params):

        if all(key in params for key in self._fields):
            return True

        return False

    @classmethod
    def fromDict(self, params):
        if not self.isDictValid(params):
            raise ProtocolException('Error: Incorrect parameters')
        msg = LoginMessage()
        msg.setUsername(params['username'])
        msg.setPassword(params['password'])
        return msg