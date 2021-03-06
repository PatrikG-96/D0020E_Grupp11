#from .generalFunc import *
from ast import Sub
from msilib.schema import ODBCAttribute
import os
from xmlrpc.client import Server
from dotenv import load_dotenv

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import IntegrityError
import json


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
    monitorObj = Monitor(name = name)
    session.add(monitorObj) #Insert new
    session.commit()
    return monitorObj

def setNewUser(username, password, name): #Takes three string values as argument
    try:
        userObj = User(username = username, password = password, name = name, role = 'user')
        session.add(userObj)
        session.commit()
        return (True, userObj)
    except sqlalchemy.exc.IntegrityError:
        print("Username already exist")
        return (False, None)

def deleteUser(userValue): #Takes either userID or username
    if (isinstance(userValue, int) == True):
        session.query(User).filter(User.userID == userValue).delete()
        session.commit()

    else:
        session.query(User).filter(User.username == userValue).delete()
        session.commit()

def setNewSubscription(userID, monitorID): #Takes two int values as argument
    try:
        subscriptionObj = Subscription(userID = userID, monitorID = monitorID)
        session.add(subscriptionObj)
        session.commit()
        return True
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        return False

def deleteSubscriber(userID, monitorID):
    session.query(Subscription).filter(Subscription.userID == userID, Subscription.monitorID == monitorID).delete()
    session.commit()

def setNewDevice(monitorID):
    deviceObj = Sensor(monitorID = monitorID)
    session.add(deviceObj)
    session.commit()
    return deviceObj

def deleteMonitor(monitorID):
    session.query(Monitor).filter(Monitor.monitorID == monitorID).delete()
    session.commit()

def deleteDevice(deviceID):
    session.query(Sensor).filter(Sensor.sensorID == deviceID).delete()
    session.commit()
    
def deleteSubscription(userID, monitorID):
    session.query(Subscription).filter(and_(Subscription.userID == userID, Subscription.monitorID == monitorID))
    session.commit()

def addServerAccessToken(clientID, token, timestamp):
    serverAccess  = ServerAccess(clientID = clientID, token = token, timestamp = timestamp)
    try:
        session.add(serverAccess)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        deleteServerAccess(clientID)
        addServerAccessToken(clientID, token, timestamp)
    except Exception as e:
        raise Exception(str(e))
    return serverAccess    

def deleteServerAccess(clientID):
    session.query(ServerAccess).filter(ServerAccess.clientID == clientID).delete()
    session.commit()

def setNewAlarm(monitorID, alarmType, timestamp): #Takes one string and one int value as argument
    
    res = session.query(AlarmType).filter(AlarmType.nameType == alarmType).all()[0]
    
    alarmObj = Alarm(monitorID = monitorID, alarmType = res.alarmTypeID, read = 0, resolved = 0, timestamp = timestamp)
    session.add(alarmObj)
    session.commit()
    return alarmObj

def readAlarm(alarmID, userID, timestamp):
    try:
        res = session.query(ActionType).filter(ActionType.nameType == "read").all()[0]
        actionObj = Action(alarmID = alarmID, userID = userID, actionType = res.actionTypeID, timestamp = timestamp)
        session.add(actionObj)
        obj = session.query(Alarm).get(alarmID)
        obj.read = 1
        session.commit()
        return actionObj
    except Exception as e:
        session.rollback()
        raise Exception(e)
    
def resolveAlarm(alarmID, userID, timestamp):
    try:
        res = session.query(ActionType).filter(ActionType.nameType == "solved").all()[0]
        actionObj = Action(alarmID = alarmID, userID = userID, actionType = res.actionTypeID, timestamp = timestamp)
        session.add(actionObj)
        obj = session.query(Alarm).get(alarmID)
        obj.resolved = 1
        session.commit()
        return actionObj
    except Exception as e:
        session.rollback()
        raise Exception(e)
    
def getSensorMonitor(sensorID):
    return session.query(Monitor).join(Sensor, Sensor.sensorID == sensorID).filter(Sensor.monitorID == Monitor.monitorID).all()[0]

def getSensor(deviceID):
    return session.query(Sensor).filter(Sensor.deviceID == deviceID).all()[0]

def getAllAlarms(): #Returns a resultset in the form of list of objects.
    return session.query(Alarm).join(AlarmType).filter(Alarm.alarmType == AlarmType.alarmTypeID).all()
        
def getServerAccess(clientID):
    return session.get(ServerAccess, clientID)
    
    
def getDevices():#Returns a resultset in the form of list of objects.
    return session.query(Sensor).all()

def getSubscribers(monitorID): #Gets all the users that are subscripted to a monitor. Takes an int as argument.
    result=session.query(Subscription).filter(Subscription.monitorID==monitorID).all()
    return result

def getSubscribersSensor(deviceID): #Gets all the users that are subscripted to a monitor through deviceID. Takes an int as argument.
    #select subscription.userID from subscription inner join sensor on sensor.deviceID=machineID where sensor.monitorID=subscription.monitorID
    result=session.query(Subscription).join(Sensor, Sensor.sensorID == deviceID).filter(Sensor.monitorID==Subscription.monitorID).all()
    return result

def getUserDeviceSubscriptions(userID):
    result=session.query(Sensor).join(Subscription, Subscription.userID == userID).filter(Subscription.monitorID==Sensor.monitorID).all()
    #result = session.query(Sensor.deviceID, Subscription).filter(Subscription.monitorID==Sensor.monitorID, Subscription.userID==userID).all()
    return result
    
def getUserActiveAlarms(userID):
    result = session.query(Alarm).filter(Alarm.monitorID==Subscription.monitorID, 
        Subscription.userID==userID, or_(Alarm.read==0, Alarm.resolved==0)).all()
    return result

def getUser(userValue): #Returns a user with id, name and password. Takes a int or string
    if (isinstance(userValue, int) == True):
        result = session.query(User).filter(User.userID == userValue).all()[0]
        if not result: #If user do not exist
            return False
        return result

    else:
        result = session.query(User).filter(User.username == userValue).all()
        if not result:
            return False
        return result[0]

def getAllAlarmNotRead(): #Returns all alarms that are not read
    result = session.query(Alarm).join(AlarmType).filter(Alarm.read==0, AlarmType.alarmTypeID ==Alarm.alarmType).all()
    return result

def getAllAlarmNotSolved(): #Returns all alarms that are not solved
    result = session.query(Alarm).filter(Alarm.resolved == 0).all()
    return result



def getAllMonitors():
    
    return session.query(Monitor).all()