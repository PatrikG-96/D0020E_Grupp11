import abc
from .ProtocolException import ProtocolException

class Message(object):

    __metaclass__= abc.ABCMeta

    def __init__(self, fields):
        if ('username' in fields): self.username = None
        if ('password' in fields): self.password = None
        if ('user_id' in fields): self.user_id = None
        if ('device_id' in fields): self.device_id = None
        if ('alarm_id' in fields ): self.alarm_id = None
        if ('alarm_flag' in fields ): self.alarm_flag = None
        if ('table_data'in fields): self.table_data = None
        if ('response_type' in fields): self.response_type = None 

    @property
    @classmethod
    @abc.abstractmethod
    def _fields(cls):
        raise NotImplementedError

    @abc.abstractstaticmethod
    def isDictValid(self, params):
        if all(key in params for key in self._fields):
            return True
        return False

    @abc.abstractstaticmethod
    def fromDict(self, params, message):
        if not self.isDictValid(params):
            raise ProtocolException('Error: Incorrect parameters')

        msg = message
        
        if ('username' in params): msg.setUsername(params['username'])
        if ('password' in params): msg.setPassword(params['password'])
        if ('user_id' in params): msg.setUserId(params['user_id'])
        if ('device_id' in params): msg.setDeviceId(params['device_id'])
        if ('alarm_id' in params ): msg.setAlarmId(params['alarm_id'])
        if ('alarm_flag' in params ): msg.setAlarmFlag(params['alarm_flag'])
        if ('table_data'in params): msg.setTableData(params['table_data'])
        if ('response_typed'in params): msg.setResponseType(params['response_type'])
   
        return msg