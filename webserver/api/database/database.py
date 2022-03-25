
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
Monitor = Base.classes.monitor
#Endpoints = Base.classes.endpoints

# May contain some redundant functions

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

def getMonitor(monitorID):
    
    return session.get(Monitor, monitorID)

def getAllMonitors():
    
    return session.query(Monitor).all()

def getUserDeviceSubscriptions(userID):
    result=session.query(Monitor).join(Subscription, Subscription.userID == userID).filter(Subscription.monitorID==Monitor.monitorID).all()
    #result = session.query(Sensor.deviceID, Subscription).filter(Subscription.monitorID==Sensor.monitorID, Subscription.userID==userID).all()
    return result
    

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

def deleteMonitor(monitorID):
    """Deletes a monitor.
        
    Parameters
    ----------
    monitorID : int
        The identification of a monitor.
    """
    session.query(Monitor).filter(Monitor.monitorID == monitorID).delete()
    session.commit()



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





def getSubscribers_m(monitorID): #Gets all the users that are subscripted to a monitor. Takes an int as argument.
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

    result=session.query(Subscription).filter(Subscription.monitorID==monitorID).all()
    return result


def getSubscriber_s(deviceID): #Gets all the users that are subscripted to a monitor through deviceID. Takes an int as argument.
    """Return all the users that are subscripted to the monitor of a sensor given its deviceID.
        
    Parameters
    ----------
    deviceID : str
        The deviceID of a sensor.
        
    Returns
    ------
    list
        A list of all subscription-object filtered by the parameter in the database.
    """

    result=session.query(Subscription).join(Monitor, Monitor.monitorID == deviceID).filter(Monitor.monitorID==Subscription.monitorID).all()
    return result

def getUserDeviceSubscriptions(userID):
    """Return all monitors that a user is subscribed to
    
    Parameters
    ----------
    userID : int
        unique ID of the user
        
    Returns
    -------
    List of Monitor objects, one for each that the user is subscribed to
    """
    
    result=session.query(Monitor).join(Subscription, Subscription.userID == userID).filter(Subscription.monitorID==Monitor.monitorID).all()
   
    return result
    

def getMonitor(monitorID):
    """Return the specific monitor
    
    Parameters
    ----------
    monitorID : int
        unique ID of the monitor
        
    Returns
    -------
    Monitor object with the specific ID
    """
    return session.get(Monitor, monitorID)

def getAllMonitors():
    """Return a list of all known monitors
    
    Returns
    -------
    A list of all known monitors
    """
    return session.query(Monitor).all()


def storeSubscription(endpoint : str, userID : int):
    """Store a new endpoint.
        Parameters
        ----------
        endpoint : string
            A dictionary of the endpoint.
        userID : int
            The identification of a user.
        Returns
        ------
        tuple
            Either return True or False for the bolean and the newly stored object of the endpoint or none for object depending if it succeedes.
    """
    session.commit()
    resultSet = session.query(Endpoints).filter(Endpoints.endpoint == endpoint).all()
    submittedEndpoint = json.loads(endpoint)["endpoint"]
    for row in resultSet:
        row_as_dict = {'id': row.id, 'endpoint': row.endpoint, 'userID': row.userID}
        rowEndpoint = json.loads(row_as_dict["endpoint"])["endpoint"]
        if(submittedEndpoint == rowEndpoint):
            row.endpoint = endpoint
            row.userID = userID
            session.commit
            return (True, None)

    endpointObj = Endpoints(endpoint=endpoint, userID=userID)
    session.add(endpointObj)
    session.commit()
    return (True, endpointObj)

def getSubscription(userID : int):
    """Return the endpoint that a user is subscripted to.
        Parameters
        ----------
        userID : int or string
            The identification of a user.
        Returns
        ------
        string
            An endpoint filtered by the parameter.
    """
    session.commit()
    resultSet = session.query(Endpoints).filter(Endpoints.userID == userID).all()
    return resultSet[0].endpoint

def getAllSubscriptions():
    """Return all the objects of endpoints.
        Returns
        ------
        list
            A list of all endpoints-object.
    """
    session.commit()
    return session.query(Endpoints).all()

def deleteSubscription(endpoint : str):
    """Store a new endpoint.
        Parameters
        ----------
        endpoint : string
            A dictionary of the endpoint.
        Returns
        ------
        boolean
            True if it's the same endpoint.
    """
    session.commit()
    resultSet = session.query(Endpoints).filter(Endpoints.endpoint == endpoint).all()
    submittedEndpoint = json.loads(endpoint)["endpoint"]
    for row in resultSet:
        row_as_dict = {'id': row.id, 'endpoint': row.endpoint, 'userID': row.userID}
        rowEndpoint = json.loads(row_as_dict["endpoint"])["endpoint"]
        if(submittedEndpoint == rowEndpoint):
            print("the same endpoint")
            session.delete(row)
            session.commit()
            return True