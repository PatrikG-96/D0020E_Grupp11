
from .AlarmController import AlarmController

from twisted.internet.defer import Deferred
from controller.Callbacks import *

class MonitorController:
    
    def __init__(self, alarm_controller : AlarmController):
        self.factory = None
        self.alarm_controller = alarm_controller
    
    def registerFactory(self, factory):
        self.factory = factory
        
    def getMonitorCallbacks(self, proto_cb):
        deferred = Deferred()
        deferred.addCallback(decode)
        deferred.addCallbacks(toJson, decodeErr)
        deferred.addCallbacks(parseJson, jsonErr)
        deferred.addCallbacks(decideAction, parseErr)
        deferred.addErrback(decideErr)
        #deferred.addCallback(msgToJson)
        deferred.addCallback(proto_cb)
        return deferred
    
    def triggerAlerts(self, message : AlarmNotificationMessage):
        
        # get uids from database.
        # message.monitor_id
        uids = [1,2]
        
        self.alarm_controller.triggerFactory(uids, message)
    
    
