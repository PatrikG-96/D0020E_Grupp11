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
def setNewMonitor(name : str): #Takes one string values as argument
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

def setNewUser(username : str, password : str, name : str): #Takes three string values as argument
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

def deleteUser(userValue : str or int): #Takes either userID or username
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

def setNewSubscription(userID : int, monitorID : int): #Takes two int values as argument
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

def deleteSubscriber(userID : int, monitorID : int):
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

def setNewDevice(monitorID : int):
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

def deleteMonitor(monitorID : int):
    """Deletes a monitor.

        Parameters
        ----------
        monitorID : int
            The identification of a monitor.
    """

    session.query(Monitor).filter(Monitor.monitorID == monitorID).delete()
    session.commit()

def deleteDevice(deviceID : int):
    """Deletes a sensor.

        Parameters
        ----------
        deviceID : int
            The identification of a device.
    """
    session.query(Sensor).filter(Sensor.deviceID == deviceID).delete()
    session.commit()

def setNewAlarm(monitorID : int, alarmType : int, timestamp : str): #Takes two string an one  value as argument
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

    alarmObj = Alarm(monitorID = monitorID, alarmType = alarmType, read = 0, resolved = 0, timestamp = timestamp)
    session.add(alarmObj)
    session.commit()
    return alarmObj

def readAlarm(alarmID : int, userID : int, timestamp : str, actionType : str):
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

    actionObj = Action(alarmID = alarmID, userID = userID, actionType = actionType, timestamp = timestamp)
    session.add(actionObj)
    obj = session.query(Alarm).get(alarmID)
    obj.read = 1
    session.commit()
    return actionObj
    
def resolveAlarm(alarmID : int, userID : int, timestamp : str, actionType : str):
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

    actionObj = Action(alarmID = alarmID, userID = userID, actionType = actionType, timestamp = timestamp)
    session.add(actionObj)
    obj = session.query(Alarm).get(alarmID)
    obj.resolved = 1
    session.commit()
    return actionObj
    
def getAllAlarms(): #Returns a resultset in the form of list of objects.
    """Return all the objects of alarm.

        Returns
        ------
        list
            A list of all alarm-object in the database.
    """

    return session.query(Alarm).all()
        
    
def getDevices():#Returns a resultset in the form of list of objects.
    """Return all the objects of sensor.

        Returns
        ------
        list
            A list of all sensor-object in the database.
    """
    return session.query(Sensor).all()

def getSubscribers(monitorID : int): #Gets all the users that are subscripted to a monitor. Takes an int as argument.
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

def getSubscribers(deviceID : int): #Gets all the users that are subscripted to a monitor through deviceID. Takes an int as argument.
    #select subscription.userID from subscription inner join sensor on sensor.deviceID=machineID where sensor.monitorID=subscription.monitorID
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

    result=session.query(Subscription).join(Sensor, Sensor.deviceID == deviceID).filter(Sensor.monitorID==Subscription.monitorID).all()
    return result

def getUserDeviceSubscriptions(userID : int):
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

    result=session.query(Sensor).join(Subscription, Subscription.userID == userID).filter(Subscription.monitorID==Sensor.monitorID).all()
    #result = session.query(Sensor.deviceID, Subscription).filter(Subscription.monitorID==Sensor.monitorID, Subscription.userID==userID).all()
    return result
    
def getUserActiveAlarms(userID : int):
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

    result = session.query(Alarm).filter(Alarm.monitorID==Subscription.monitorID, 
        Subscription.userID==userID, or_(Alarm.read==0, Alarm.resolved==0)).all()
    return result

def getUser(userValue : int or str): #Returns a user with id, name and password. Takes a int or string
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

    if (isinstance(userValue, int) == True):
        result = session.query(User).filter(User.userID == userValue)
        if not result: #If user do not exist
            return False
        return result[0]

    else:
        result = session.query(User).filter(User.username == userValue)
        if not result:
            return False
        return result[0]

def getAllAlarmNotRead(): #Returns all alarms that are not read
    """Return all the objects that are not read of alarm.

        Returns
        ------
        list
            A list of all alarm-object filtered by parameter in the database.
    """

    result = session.query(Alarm).filter(Alarm.read==0).all()
    return result

def getAllAlarmNotSolved(): #Returns all alarms that are not solved
    """Return all the objects that are not resolved of alarm.

        Returns
        ------
        list
            A list of all alarm-object filtered by parameter in the database.
    """
    result = session.query(Alarm).filter(Alarm.resolved == 0).all()
    return result


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
    resultSet = session.query(Endpoints).filter(Endpoints.userID == userID).all()
    return resultSet[0].endpoint

def getAllSubscriptions():
    """Return all the objects of endpoints.

        Returns
        ------
        list
            A list of all endpoints-object.
    """
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
