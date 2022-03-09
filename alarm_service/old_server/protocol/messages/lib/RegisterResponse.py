from ..Message import Message

class RegisterResponse(Message):

    _fields = ['user_id']

    def __init__(self):
        field = ['user_id']
        super().__init__(field)

    def setUserId(self, uid):
        self.user_id = uid

    def getUserId(self):
        return self.user_id

    @classmethod
    def isDictValid(self, params):
        return super().isDictValid(self, params)

    @classmethod
    def fromDict(self, params):
        return super().fromDict(self, params, RegisterResponse())