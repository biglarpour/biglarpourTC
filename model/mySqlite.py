__author__ = 'abo.biglarpour'

import sqlite3
import threading
import json

class MySqlite(object):
    locks = {}
    lock = threading.Lock()

    def __init__(self, dbPath):
        """
        Abstact sqlite3 object for all handling of sql operations
        :param dbPath: full path to database file
        """
        super(MySqlite, self).__init__()
        self.dbPath = dbPath

    @staticmethod
    def dictionaryFactory(cursor, row):
        """
        :param cursor: sql cursor object
        :param row: current row being fetched
        :return: a dictionary of columns and there values for the given row
        """
        d = {}
        for idx,col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def connect(self):
        """
        connect to a sqlite3 database
        :param self.dbPath: full path to the database
        :return: a sqlite3 connect object
        """
        connect = sqlite3.connect(self.dbPath)
        connect.row_factory = self.dictionaryFactory
        return connect

    def createTable(self, tableName, columnsDict, foreignKeys=None):
        """
        creates a table if not already exists
        :param tableName: name of the table
        :param columnsDict: a json dumps dictionary with keys as columns and values as column type
        """
        if foreignKeys is None:
            foreignKeys = []
        columnsDict = json.loads(columnsDict)
        with self.connect() as con:
            cur  = con.cursor()
            self.lockForPath(self.dbPath)
            columns = ",".join("%s %s"%(key, value) for key, value in columnsDict.items())
            for foreign in foreignKeys:
                columns += ", FOREIGN KEY (%(key)s) REFERENCES %(refTable)s (%(refValue)s)"%foreign
            cur.execute("CREATE TABLE IF NOT EXISTS %s(%s)"%(tableName, columns))
        self.unlockForPath(self.dbPath)


    def addValue(self, tableName, valueDict):
        """
        Add a single row to the table
        :param valueDict: a json dumps dictionary of all the columns and values to insert
                          Keys are column names and values are the value to insert
        """
        if not isinstance(valueDict, dict):
            valueDict = json.loads(valueDict)
        with self.connect() as con:
            self.lockForPath(self.dbPath)
            cur = con.cursor()
            columns = ",".join(valueDict.keys())
            addData  = tuple(valueDict.values())
            valueStr = "?,"*len(addData)
            valueStr = valueStr[0:-1]
            addCmd = "INSERT INTO %s(%s) VALUES(%s)"%(tableName, columns, valueStr)
            cur.execute(addCmd, addData)
        self.unlockForPath(self.dbPath)

    def addListValues(self, tableName, valueList):
        """
        Calls addValue on each list item
        :param valueList: list of dictionaries. see addValue for more info.
        """
        valueList = json.loads(valueList)
        for valueDict in valueList:
            self.addValue(tableName, valueDict)

    def queryValues(self, tableName, queryDict, fetchone=False):
        """
        Query a list of rows based on the provided key and value
        :param queryDict: a dictionary of all the keys and values to validate against
                          if queryDict is NoneType, method will return all rows for table
        :return: a list of rows that match the queryDict keys and values
        """
        con = self.connect()
        cur = con.cursor()
        queryData = tuple()
        queryColumns = ""
        if isinstance(queryDict, dict):
            queryData = tuple(queryDict.values())
            queryColumns = "WHERE %s"%self.getTagString(queryDict.keys())
        queryCmd = "SELECT * FROM %s %s"%(tableName, queryColumns)
        cur.execute(queryCmd, queryData)
        if fetchone:
            return cur.fetchone()
        return cur.fetchall()

    def rowExists(self, tableName, queryDict):
        """
        Checks if a specific row exists
        :param queryDict: a dictionary of all the keys and values to validate against.
        :return: Boolean whether the row exists or not
        """
        con = self.connect()
        cur = con.cursor()
        queryData = tuple(queryDict.values())
        queryColumns = self.getTagString(queryDict.keys())
        cur.execute(
            "SELECT COUNT(*) FROM %s WHERE %s"%(tableName, queryColumns), queryData)
        result = cur.fetchone()
        if result.get('COUNT(*)') == 1:
            return True
        return False

    def tableExists(self, tableName):
        """
        Checks if table exists in the database
        :param tableName: name of table
        :return: Boolean
        """
        con = self.connect()
        cur = con.cursor()
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='{0}'".format(tableName))
        if cur.fetchone():
            return True

        return False

    def updateRow(self, tableName, queryDict, valueDict):
        """
        Update row based on queryDict with the valueDict
        :param queryDict: a dictionary of all the keys and values to validate against.
        :param valueDict: a dictionary of all the columns and values to update
        """
        valueDict = json.loads(valueDict)
        queryDict = json.loads(queryDict)
        if self.rowExists(tableName, queryDict):
            with self.connect() as con:
                self.lockForPath(self.dbPath)
                cur = con.cursor()
                valuesStr = ",".join("%s=?"%key for key in valueDict.keys())
                tagStr = " AND ".join("%s=?"%key for key in queryDict.keys())
                dataDict = valueDict.values()
                dataDict.extend(queryDict.values())
                updateCmd = "UPDATE %s SET %s WHERE %s"%(tableName, valuesStr, self.getTagString(queryDict.keys()))
                cur.execute(updateCmd, tuple(dataDict))
            self.unlockForPath(self.dbPath)
        else:
            self.addValue(tableName, valueDict)

    def getTagString(self, tags):
        """
        given a set of tags or keys creates a SQL formatted string with AND separated
        :param tags: list of tags or keys
        :return: AND separated string of keys equaled to ?. ie. "Country=? AND City=?"
        """
        return ' AND '.join("%s=?"%tag for tag in tags)

    def lockForPath(self, lockName):
        """
        Using thread locking lock the path and insert into dictionary cache
        :param lockName: the path or key to the db file to lock
        """
        lockInfo = self.locks.get(lockName, None)
        if lockInfo is None:
            self.locks[lockName] = [threading.Lock(), None]
            lockInfo = self.locks[lockName]
        print '__lockForPath:: acquiring %s' % lockName
        lockInfo[0].acquire()
        lockInfo[1] = threading.Timer(10, self.lockReleaseTimer, args=[lockName])
        lockInfo[1].start()
        print '__lockForPath:: acquired %s' % lockName

    def lockReleaseTimer(self, lockName):
        """
        Forced released of locked process lockName
        :param lockName: the path or key to the db file to lock
        """
        self.unlockForPath(lockName)

    def unlockForPath(self, lockName):
        """
        Using thread locking unlock the path
        :param lockName: the path or key to the db file to lock
        """
        lockInfo = self.locks.get(lockName, None)
        if lockInfo is not None:
            lockInfo[1].cancel()
            lockInfo[0].release()
            print '__unlockForPath:: %s' % lockName