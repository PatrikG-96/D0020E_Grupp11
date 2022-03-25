#from .generalFunc import *
from ast import Sub
from msilib.schema import ODBCAttribute
import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.automap import automap_base
import json

"""
This module contains functions for accessing the alarm database.
"""

load_dotenv()

name = os.getenv("DB_NAME")
host = os.getenv("DB_HOST")
password = os.getenv("DB_PASSWORD")
user = os.getenv("DB_USER")

try:
    engine = create_engine(f"mysql://{user}:{password}@{host}/{name}", echo = False) #takes database as one argument, returns an engine object
    #__connection = engine.connect() #Establish DBAPI connection to database
    Session = sessionmaker(bind = engine)
    session = Session()
except sqlalchemy.exc.OperationalError:
    print("Can't connect to database")

# Make mapped classes
metadata = MetaData() #Get the tables from the database
metadata.reflect(bind=engine)

Base = automap_base() 
Base.prepare(engine, reflect=True) #Reflect the tables in the database

User = Base.classes.user
Subscription = Base.classes.subscription
Sensor = Base.classes.sensor
Monitor = Base.classes.monitor
Alarm = Base.classes.alarm
AlarmType = Base.classes.alarmtype
Action = Base.classes.action
ActionType = Base.classes.actiontype
ServerAccess = Base.classes.serveraccess
#Endpoints = Base.classes.endpoints

#The functions
def setNewMonitor(name): #Takes one string values as argument
    
    """Creates a new monitor.
        
    Parameters
    ----------
    name : string
        The name of the person that the monitor is set up for.
        
    Returns
    ------
    object
        The object of the newly created monitor.
    """
    monitorObj = Monitor(name = name)
    session.add(monitorObj) #Insert new
    session.commit()
    return monitorObj

def setNewUser(username, password, name): #Takes three string values as argument
    """Creates a new user.
        
    Parameters
    ----------
    username : string
        The username of the user.        
    password : string
        The password of the user.
    name : string
        The name of the user
        
    Returns
    ------
    tuple
        Either return True or False for the bolean and the newly created object of the user or none for object depending if it succeedes.
    """
    try:
        userObj = User(username = username, password = password, name = name, role = 'user')
        session.add(userObj)
        session.commit()
        return (True, userObj)
    except sqlalchemy.exc.IntegrityError:
        print("Username already exist")
        return (False, None)

def deleteUser(userValue): #Takes either userID or username
    """Deletes a user.
    
    Parameters
    ----------
    userValue : string or int
        The data of the user that is to be deleted.
    """
    if (isinstance(userValue, int) == True):
        session.query(User).filter(User.userID == userValue).delete()
        session.commit()

    else:
        session.query(User).filter(User.username == userValue).delete()
        session.commit()

def setNewSubscription(userID, monitorID): #Takes two int values as argument
    """Creates a new subscription for a user and monitor.
        
    Parameters
    ----------
    userID : int
        The identification of a user.
    monitorID : int
        The identification of a monitor.
        
    Returns
    ------
    tuple
        Either return True or False for the bolean and the newly created object of the monitor or none for object depending if it succeedes.
    """
    try:
        subscriptionObj = Subscription(userID = userID, monitorID = monitorID)
        session.add(subscriptionObj)
        session.commit()
        return (True, subscriptionObj)
    except sqlalchemy.exc.IntegrityError:
        print("Foreign key constraint: value of value of machineID and/or userID do not exist")
        return (False, None)

def deleteSubscriber(userID, monitorID):
    """Deletes a subscription between a user and monitor.
        
    Parameters
    ----------
    userID : int
        The identification of a user.
    monitorID : int
        The identification of a monitor.
    """
    session.query(Subscription).filter(Subscription.userID == userID, Subscription.monitorID == monitorID).delete()
    session.commit()

def setNewDevice(monitorID):
    """Creates a new device.
        
    Parameters
    ----------
    monitorID : int
        The identification of a monitor.
        
    Returns
    ------
    object
        The object of the newly created device.
    """
    deviceObj = Sensor(monitorID = monitorID)
    session.add(deviceObj)
    session.commit()
    return deviceObj

def deleteMonitor(monitorID):
    """Deletes a monitor.
        
    Parameters
    ----------
    monitorID : int
        The identification of a monitor.
    """
    session.query(Monitor).filter(Monitor.monitorID == monitorID).delete()
    session.commit()

def deleteDevice(deviceID):
    """Deletes a sensor.
        
    Parameters
    ----------
    deviceID : int
        The identification of a device.
    """
    session.query(Sensor).filter(Sensor.sensorID == deviceID).delete()
    session.commit()

def setNewAlarm(monitorID, alarmType, timestamp): #Takes one string and one int value as argument
    """Creates a new alarm.
        
    Parameters
    ----------
    monitorID : int
        The identification of a monitor.
    alarmType : int
        The identification of what type of alarm it is.
    timestamp : timestamp
        The date of the created alarm. Has the format yyyy-mm-dd h:m:s.
        
    Returns
    ------
    object
        The object of the newly created alarm.
    """
    res = session.query(AlarmType).filter(AlarmType.nameType == alarmType).all()[0]
    
    alarmObj = Alarm(monitorID = monitorID, alarmType = res.alarmTypeID, read = 0, resolved = 0, timestamp = timestamp)
    session.add(alarmObj)
    session.commit()
    return alarmObj

def readAlarm(alarmID, userID, timestamp):
    """Changes the read value of the alarm.
    
    Parameters
    ----------
    alarmID : int
        The identification of an alarm.        
    userID : int
        The identification of a user.
    timestamp : timestamp
        The date of the action. Has the format yyyy-mm-dd h:m:s.
    actionType : int
        The identification of what type of action it is.
        
    Returns
    ------
    object
        The object of the newly created action.
    """
    res = session.query(ActionType).filter(ActionType.nameType == "read").all()[0]
    actionObj = Action(alarmID = alarmID, userID = userID, actionType = res.actionTypeID, timestamp = timestamp)
    session.add(actionObj)
    obj = session.query(Alarm).get(alarmID)
    obj.read = 1
    session.commit()
    return actionObj
    
def resolveAlarm(alarmID, userID, timestamp):
    """Changes the resolved value of the alarm.
        
    Parameters
    ----------
    alarmID : int
        The identification of an alarm.
    userID : int
        The identification of a user.
    timestamp : timestamp
        The date of the action. Has the format yyyy-mm-dd h:m:s.
    actionType : int
        The identification of what type of action it is.
        
    Returns
    ------
    object
        The object of the newly created action.
    """
    res = session.query(ActionType).filter(ActionType.nameType == "solved").all()[0]
    actionObj = Action(alarmID = alarmID, userID = userID, actionType = res.actionTypeID, timestamp = timestamp)
    session.add(actionObj)
    obj = session.query(Alarm).get(alarmID)
    obj.resolved = 1
    session.commit()
    return actionObj
    
def getSensorMonitor(sensorID):
    """Return the parent monitor of this sensor
    
    Parameters
    ----------
    sensorID : int
        unique ID for this sensor
        
    Returns
    -------
    object
        Monitor object for the monitor that is the parent of the sensor
    """
    session.commit()
    return session.query(Monitor).join(Sensor, Sensor.sensorID == sensorID).filter(Sensor.monitorID == Monitor.monitorID).all()[0]

def getSensor(deviceID):
    """Return the sensor with the specificed deviceID
    
    Parameters
    ----------
    deviceID : str
        a unique string identifier for a sensor
        
    Returns
    -------
    object
        Sensor object with this deviceID
    """
    session.commit()
    return session.query(Sensor).filter(Sensor.deviceID == deviceID).all()[0]

def getAllAlarms(): #Returns a resultset in the form of list of objects.
    """Return all the objects of alarm.
        
    Returns
    ------
    list
        A list of all alarm-object in the database.
    """
    session.commit()
    return session.query(Alarm).all()
        
        
def getServerAccess(clientID):
    """Return the server access token for this client
    
    Parameters
    ----------
    clientID : int
        unique ID of the client
        
    Returns
    -------
    object
        A ServerAccess object for this specific client
    """
    session.commit()
    return session.get(ServerAccess, clientID)
    
    
def getDevices():#Returns a resultset in the form of list of objects.
    """Return all the objects of sensor.
        
    Returns
    ------
    list
        A list of all sensor-object in the database.
    """
    session.commit()
    return session.query(Sensor).all()

def getSubscribers(monitorID): #Gets all the users that are subscripted to a monitor. Takes an int as argument.
    """Return all the users that are subscripted to the monitorID.
        
    Parameters
    ----------
    monitorID : int
        The identification of a monitor.
        
    Returns
    ------
    list
        A list of all subscription-object filtered by the parameter in the database.
    """
    session.commit()
    result=session.query(Subscription).filter(Subscription.monitorID==monitorID).all()
    return result

def getSubscribers(monitorID): #Gets all the users that are subscripted to a monitor through deviceID. Takes an int as argument.
    """Return all the users that are subscripted to a monitor through deviceID. 
       
    Parameters
    ----------
    deviceID : int
        The identification of a sensor.
        
    Returns
    ------
    list
        A list of all subscription-object filtered by the parameter in the database.
    """
    session.commit()
    result=session.query(Subscription).join(Monitor, Monitor.monitorID == monitorID).filter(Monitor.monitorID==Subscription.monitorID).all()
    return result

def getUserDeviceSubscriptions(userID):
    """Return all devices that a user is subscripted to.
        
    Parameters
    ----------
    userID : int
        The identification of a user.
        
    Returns
    ------
    list
        A list of all sensor-object filtered by the parameter in the database.
    """
    session.commit()
    result=session.query(Sensor).join(Subscription, Subscription.userID == userID).filter(Subscription.monitorID==Sensor.monitorID).all()
    #result = session.query(Sensor.deviceID, Subscription).filter(Subscription.monitorID==Sensor.monitorID, Subscription.userID==userID).all()
    return result
    
def getUserActiveAlarms(userID):
    """Return all active alarm of a monitor that a user is subscripted to.
    
    Parameters
    ----------
    userID : int
        The identification of a user.
        
    Returns
    ------
    list
        A list of all alarm-object that are active filtered by the parameter in the database.
    """
    session.commit()
    result = session.query(Alarm).filter(Alarm.monitorID==Subscription.monitorID, 
        Subscription.userID==userID, or_(Alarm.read==0, Alarm.resolved==0)).all()
    return result

def getUser(userValue): #Returns a user with id, name and password. Takes a int or string
    """Return a user.
        
    Parameters
    ----------
    uservalue : int or string
        The identification of a user.
    
    Returns
    ------
    object
        The user-object filtered by the parameter.
    """
    session.commit()
    if (isinstance(userValue, int) == True):
        result = session.query(User).filter(User.userID == userValue).all()[0]
        if not result: #If user do not exist
            return False
        return result

    else:
        result = session.query(User).filter(User.username == userValue).all()[0]
        if not result:
            return False
        return result

def getAllAlarmNotRead(): #Returns all alarms that are not read
    """Return all the objects that are not read of alarm.
    
    Returns
    ------
    list
        A list of all alarm-object filtered by parameter in the database.
    """
    session.commit()
    result = session.query(Alarm).filter(Alarm.read==0).all()
    return result

def getAllAlarmNotSolved(): #Returns all alarms that are not solved
    """Return all the objects that are not resolved of alarm.
    
    Returns
    ------
    list
        A list of all alarm-object filtered by parameter in the database.
    """
    session.commit()
    result = session.query(Alarm).filter(Alarm.resolved == 0).all()
    return result


