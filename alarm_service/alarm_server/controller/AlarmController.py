from twisted.internet.defer import Deferred
from controller.Callbacks import *
import json

from network.AlarmFactory import AlarmFactory

class AlarmController:
    
    def __init__(self):
        self.factory = None
        
    def registerFactory(self, factory : AlarmFactory):
        self.factory = factory
        
    def triggerFactory(self, ids, message):
        self.factory.trigger(ids, message)
    
    def getAlarmCallbacks(self, proto_cb):
        deferred = Deferred()
        deferred.addCallback(decode)
        deferred.addCallbacks(toJson, decodeErr)
        deferred.addCallbacks(parseJson, jsonErr)
        deferred.addCallbacks(decideAction, parseErr)
        deferred.addErrback(decideErr)
        deferred.addCallback(proto_cb)
        return deferred
        
    
        