
import enum

class MessageTypes(enum.Enum):
    RegisterMessage = 1
    RegisterResponce = 2
    LoginMessage = 3
    LoginResponce = 4
    AlarmMessage = 5
    AlarmResponce = 6
    HistoryRequest = 7
    HistoryResponce = 8

    @classmethod
    def has_key(self, key):
        return key in list(MessageTypes)

