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
        session.commit()
        return True
    except sqlalchemy.exc.IntegrityError:
        print("Foreign key constraint: value of value of machineID and/or userID do not exist")
        session.rollback()
        return False

def deleteSubscriber(userID, monitorID):
    session.query(Subscription).filter(Subscription.userID == userID, Subscription.monitorID == monitorID).delete()
    session.commit()


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