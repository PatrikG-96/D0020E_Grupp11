from ast import Subscript
from .generalFunc import *
from msilib.schema import ODBCAttribute
import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import *
import json

load_dotenv()

name = os.getenv("NAME")
host = os.getenv("HOST")
password = os.getenv("PASSWORD")
user = os.getenv("USER")

try:
    engine = create_engine(f"mysql://{user}:{password}@{host}/{name}", echo = True) #takes database as one argument, returns an engine object
    #__connection = engine.connect() #Establish DBAPI connection to database
except sqlalchemy.exc.OperationalError:
    print("Can't connect to database")

#Get the tables
metadata = MetaData(bind=engine) #Get the tables from the database
MetaData.reflect(metadata)

#endpoints = Table('endpoints', metadata,
#                     autoload=True, autoload_with=engine)
#elderly = Table('elderly', metadata, autoload=True, autoload_with=engine) #Get information on table
#sensor = Table('sensor', metadata, autoload=True, autoload_with=engine) 
#user = Table('user', metadata, autoload=True, autoload_with=engine) 
#subscription = Table('subscription', metadata, autoload=True, autoload_with=engine) 
#alarm = Table('alarm', metadata, autoload=True, autoload_with=engine) 
#action = Table('action', metadata, autoload=True, autoload_with=engine) 
#client = Table('client', metadata, autoload=True, autoload_with=engine) 

endpoints = metadata.tables['endpoints']
elderly = metadata.tables['elderly']
sensor = metadata.tables['sensor']
user = metadata.tables['user']
subscription = metadata.tables['subscription']
alarm = metadata.tables['alarm']
action = metadata.tables['action']
client = metadata.tables['client']


#The functions
def setNewElderly(name): #Takes one string values as argument
    with engine.connect() as conn:
        query = insert(elderly).values(name=name) #Insert operation
        conn.execute(query) #Execute the query

def setNewUser(client_id, username, password): #Takes two string values as argument
    with engine.connect() as conn:
        query = insert(user).values(client = client_id, username=username, password=password)
        conn.execute(query) #Execute the query

def setNewSubscription(userID, machineID): #Takes two int values as argument
    with engine.connect() as conn:
        query = insert(subscription).values(userID=userID, machineID=machineID) #Insert operation
        conn.execute(query) #Execute the query

def deleteSubcription(userID, machineID):
    with engine.connect() as conn:
        query = delete(subscription).where(and_(subscription.columns.userID == userID, subscription.columns.machineID == machineID))
        conn.execute(query)

def setNewAlarm(alarmFlag, machineID): #Takes one string and one int value as argument
    with engine.connect() as conn:
        query = insert(alarm).values(alarmFlag = alarmFlag, machineID = machineID, received = 0, resolved = 0)
        conn.execute(query)


def addClient(clientID):
    print("test")
    with engine.connect() as conn:
        query = insert(client).values(clientID = clientID)
        conn.execute(query)

def getClients():
    with engine.connect() as conn:
        query = select(client.columns.clientID)
        return conn.execute(query).fetchall()

def readAlarm(alarmID, userID, timestamp):
    with engine.connect() as conn:
        query = insert(action).values(alarmID = alarmID, userID = userID, timestamp = timestamp, actionType = 'READ')
        conn.execute(query)
        query = update(alarm).values(received = 1).where(alarm.columns.alarmID == alarmID)
        conn.execute(query)
    
def resolveAlarm(alarmID, userID, timestamp):
    with engine.connect() as conn:
        query = insert(action).values(alarmID = alarmID, userID = userID, timestamp = timestamp, actionType = 'SOLVED')
        conn.execute(query)
        query = update(alarm).values(resolved = 1).where(alarm.columns.alarmID == alarmID)
        conn.execute(query)
    
def getAllAlarms():
    with engine.connect() as conn:
        query = select(alarm)
        return conn.execute(query).fetchall()
        
    
def getDevices():
    with engine.connect() as conn:
        query = select(sensor)
        return conn.execute(query).fetchall()

def getSubscribers(machineID): #Gets all the users that are subscripted to machineID. Takes an int as argument.
    #return func.getSpecifiedData(__connection, subscription, 'userID', 'machineID', machineID)
    with engine.connect() as conn:
        query = select(subscription.columns.userID).where(subscription.columns.machineID == machineID)
        return conn.execute(query).fetchall()

def getUserDeviceSubscriptions(userID):
    with engine.connect() as conn:
        query = select(alarm.columns.machineID, subscription).where(and_(alarm.columns.machineID == subscription.columns.machineID,
                                                                     subscription.columns.userID == userID))
        return conn.execute(query).fetchall()
    
def getUserActiveAlarms(userID):
    with engine.connect() as conn:
        j = alarm.join(subscription, and_(subscription.columns.machineID == alarm.columns.machineID, subscription.columns.userID == userID))
        query = select(alarm, subscription).where(or_(alarm.columns.received == 0, alarm.columns.resolved == 0)).select_from(j)
        return conn.execute(query).fetchall()


def getClientUser(client_id, username):
    with engine.connect() as conn:
        query = select(user).where(and_(user.columns.username==username, user.columns.client == client_id))
        result = conn.execute(query)
        return result.fetchall()
    


def getUser(userValue): #Returns a user with id, name and password. Takes a int or string
    if (isinstance(userValue, int) == True):
        with engine.connect() as conn:
            query = select(user).where(user.columns.userID == userValue)
            result = conn.execute(query) #Execute the query
            return changeToList(result.fetchall())
    else:
        with engine.connect() as conn:
            query = select(user).where(user.columns.username == userValue)
            result = conn.execute(query) #Execute the query
            return changeToList(result.fetchall())

def getAllAlarmNotRead(): #Returns all alarms that are not read
    with engine.connect() as conn:
        query = select(alarm).where(alarm.columns.received == 0)
        result = conn.execute(query) #Execute the query
        return result.fetchall()



def getAllAlarmNotReadSpecified(user_id):  #Returns a list of alarmID of alarms that are not read of a user. Takes an int as argument.
    if(func.CheckIfExist(__connection, subscription, 'userID', user_id) == True):
        allMachineID = func.getSpecifiedData(__connection, subscription, 'machineID', 'userID', user_id) # A list of the machineID that use is subscribed to
        
        allAlarmID = []
        for x in allMachineID:
            allAlarmID += func.getSpecifiedData(__connection, alarm, 'alarmID', 'machineID', x)

        
        notRead = [] #A list of alarmID of alarms that are not read
        
        for x in allAlarmID:
            query = select(action.columns.alarmID).where(and_(action.columns.alarmID == x, action.columns.hasRead == 0)) 
            result = __connection.execute(query) #Execute the query
            notRead += result.fetchall()
        return func.changeToList(notRead)

    return "UserID do not exist"


def getAllAlarmNotSolved(): #Returns all alarms that are not read
    with engine.connect() as conn:
        j = alarm.join(action, alarm.columns.alarmID == action.columns.alarmID)
        query = select([alarm, action]).where(action.columns.solved==0).select_from(j)
        result = conn.execute(query) #Execute the query
        return result.fetchall()

def getAllAlarmNotSolvedSpecified(user_id):  #Re    turns a list of alarmID of alarms that are not read of a user. Takes an int as argument.
    if(func.CheckIfExist(__connection, subscription, 'userID', user_id) == True):
        allMachineID = func.getSpecifiedData(__connection, subscription, 'machineID', 'userID', user_id) # A list of the machineID that use is subscribed to
        
        allAlarmID = []
        for x in allMachineID:
            allAlarmID += func.getSpecifiedData(__connection, alarm, 'alarmID', 'machineID', x)

        
        notRead = [] #A list of alarmID of alarms that are not read
        
        for x in allAlarmID:
            query = select(action.columns.alarmID).where(and_(action.columns.alarmID == x, action.columns.sovled == 0)) 
            result = __connection.execute(query) #Execute the query
            notRead += result.fetchall()
        return func.changeToList(notRead)


def storeSubscription(endpoint, userID):
    with engine.connect() as connection:
        query = select(endpoints).where(endpoints.columns.endpoint == endpoint)
        resultSet = connection.execute(query).fetchall()
        submittedEndpoint = json.loads(endpoint)["endpoint"]
        for row in resultSet:
            row_as_dict = dict(row)
            rowEndpoint = json.loads(row_as_dict["endpoint"])["endpoint"]
            if(submittedEndpoint == rowEndpoint):
                query = update(endpoints).where(endpoints.columns.endpoint == endpoint).values(endpoint=endpoint, user=userID)
                connection.execute(query)
                return True

        query = insert(endpoints).values(endpoint=endpoint, user=userID)
        connection.execute(query)
        return True

def getSubscription(userID):
    with engine.connect() as connection:
        query = select(endpoints).where(endpoints.columns.user == userID)
        resultSet = connection.execute(query).fetchall()
        for row in resultSet:
            row_as_dict = dict(row)
            return row_as_dict["endpoint"]

def getAllSubscriptions():
    with engine.connect() as connection:
        query = select(endpoints)
        resultSet = connection.execute(query).fetchall()
        return resultSet

def deleteSubscription(endpoint):
    with engine.connect() as connection:
        query = select(endpoints).where(endpoints.columns.endpoint == endpoint)
        resultSet = connection.execute(query).fetchall()
        submittedEndpoint = json.loads(endpoint)["endpoint"]
        for row in resultSet:
            row_as_dict = dict(row)
            rowEndpoint = json.loads(row_as_dict["endpoint"])["endpoint"]
            if(submittedEndpoint == rowEndpoint):
                print("the same endpoint")
                query = delete(endpoints).where(endpoints.columns.endpoint == rowEndpoint)
                connection.execute(query)
                return True