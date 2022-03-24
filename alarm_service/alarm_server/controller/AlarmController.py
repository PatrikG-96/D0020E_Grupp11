from twisted.internet.defer import Deferred
from controller.Callbacks import *
import json
from twisted.python import log
from network.AlarmFactory import AlarmFactory
from database.database import getSubscribers

class AlarmController:
    """Class that contains and represents the logic of the Alarm side of the server
    
    Attributes
    ----------
    factory : AlarmFactory
        Factory instance to be used to trigger alarms notifications
        
    Methods
    -------
    registerFactory(factory : AlarmFactory)
        Sets the factory attribute of this controller. This instance will be used to trigger alarms
    alertClients(message : AlarmNotificationMessage)
        Given an AlarmNotification message, finds the users that are subscribed to the monitor that triggered it (using the database),
        and tells the factory to alert these users with this AlarmNotification message.
    getAlarmCallbacks(proto_cb : function)
        Creates a new Deferred object and adds all neccessary callbacks for the alarm side of the server. Returns this object.
    """
    
    
    def __init__(self):
        self.factory = None
        
    def registerFactory(self, factory : AlarmFactory):
        """Sets the factory to trigger alerts for this controller

        Parameters
        ----------
        factory : AlarmFactory
            the factory to trigger alerts for this controller
        """
        self.factory = factory
        
    def alertClients(self, message : AlarmNotificationMessage):
        """Initializes the process of sending an AlarmNotification to all interested clients. Queries database for subscribers
           for the specific monitor of the AlarmNotification, then triggers the AlarmFactory instance. 

        Parameters
        ----------
        message : AlarmNotificationMessage
            Protocol message object generated as a result of a SensorAlertMessage, will be forwarded to factory then sent to clients
        """
        ids = []
        subs = getSubscribers(message.monitor_id)
        for sub in subs:
            ids.append(sub.userID)
        
        log.msg(f"Alert clients!")
        self.factory.sendToAll(message, ids)
    
    def getAlarmCallbacks(self, proto_cb):
        """Creates a new Deferred object and adds all relevant callbacks for the alarm parsing process, then returns it.

        Parameters
        ----------
        proto_cb : function
            A callback function that the protocol defines itself. Could be a function for sending the eventual response message.  
        
        Returns
        -------
        A Deferred object with all neccessary callbacks added to it, including the protocol specific one from parameters.
        """
        deferred = Deferred()
        deferred.addCallback(decode)
        deferred.addCallbacks(toJson, decodeErr)
        deferred.addCallbacks(parseJson, jsonErr)
        deferred.addCallbacks(decideAction, parseErr)
        deferred.addErrback(decideErr)
        deferred.addCallback(proto_cb)
        return deferred
        
    
        