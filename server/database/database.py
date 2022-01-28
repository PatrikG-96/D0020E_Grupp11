from sqlalchemy import *



def test(): #Database from database-course
    engine2 = create_engine("mysql://root@localhost/sportscar", echo = True) #takes database as one argument, returns an engine object
    connection2 = engine2.connect() #Establish DBAPI connection to database
    metadata2 = MetaData() #Get the tables from the database
    users = Table('users', metadata2, autoload=True, autoload_with=engine2) #Get information on table
    
    #print(users.columns.keys()) #Print the column-names
    #print(repr(metadata2.tables['users'])) #Print full table
    #queryP = db.select(users) # SELECT * FROM users
    #result2 = connection2.execute(queryP) #Execute the query
    #resultSet2 = result2.fetchall() #Data of executed query is put in a list of tuples
    #print(resultSet2)
    #print(CheckIfExist(users, 'usersID', 1))
    #print(getSpecifiedData(users, 'usersUID', 'usersID', '1'))
    print(updateTable(users, 'usersID', 2, 'usersUID', 'asta2'))



#Connect to database
engine = create_engine("mysql://root@localhost/d0020e_g11", echo = True) #takes database as one argument, returns an engine object
connection = engine.connect() #Establish DBAPI connection to database

# #Get the tables
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
    except exc.IntegrityError:
        print("Foreign key constraint: value of value of machineID and/or userID do not exist")

def setNewAlarm(alarmFag, machineID): #Takes one string and one int value as argument
    try:
        query = insert(alarm).values(alarmFlag=alarmFag, machineID=machineID) #Insert operation
        connection.execute(query) #Execute the query
    except exc.IntegrityError:
        print("Foreign key constraint: machineID do not exist")

def setNewAction(alarmID): #Takes one int value as argument
    try:
        query = insert(action).values(alarmID=alarmID, hasRead=0, solved=0) #Insert operation
        connection.execute(query) #Execute the query
    except exc.IntegrityError:
        print("Foreign key constraint: value of alarmID do not exist")

#Fungerar ej. FUUUUUUCK
def updateTable(table, searchColumn, searchValue, column, value): #Updates a table. searchColumn must be unique. Takes a table variable, a string for column and string/int for value and search value. 
    if(CheckIfExist(table, searchColumn, searchValue) != 1):
        return "Does not exist"
    query = update(table).values(**{column: value}).where(table.columns[searchColumn]==searchValue)
    connection.execute(query) #Execute the query


def getAllData(table):
    query = select([table])
    result = connection.execute(query) #Execute the query
    return result.fetchall() #returns a list of tuples


def getSpecifiedData(table, desiredColumn, searchColumn, searchValue):
    query = select([table.columns[desiredColumn]]).where(table.columns[searchColumn] == searchValue) 
    result = connection.execute(query) #Execute the query
    return(result.fetchall())


#Error handling

def getColumnIndex(table, column):
    columnsOfTable = table.columns.keys() #Get the columns of the table

    for x in columnsOfTable:
        if x == column: 
            #print(index)
            return columnsOfTable.index(x)
            

def CheckIfExist(table, column, value): #See if the value exist in the parent table. Takes a Table object, string and the desired value.
    query = select([table]) # SELECT * FROM table
    result = connection.execute(query) #Execute the query
    resultList = result.fetchall() #Data of executed query is put in a list of tuples
    
    index = getColumnIndex(table, column)

    for x in resultList: #check the tuples 
        if x[index] == value:
            return 1


name='testu6666555'
passWord='passpass66665'
setNewUser(name, passWord)
#test()