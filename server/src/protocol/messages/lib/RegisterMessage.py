from ..Message import Message

class RegisterMessage(Message):

    _fields = ['username', 'password']
        
    def __init__(self):
        field = ['username', 'password']
        super().__init__(field)    

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
        return super().isDictValid(self, params)

    @classmethod
    def fromDict(self, params):
        return super().fromDict(self, params, RegisterMessage())
