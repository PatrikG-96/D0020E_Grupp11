<<<<<<< HEAD
from .generalFunc import *
=======
#from .generalFunc import *
>>>>>>> 5f5d6dbe180ca57e525fb55f3fccabb12b0f6d28
from ast import Sub
from msilib.schema import ODBCAttribute
import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.automap import automap_base
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
<<<<<<< HEAD

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
Endpoints = Base.classes.endpoints

#The functions
def setNewMonitor(name): #Takes one string values as argument
    session.add(Monitor(name = name)) #Insert new
    session.commit()

def setNewUser(username, password, name): #Takes two string values as argument
    try:
        session.add(User(username = username, password = password, name = name, role = 'user'))
        session.commit()
        return True
    except sqlalchemy.exc.IntegrityError:
        print("Username already exist")
        return False

def setNewSubscription(userID, monitorID): #Takes two int values as argument
    try:
        session.add(Subscription(userID = userID, monitorID = monitorID))
=======
metadata.reflect(bind=engine)

Base = automap_base() 
Base.prepare(engine, reflect=True) #Reflect the tables in the database

User = Base.classes.user
Subscription = Base.classes.subscription
Monitor = Base.classes.monitor
Endpoints = Base.classes.endpoints

#The functions
def setNewMonitor(id, name): #Takes one string values as argument
    try:
        monitorObj = Monitor(monitorID = id, name = name)
        session.add(monitorObj) #Insert new
        session.commit()
        return monitorObj
    except Exception as e:
        session.rollback()
        raise Exception(e)

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
>>>>>>> 5f5d6dbe180ca57e525fb55f3fccabb12b0f6d28
        session.commit()
        return True
    except sqlalchemy.exc.IntegrityError:
        print("Foreign key constraint: value of value of machineID and/or userID do not exist")
        session.rollback()
        return False

<<<<<<< HEAD
def setNewDevice(monitorID):
    session.add(Sensor(monitorID = monitorID))
=======
def deleteSubscriber(userID, monitorID):
    session.query(Subscription).filter(Subscription.userID == userID, Subscription.monitorID == monitorID).delete()
>>>>>>> 5f5d6dbe180ca57e525fb55f3fccabb12b0f6d28
    session.commit()

def setNewAlarm(monitorID, alarmType, timestamp): #Takes one string and one int value as argument
    session.add(Alarm(monitorID = monitorID, alarmType = alarmType, read = 0, resolved = 0, timestamp = timestamp))
    session.commit()

<<<<<<< HEAD
def readAlarm(alarmID, userID, timestamp, actionType):
    session.add(Action(alarmID = alarmID, userID = userID, actionType = actionType, timestamp = timestamp))
    obj = session.query(Alarm).get(alarmID)
    obj.read = 1
    session.commit()
    
def resolveAlarm(alarmID, userID, timestamp, actionType):
    session.add(Action(alarmID = alarmID, userID = userID, actionType = actionType, timestamp = timestamp))
    obj = session.query(Alarm).get(alarmID)
    obj.resolved = 1
    session.commit()
    
def getAllAlarms(): #Returns a resultset in the form of list of objects.
    return session.query(Alarm).all()
        
    
def getDevices():#Returns a resultset in the form of list of objects.
    return session.query(Sensor).all()

def getSubscribers(deviceID): #Gets all the users that are subscripted to a monitor thorugh deviceID. Takes an int as argument.
    #select subscription.userID from subscription inner join sensor on sensor.deviceID=machineID where sensor.monitorID=subscription.monitorID
    result=session.query(Subscription).join(Sensor, Sensor.deviceID == deviceID).filter(Sensor.monitorID==Subscription.monitorID).all()
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
        result = session.query(User).filter(User.userID == userValue).all()
        return result

    else:
        result = session.query(User).filter(User.username == userValue).all()
        return result

def getAllAlarmNotRead(): #Returns all alarms that are not read
    result = session.query(Alarm).filter(Alarm.read==0).all()
    return result

def getAllAlarmNotSolved(): #Returns all alarms that are not solved
    result = session.query(Alarm).filter(Alarm.resolved == 0).all()
    return result


def storeSubscription(endpoint, userID):
    resultSet = session.query(Endpoints).filter(Endpoints.endpoint == endpoint).all()
    submittedEndpoint = json.loads(endpoint)["endpoint"]
    for row in resultSet:
        row_as_dict = {'id': row.id, 'endpoint': row.endpoint, 'userID': row.userID}
        rowEndpoint = json.loads(row_as_dict["endpoint"])["endpoint"]
        if(submittedEndpoint == rowEndpoint):
            row.endpoint = endpoint
            row.userID = userID
            session.commit
            return True

    session.add(Endpoints(endpoint=endpoint, userID=userID))
    session.commit()
    return True

def getSubscription(userID):
    resultSet = session.query(Endpoints).filter(Endpoints.userID == userID)
    return resultSet[0].endpoint

def getAllSubscriptions():
    return session.query(Endpoints).all()

def deleteSubscription(endpoint):
    with engine.connect() as connection:
        resultSet = session.query(Endpoints).filter(Endpoints.endpoint == endpoint)
        submittedEndpoint = json.loads(endpoint)["endpoint"]
        for row in resultSet:
            row_as_dict = {'id': row.id, 'endpoint': row.endpoint, 'userID': row.userID}
            rowEndpoint = json.loads(row_as_dict["endpoint"])["endpoint"]
            if(submittedEndpoint == rowEndpoint):
                print("the same endpoint")
                session.delete(row)
                session.commit()
                return True



=======
def deleteMonitor(monitorID):
    session.query(Monitor).filter(Monitor.monitorID == monitorID).delete()
    session.commit()

def getSubscribers_m(monitorID): #Gets all the users that are subscripted to a monitor. Takes an int as argument.
    result=session.query(Subscription).filter(Subscription.monitorID==monitorID).all()
    return result


def getSubscriber_s(deviceID): #Gets all the users that are subscripted to a monitor through deviceID. Takes an int as argument.
    #select subscription.userID from subscription inner join sensor on sensor.deviceID=machineID where sensor.monitorID=subscription.monitorID
    result=session.query(Subscription).join(Monitor, Monitor.monitorID == deviceID).filter(Monitor.monitorID==Subscription.monitorID).all()
    return result

def getUserDeviceSubscriptions(userID):
    result=session.query(Monitor).join(Subscription, Subscription.userID == userID).filter(Subscription.monitorID==Monitor.monitorID).all()
    #result = session.query(Sensor.deviceID, Subscription).filter(Subscription.monitorID==Sensor.monitorID, Subscription.userID==userID).all()
    return result
    

def getUser(userValue): #Returns a user with id, name and password. Takes a int or string
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

def getMonitor(monitorID):
    
    return session.get(Monitor, monitorID)

def getAllMonitors():
    
    return session.query(Monitor).all()
>>>>>>> 5f5d6dbe180ca57e525fb55f3fccabb12b0f6d28
