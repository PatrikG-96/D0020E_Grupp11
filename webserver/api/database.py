import sqlalchemy as db
import json

db_name = "d0020e_dev"
user = "root"
password = "D0020E_GRUPP11"
server_name = "localhost"

# Connect to database
# takes database as one argument, returns an engine object
engine = db.create_engine("mysql://" + user + ":" +
                          password + "@" + server_name + "/" + db_name, echo=True)
connection = engine.connect()  # Establish DBAPI connection to database

# Get the tables
metadata = db.MetaData()  # Get the tables from the databases
elderly = db.Table('elderly', metadata, autoload=True,
                   autoload_with=engine)  # Get information on table
sensor = db.Table('sensor', metadata, autoload=True, autoload_with=engine)
user = db.Table('user', metadata, autoload=True, autoload_with=engine)
subscription = db.Table('subscription', metadata,
                        autoload=True, autoload_with=engine)
endpoints = db.Table('endpoints', metadata,
                     autoload=True, autoload_with=engine)
alarm = db.Table('alarm', metadata, autoload=True, autoload_with=engine)
action = db.Table('action', metadata, autoload=True, autoload_with=engine)

# The functions


def newElderly(name):  # Takes one string values as argument
    query = db.insert(elderly).values(name=name)  # Insert operation
    connection.execute(query)  # Execute the query


def newUser(username, password):  # Takes two string values as argument
    query = db.insert(user).values(username=username, password=password)
    connection.execute(query)  # Execute the query


def get_user(user_id=None, username=None):

    print("in get user")
    if user_id is None and username is None:
        raise Exception()

    if user_id is None:

        query = db.select(user).where(user.columns.username == username)
        return connection.execute(query).fetchall()[0]

    if username is None:

        query = db.select(user).where(user.columns.user_id == user_id)
        return connection.execute(query).fetchall()[0]

    query = db.select(user).where(user.columns.username ==
                                  username, user.columns.user_id == user_id)
    return connection.execute(query).fetchall()[0]


def newSubscription(userID, machineID):  # Takes two int values as argument
    try:
        query = db.insert(alarm).values(
            userID=userID, machineID=machineID)  # Insert operation
        connection.execute(query)  # Execute the query
    except db.exc.IntegrityError:
        print("Foreign key constraint: machineID and/or userID do not exist")


def newAlarm(alarmFag, machineID):  # Takes one string and one int value as argument
    try:
        query = db.insert(alarm).values(alarmFlag=alarmFag,
                                        machineID=machineID)  # Insert operation
        connection.execute(query)  # Execute the query
    except db.exc.IntegrityError:
        print("Foreign key constraint: machineID do not exist")


def newAction(alarmID):  # Takes one int value as argument
    try:
        query = db.insert(action).values(
            alarmID=alarmID, hasRead=0, solved=0)  # Insert operation
        connection.execute(query)  # Execute the query
    except db.exc.IntegrityError:
        print("Foreign key constraint: alarmID do not exist")


# Updates the Action table, either 'hasRead' or 'solved'. Takes one string as argument. Not finished
def updateAction(column, actionID):
    if(CheckIfExist(actionID, action) != 1):
        return "Does not exist"
    db.update(action).values(column=1).where(actionID=actionID)

# Error handling


def CheckIfExist(value, table):  # See if the value exist in the parent table
    query = db.select([table])  # SELECT * FROM *table*
    result = connection.execute(query)  # Execute the query
    resultSet = result.fetchall()  # Data of executed query is put in a list of tuples
    for x in resultSet:  # check the tuples
        for y in x:  # check the elements in the tuple
            if value == y:
                return True
    return False


def storeSubscription(endpoint, userID):
    connection = engine.connect()
    query = db.select(endpoints).where(endpoints.columns.endpoint == endpoint)
    resultSet = connection.execute(query).fetchall()
    submittedEndpoint = json.loads(endpoint)["endpoint"]
    for row in resultSet:
        row_as_dict = dict(row)
        rowEndpoint = json.loads(row_as_dict["endpoint"])["endpoint"]
        if(submittedEndpoint == rowEndpoint):
            query = db.update(endpoints).where(endpoints.columns.endpoint == endpoint).values(endpoint=endpoint, user=userID)
            connection.execute(query)
            connection.close()
            return True

    query = db.insert(endpoints).values(endpoint=endpoint, user=userID)
    connection.execute(query)
    connection.close()
    return True

def getSubscription(userID):
    connection = engine.connect()
    query = db.select(endpoints).where(endpoints.columns.user == userID)
    resultSet = connection.execute(query).fetchall()
    for row in resultSet:
        row_as_dict = dict(row)
        return row_as_dict["endpoint"]

def getAllSubscriptions():
    connection = engine.connect()
    query = db.select(endpoints)
    resultSet = connection.execute(query).fetchall()
    return resultSet

def deleteSubscription(endpoint):
    connection = engine.connect()
    query = db.select(endpoints).where(endpoints.columns.endpoint == endpoint)
    resultSet = connection.execute(query).fetchall()
    submittedEndpoint = json.loads(endpoint)["endpoint"]
    for row in resultSet:
        row_as_dict = dict(row)
        rowEndpoint = json.loads(row_as_dict["endpoint"])["endpoint"]
        if(submittedEndpoint == rowEndpoint):
            print("the same endpoint")
            query = db.delete(endpoints).where(endpoints.columns.endpoint == rowEndpoint)
            connection.execute(query)
            connection.close()
            return True