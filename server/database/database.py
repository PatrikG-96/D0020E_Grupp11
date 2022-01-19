import sqlalchemy as db

def test(): #Database from database-course
    engine2 = db.create_engine("mysql://root@localhost/sportscar", echo = True) #takes database as one argument, returns an engine object
    connection2 = engine2.connect() #Establish DBAPI connection to database
    metadata2 = db.MetaData() #Get the tables from the database
    users = db.Table('users', metadata2, autoload=True, autoload_with=engine2) #Get information on table

    #print(users.columns.keys()) #Print the column-names
    #print(repr(metadata.tables['users'])) #Print full table
    queryP = db.select([users]) # SELECT * FROM users
    result2 = connection2.execute(queryP) #Execute the query
    resultSet2 = result2.fetchall() #Data of executed query is put in a list of tuples
    print(resultSet2)


#Connect to database
engine = db.create_engine("mysql://root@localhost/d0020e_g11", echo = True) #takes database as one argument, returns an engine object
connection = engine.connect() #Establish DBAPI connection to database

#Get the tables
metadata = db.MetaData() #Get the tables from the database
elderly = db.Table('elderly', metadata, autoload=True, autoload_with=engine) #Get information on table
sensor = db.Table('sensor', metadata, autoload=True, autoload_with=engine) 
user = db.Table('user', metadata, autoload=True, autoload_with=engine) 
subscription = db.Table('subscription', metadata, autoload=True, autoload_with=engine) 
alarm = db.Table('alarm', metadata, autoload=True, autoload_with=engine) 
action = db.Table('action', metadata, autoload=True, autoload_with=engine) 

#The functions
def newElderly(name): #Takes one string values as argument
    query = db.insert(elderly).values(name=name) #Insert operation
    connection.execute(query) #Execute the query

def newUser(username, password): #Takes two string values as argument
    query = db.insert(user).values(username=username, password=password)
    connection.execute(query) #Execute the query

def newSubscription(userID, machineID): #Takes two int values as argument
    try:
        query = db.insert(alarm).values(userID=userID, machineID=machineID) #Insert operation
        connection.execute(query) #Execute the query
    except db.exc.IntegrityError:
        print("Foreign key constraint: machineID and/or userID do not exist")

def newAlarm(alarmFag, machineID): #Takes one string and one int value as argument
    try:
        query = db.insert(alarm).values(alarmFlag=alarmFag, machineID=machineID) #Insert operation
        connection.execute(query) #Execute the query
    except db.exc.IntegrityError:
        print("Foreign key constraint: machineID do not exist")

def newAction(alarmID): #Takes one int value as argument
    try:
        query = db.insert(action).values(alarmID=alarmID, hasRead=0, solved=0) #Insert operation
        connection.execute(query) #Execute the query
    except db.exc.IntegrityError:
        print("Foreign key constraint: alarmID do not exist")

def updateAction(column, actionID): #Updates the Action table, either 'hasRead' or 'solved'. Takes one string as argument. Not finished
    if(CheckIfExist(actionID, action) != 1):
        return "Does not exist"
    db.update(action).values(column=1).where(actionID=actionID)

#Error handling
def CheckIfExist(value, table): #See if the value exist in the parent table
    query = db.select([table]) # SELECT * FROM *table*
    result = connection.execute(query) #Execute the query
    resultSet = result.fetchall() #Data of executed query is put in a list of tuples
    for x in resultSet: #check the tuples 
        for y in x: #check the elements in the tuple
            if value == y:
                return 1


