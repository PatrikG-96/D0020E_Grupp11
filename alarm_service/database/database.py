from sqlalchemy import *
import sqlalchemy
import generalFunc as func



def test(): #Database from database-course
    
    engine2 = create_engine("mysql://root@localhost/sportscar", echo = True) #takes database as one argument, returns an engine object
    connection2 = engine2.connect() #Establish DBAPI connection to database
    metadata2 = MetaData() #Get the tables from the database
    users = Table('users', metadata2, autoload=True, autoload_with=engine2) #Get information on table
    basket = Table('basket', metadata2, autoload=True, autoload_with=engine2) #Get information on table
    #print(users.columns.keys()) #Print the column-names
    #print(repr(metadata2.tables['users'])) #Print full table
    queryP = select(users) # SELECT * FROM users
    result2 = connection2.execute(queryP) #Execute the query
    resultSet2 = result2.fetchall() #Data of executed query is put in a list of tuples
    print(resultSet2)
    #print(func.CheckIfExist(connection, users, 'usersID', 66))
    print(func.getSpecifiedData(connection2, users, 'usersUID', 'usersID', '1'))
    #print(func.updateTable(connection, users, 'usersID', 2, 'usersUID', 'testu66'))



#Connect to database
try:
    engine = create_engine("mysql://root@localhost/d0020e_g11", echo = True) #takes database as one argument, returns an engine object
    connection = engine.connect() #Establish DBAPI connection to database
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
    connection.execute(query) #Execute the query

def setNewUser(username, password): #Takes two string values as argument
    query = insert(user).values(username=username, password=password)
    connection.execute(query) #Execute the query

def setNewSubscription(userID, machineID): #Takes two int values as argument
    try:
        query = insert(alarm).values(userID=userID, machineID=machineID) #Insert operation
        connection.execute(query) #Execute the query
    except sqlalchemy.exc.IntegrityError:
        print("Foreign key constraint: value of value of machineID and/or userID do not exist")

def setNewAlarmAndAction(alarmFlag, machineID): #Takes one string and one int value as argument
    trans = connection.begin()
    try:
        query = insert(alarm).values(alarmFlag=alarmFlag, machineID=machineID) #Insert operation
        result=connection.execute(query) #Execute the query
        alarm_id = result.inserted_primary_key[0]

        #Set in action table
        query = insert(action).values(alarmID=alarm_id, hasRead=0, solved=0) #Insert operation
        connection.execute(query)
        trans.commit()
    except:
        trans.rollback()

def logIn(username, password): #Checks if the username and password exist in the table. Takes two string as argument
    if(func.CheckIfExist(connection, user, 'username', username) == True and func.CheckIfExist(connection, user, 'password', password) == True):
        return True
    return False    

def getSubscribers(machineID): #Gets all the users that are subscripted to machineID. Takes an int as argument.
    return func.getSpecifiedData(connection, subscription, 'userID', 'machineID', machineID)

def getUser(userValue): #Returns a user with id, name and password. Takes a int or string
    if (isinstance(userValue, int) == True):
        query = select(user).where(user.columns.userID == userValue)
        result = connection.execute(query) #Execute the query
        return func.changeToList(result.fetchall())
    else:
        query = select(user).where(user.columns.username == userValue)
        result = connection.execute(query) #Execute the query
        return func.changeToList(result.fetchall())

def getAllAlarmNotRead(): #Returns all alarms that are not read
    query = select(action).where(action.columns.hasRead == 0)
    result = connection.execute(query) #Execute the query
    return result.fetchall()

def getAllAlarmNotReadSpecified(user_id):  #Returns a list of alarmID of alarms that are not read of a user. Takes an int as argument.
    if(func.CheckIfExist(connection, subscription, 'userID', user_id) == True):
        allMachineID = func.getSpecifiedData(connection, subscription, 'machineID', 'userID', user_id) # A list of the machineID that use is subscribed to
        
        allAlarmID = []
        for x in allMachineID:
            allAlarmID += func.getSpecifiedData(connection, alarm, 'alarmID', 'machineID', x)

        
        notRead = [] #A list of alarmID of alarms that are not read
        
        for x in allAlarmID:
            query = select(action.columns.alarmID).where(and_(action.columns.alarmID == x, action.columns.hasRead == 0)) 
            result = connection.execute(query) #Execute the query
            notRead += result.fetchall()
        return func.changeToList(notRead)

    return "UserID do not exist"



 

name='testu6666555'
passWord='passpass66665'
setNewUser(name, passWord)
#test()