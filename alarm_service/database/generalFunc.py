from sqlalchemy import *


def updateTable(connection, table, searchColumn, searchValue, column, value): #Updates a table. searchColumn must be unique. Takes a table variable, a string for column and string/int for value and search value. 
    if(CheckIfExist(connection, table, searchColumn, searchValue) == False):
        return "Does not exist"
    query = update(table).values(**{column: value}).where(table.columns[searchColumn] == searchValue) # **kwargs used to make it work
    connection.execute(query) #Execute the query

def getAllData(connection, table):
    query = select([table])
    result = connection.execute(query) #Execute the query
    return result.fetchall() #returns a list of tuples

def changeToList(result):
    allData = []
    
    for x in result:
        for y in x:
            allData.append(y)
    return allData

def getSpecifiedData(connection, table, desiredColumn, searchColumn, searchValue):
    query = select([table.columns[desiredColumn]]).where(table.columns[searchColumn] == searchValue) 
    result = connection.execute(query) #Execute the query
    result = result.fetchall() #Gets list of tuples
    return changeToList(result)
            
def CheckIfExist(connection, table, column, value): #See if the value exist in the parent table. Takes a Table object, string and the desired value.
    query = select([table.columns[column]]) # SELECT column FROM table
    result = connection.execute(query) #Execute the query
    resultList = result.fetchall() #Data of executed query is put in a list of tuples

    for x in resultList: #check the tuples 
        for y in x:
            if y == value:
                return True
    return False