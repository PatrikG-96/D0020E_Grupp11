from twisted.internet.defer import Deferred
from controller.Callbacks import *
import json
from twisted.python import log
from network.AlarmFactory import AlarmFactory
from database.database import getSubscribers

class AlarmController:
    
    def __init__(self):
        self.factory = None
        
    def registerFactory(self, factory : AlarmFactory):
        self.factory = factory
        
    def alertClients(self, message : AlarmNotificationMessage):
        
        ids = []
        print(f"In alertClients, monitorID: {message.monitor_id}")
        subs = getSubscribers(message.monitor_id)
        print(f"subs : {subs}")
        for sub in subs:
            ids.append(sub.userID)
        
        log.msg(f"Alert clients!")
        self.factory.sendToAll(message, ids)
    
    def getAlarmCallbacks(self, proto_cb):
        deferred = Deferred()
        deferred.addCallback(decode)
        deferred.addCallbacks(toJson, decodeErr)
        deferred.addCallbacks(parseJson, jsonErr)
        deferred.addCallbacks(decideAction, parseErr)
        deferred.addErrback(decideErr)
        deferred.addCallback(proto_cb)
        return deferred
        
    
        