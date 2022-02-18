from .generalFunc import *
from msilib.schema import ODBCAttribute
import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.automap import automap_base
import json
from datetime import datetime

load_dotenv()

name = os.getenv("NAME")
host = os.getenv("HOST")
password = os.getenv("PASSWORD")
user = os.getenv("USER")

try:
    engine = create_engine(f"mysql://{user}:{password}@{host}/{name}", echo = False) #takes database as one argument, returns an engine object
    #__connection = engine.connect() #Establish DBAPI connection to database
    Session = sessionmaker(bind = engine)
    session = Session()
except sqlalchemy.exc.OperationalError:
    print("Can't connect to database")

# Make mapped classes
metadata = MetaData() #Get the tables from the database

Base = automap_base() 
Base.prepare(engine, reflect=True) #Reflect the tables in the database
User = Base.classes.user
Subscription = Base.classes.subscription
Sensor = Base.classes.sensor
Elderly = Base.classes.elderly
Alarm = Base.classes.alarm
AlarmType = Base.classes.alarmtype
Action = Base.classes.action
ActionType = Base.classes.actiontype
Endpoints = Base.classes.endpoints

#The functions
def setNewElderly(name): #Takes one string values as argument
    session.add(Elderly(name = name)) #Insert new
    session.commit()

def setNewUser(username, password, name): #Takes two string values as argument
    try:
        session.add(User(username = username, password = password, name = name, role = 'user'))
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        print("Username already exist")

def setNewSubscription(userID, elderlyID): #Takes two int values as argument
    try:
        session.add(Subscription(userID = userID, elderlyID = elderlyID))
        session.commit()
        return True
    except sqlalchemy.exc.IntegrityError:
        print("Foreign key constraint: value of value of machineID and/or userID do not exist")
        return False

def setNewDevice(elderlyID):
    session.add(Sensor(elderlyID = elderlyID))
    session.commit()

def setNewAlarm(elderlyID, alarmType, timestamp): #Takes one string and one int value as argument
    session.add(Alarm(elderlyID = elderlyID, alarmType = alarmType, read = 0, resolved = 0, timestamp = timestamp))
    session.commit()

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

def getSubscribers(machineID): #Gets all the users that are subscripted to edlerly thorugh machineID. Takes an int as argument.
    #select subscription.userID from subscription inner join sensor on sensor.deviceID=machineID where sensor.elderlyID=subscription.elderlyID
    result=session.query(Subscription.userID).join(Sensor, Sensor.deviceID == machineID).filter(Sensor.elderlyID==Subscription.elderlyID).all()
    return result

def getUserDeviceSubscriptions(userID):
    result = session.query(Sensor.deviceID, Subscription).filter(Subscription.elderlyID==Sensor.elderlyID, Subscription.userID==userID).all()
    return result
    
def getUserActiveAlarms(userID):
    result = session.query(Alarm).filter(Alarm.elderlyID==Subscription.elderlyID, 
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


#print(getSubscription(1))
print(deleteSubscription("""{"endpoint":"https://updates.push.services.mozilla.com/wpush/v2/gAAAAABiA9a0z4LIENAEjvbvUzGtdKOhD5nOu9npFvVwPA73vLSqp00V7_jwoN1PVyigDFZHxlT80KdLmceC-pQ0csbr3ENouWaqymtsmC6aMO2Vum4tFoZAct0x-xvq4MKnhdB9abx-NQBJHmbApszrgB2qIGfRnyiIIPw4sNinXCzHOvwDS8o","expirationTime":null,"keys":{"auth":"BU802LufUiqraVSMDdgGLg","p256dh":"BMMjodI_R_Lh-z1czK1PQbWqRV8RgoFQeCPj0fSg6ZYgInPdYriYQnNsD6kc-m6vZEoDr555jiURL8ULkP3NcoE"}}"""))