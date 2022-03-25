
from network.MonitorFactory import MonitorFactory
from .AlarmController import AlarmController
from twisted.internet.defer import Deferred
from controller.Callbacks import *

class MonitorController:
    
    """Class that contains and represents the logic of the Monitor side of the server
    
    Attributes
    ----------
    factory : MonitorFactory
        Factory object used to create the actual connections
    alarm_controller : AlarmController
        A references to the AlarmController used in the Alarm side of the server. This allows
        Monitor client communications to trigger sending AlarmNotification to Alarm side clients
        
    Methods
    -------
    registerFactory(factory : MonitorFactory)
        Adds the MonitorFactory object to the controller
    getMonitorCallbacks(proto_cb : function)
        Creates a new Deferred object and adds all neccessary callbacks for the monitor side of the server. Returns this object.
    triggerAlerts(message : AlarmNotificationMessage)
        Trigger the process of alerting clients with an alarm notification message
    """
    
    def __init__(self, alarm_controller : AlarmController):
        """Creates the controller

        Parameters
        ----------
        alarm_controller : AlarmController
            Reference to the AlarmController used in the server
        """
        self.factory = None
        self.alarm_controller = alarm_controller
    
    def registerFactory(self, factory : MonitorFactory):
        """Sets the factory of this controller

        Parameters
        ----------
        factory : MonitorFactory
            Factory references to use in this controller
        """
        self.factory = factory
        
    def getMonitorCallbacks(self, proto_cb):
        """Creates a new Deferred object and adds all relevant callbacks for the monitor parsing process, then returns it.

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
    
    def triggerAlerts(self, message : AlarmNotificationMessage):
        """The starting point for the alarm notification process. A monitor protocol can use this function to pass
           the AlarmNotificationMessage found in the "alarm" field of the SensorAlertResponseMessage to the Alarm
           side of the server.

        Parameters
        ----------
        message : AlarmNotificationMessage
            The AlarmNotification message found in the "alarm" field of the SensorAlertResponseMessage
        """
        self.alarm_controller.alertClients(message)
    
    
