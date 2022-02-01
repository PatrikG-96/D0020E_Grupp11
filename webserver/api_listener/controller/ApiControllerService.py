import json
from xml.dom import NotSupportedErr
from twisted.internet.defer import Deferred
from twisted.python import log

class ApiControllerService:
    
    def __init__(self):
        pass
    
    def setParsingCallbacks(self, deferred):
        log.msg("Adding parsing callbacks")
        deferred.addCallback(self.toJson)
        deferred.addCallback(self.decide)
        deferred.addErrback(self.typeError)
        
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
        
    def actOnFallDetected(self, json_data):
        log.msg("Should log to db.")
        return None
        
    def actOnFallConfirmed(self, json_data):
        print("Add to database")
        print("Need to alert")
        return json_data
        
    def typeError(self, reason):
        print('Reason!')
        return None