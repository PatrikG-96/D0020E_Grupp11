from generalFunc import *
from msilib.schema import ODBCAttribute
import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import *

load_dotenv()

name = os.getenv("NAME")
host = os.getenv("HOST")
password = os.getenv("PASSWORD")
user = os.getenv("USER")

try:
    engine = create_engine(f"mysql://{user}:{password}@{host}/{name}", echo = False) #takes database as one argument, returns an engine object
    __connection = engine.connect() #Establish DBAPI connection to database
except sqlalchemy.exc.OperationalError:
    print("Can't connect to database")

#Get the tables
metadata = MetaData() #Get the tables from the database
elderly = Table('elderly', metadata, autoload=True, autoload_with=engine) #Get information on table
sensor = Table('sensor', metadata, autoload=True, autoload_with=engine) 
user = Table('user', metadata, autoload=True, autoload_with=engine) 
subscription = Table('subscription', metadata, autoload=True, autoload_with=engine) 
alarm = Table('alarm', metadata, autoload=True, autoload_with=engine) 
action = Table('action', metadata, autoload=True, autoload_with=engine) 

#The functions
def setNewElderly(name): #Takes one string values as argument
    query = insert(elderly).values(name=name) #Insert operation
    __connection.execute(query) #Execute the query

def setNewUser(username, password): #Takes two string values as argument
    query = insert(user).values(username=username, password=password)
    __connection.execute(query) #Execute the query

def setNewSubscription(userID, machineID): #Takes two int values as argument
    try:
        query = insert(alarm).values(userID=userID, machineID=machineID) #Insert operation
        __connection.execute(query) #Execute the query
    except sqlalchemy.exc.IntegrityError:
        print("Foreign key constraint: value of value of machineID and/or userID do not exist")

def setNewAlarmAndAction(alarmFlag, machineID): #Takes one string and one int value as argument
    trans = __connection.begin()
    try:
        query = insert(alarm).values(alarmFlag=alarmFlag, machineID=machineID) #Insert operation
        result=__connection.execute(query) #Execute the query
        alarm_id = result.inserted_primary_key[0]

        #Set in action table
        query = insert(action).values(alarmID=alarm_id, hasRead=0, solved=0) #Insert operation
        __connection.execute(query)
        trans.commit()
    except:
        trans.rollback()

def logIn(username, password): #Checks if the username and password exist in the table. Takes two string as argument
    if(func.CheckIfExist(__connection, user, 'username', username) == True and func.CheckIfExist(__connection, user, 'password', password) == True):
        return True
    return False    

def getSubscribers(machineID): #Gets all the users that are subscripted to machineID. Takes an int as argument.
    return func.getSpecifiedData(__connection, subscription, 'userID', 'machineID', machineID)

def getUser(userValue): #Returns a user with id, name and password. Takes a int or string
    if (isinstance(userValue, int) == True):
        query = select(user).where(user.columns.userID == userValue)
        result = __connection.execute(query) #Execute the query
        return changeToList(result.fetchall())
    else:
        query = select(user).where(user.columns.username == userValue)
        result = __connection.execute(query) #Execute the query
        return changeToList(result.fetchall())

def getAllAlarmNotRead(): #Returns all alarms that are not read
    query = select(action).where(action.columns.hasRead == 0)
    result = __connection.execute(query) #Execute the query
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


