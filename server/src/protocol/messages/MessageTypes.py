
import enum

class MessageTypes(enum.Enum):
    RegisterMessage = 1
    RegisterResponse = 2
    LoginMessage = 3
    LoginResponse = 4
    AlarmMessage = 5
    AlarmResponse = 6
    HistoryRequest = 7
    HistoryResponse = 8

    @classmethod
    def has_key(self, key):
        return key in list(MessageTypes)

