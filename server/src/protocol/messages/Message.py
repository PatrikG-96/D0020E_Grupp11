import abc

class Message(object):

    __metaclass__= abc.ABCMeta

    @property
    @classmethod
    @abc.abstractmethod
    def _fields(cls):
        raise NotImplementedError

    @abc.abstractstaticmethod
    def fromDict(self, params):
        return

    @abc.abstractstaticmethod
    def isDictValid(self, params):
        return

    