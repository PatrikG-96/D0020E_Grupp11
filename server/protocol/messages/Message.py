import abc
import logging

class Message(object):

    __metaclass__= abc.ABCMeta

    def __init__(self, message_string) :
        self.message_string = message_string

    def getMessageString(self):
        return self.message_string

    @abc.abstractclassmethod
    def parseMessageString(string):
        return

    @abc.abstractclassmethod
    def isValid(string):
        return