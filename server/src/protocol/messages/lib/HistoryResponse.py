from dataclasses import field
from ..Message import Message

class HistoryResponse(Message):

    _field = ['device_id', 'table_data']

    def __init__(self):
        field = ['device_id', 'table_data']
        super().__init__(field)

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
        return super().isDictValid(self, params)

    @classmethod
    def fromDict(self, params):
        return super().fromDict(self, params, HistoryResponse())