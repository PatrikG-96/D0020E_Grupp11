import json
from database.database import *
from xml.dom import NotSupportedErr
from twisted.internet.defer import Deferred
from twisted.python import log
from twisted.python import failure
from controller.Callbacks import *

class ApiControllerService:
    

    def supportAlarmType(type):
        supported_alarms.append(type)
    
    def getCallbacks(self, proto_cb):
        deferred = Deferred()
        deferred.addCallback(decode)
        deferred.addCallbacks(toJson, decodeErr)
        deferred.addCallbacks(parseJson, jsonErr)
        deferred.addCallbacks(decideAction, parseErr)
        deferred.addErrback(decideErr)
        deferred.addCallback(proto_cb)
        return deferred
        
    # incase other formats are needed, this could be for finding the right type
    def toJson(self, data):
        log.msg(f'Attempting to convert to json')
        json_data = json.loads(data)
        return json_data
    
        
    def decide(self, json_data):
        type = json_data["type"]
        log.msg(f'Deciding action on message of type: {type}')
        if type == "fall_detected":
            return self.actOnFallDetected(json_data)
        elif type == "fall_confirmed":
            return self.actOnFallConfirmed(json_data)
        else:
            raise NotSupportedErr('Unsupported alarm type')
        
    