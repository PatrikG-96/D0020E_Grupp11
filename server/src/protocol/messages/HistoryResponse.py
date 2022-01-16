from . import Message
from .ProtocolException import ProtocolException

class HistoryResponse(Message.Message):

    _field = ['device_id', 'table_data']

    def __init__(self):
        self.table_data = None
        self.device_id = None

    def setTableData(self, table_data):
        self.table_data = table_data

    def setDeviceId(self, did):
        self.device_id = did

    def getTableData(self):
        return self.table_data

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
        msg = HistoryResponse()
        msg.setTableData(params['table_data'])
        msg.setDeviceId(params['device_id'])
        return msg