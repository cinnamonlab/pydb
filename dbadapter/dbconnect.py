import mysql.connector
import time


from collections import OrderedDict

class DBConnect(object):
    """
        Python Class for connecting  with MySQL server and accelerate development project using MySQL
        Extremely easy to learn and use, friendly construction.
    """

    __instance = None
    __host = None
    __user = None
    __password = None
    __database = None
    __session = None
    __connection = None

    def __init__(self, host='localhost', user='root', password='', database=''):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

    def startTransaction(self):
        try:
            cnx = mysql.connector.connect(host=self.__host, user=self.__user, password=self.__password, database=self.__database)
            self.__connection = cnx
            self.__session = cnx.cursor()
        except mysql.connector.Error as err:
            print("Error %d: %s" % (err.args[0], err.args[1]))

    def endTransaction(self):
        self.__session.close()
        self.__connection.close()
        self.__session = None
        self.__connection = None

    def commitTransaction(self):
        self.__connection.commit()

    def rollbackTransaction(self):
        self.__connection.rollback()

    def execute(self, query: str):
        self.__session.execute(query)
        self.__log(query)


    def fetch(self, query: str):
        self.__session.execute(query)
        self.__log(query)
        return self.__association_result()

    def __association_result(self):
        result = [item for item in self.__session.fetchall()]
        if result == None:
            return None

        desc = self.__session.description

        assRes = []
        for item in result:
            dict = {}
            for (name, value) in zip(desc, item):
                dict[name[0]] = value
            assRes.append(dict)
        return assRes

    def __log(self, context=None, platform='P'):
        print("Log: ", context)
# END



    def __open(self):
        try:
            cnx = mysql.connector.connect(host=self.__host, user=self.__user, password=self.__password,
                                          database=self.__database)
            self.__connection = cnx
            self.__session = cnx.cursor()
        except mysql.connector.Error as err:
            print("Error %d: %s" % (err.args[0], err.args[1]))

    ## End def __open

    def __close(self):
        self.__session.close()
        self.__connection.close()

    ## End def __close

    def show_columns(self, table):
        """
        Show all columns name from provided table name
        """
        self.__open()
        self.__session.execute("SHOW columns FROM {0}".format(table))
        result = [column[0] for column in self.__session.fetchall()]
        self.__close()

        return result

    def select(self, table, where=None, *args, **kwargs):
        result = None
        query = 'SELECT '
        keys = args
        values = tuple(kwargs.values())
        l = len(keys) - 1

        for i, key in enumerate(keys):
            query += "`" + key + "`"
            if i < l:
                query += ","
        ## End for keys

        query += ' FROM %s' % table

        if where:
            query += " WHERE %s" % where
        ## End if where
        self.log(query)
        self.__open()
        self.__session.execute(query, values)
        result = [item for item in self.__session.fetchall()]
        self.__close()

        return result

    ## End def select

    def update(self, table, where=None, *args, **kwargs):
        values = ()
        if args:
            values = tuple(args)
        if kwargs:
            values += tuple(kwargs.values())
        if values == ():
            return 0
        query = "UPDATE %s SET " % table
        keys = kwargs.keys()
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`" + key + "` = %s"
            if i < l:
                query += ","
                ## End if i less than 1
        ## End for keys
        query += " WHERE %s" % where

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        update_rows = self.__session.rowcount
        self.__close()

        return update_rows

    ## End function update

    def insert(self, table, *args, **kwargs):
        values = None
        query = "INSERT INTO %s " % table
        if kwargs:
            keys = kwargs.keys()
            values = tuple(kwargs.values())
            query += "(" + ",".join(["`%s`"] * len(keys)) % tuple(keys) + ") VALUES (" + ",".join(
                ["%s"] * len(values)) + ")"
        elif args:
            values = args
            query += " VALUES(" + ",".join(["%s"] * len(values)) + ")"

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()
        self.__close()
        return self.__session.lastrowid

    ## End def insert

    def delete(self, table, where=None, *args):
        query = "DELETE FROM %s" % table
        if where:
            query += ' WHERE %s' % where

        values = tuple(args)

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        delete_rows = self.__session.rowcount
        self.__close()

        return delete_rows

    ## End def delete

    def select_advanced(self, sql, *args):
        start_time = time.time()
        od = OrderedDict(args)
        query = sql
        values = tuple(od.values())
        self.__open()
        self.__session.execute(query, values)
        result = self.associationResult()#[item for item in self.__session.fetchall()]
        self.__close()
        end_time = time.time()
        print("Time: "+str(end_time-start_time))
        self.log(sql)
        return result
        ## End def select_advanced
        ## End class

    def log(self, context = None, platform = 'P'):
        print(context)
        self.insert('ai_logs', content=context, platform=platform)

    def associationResult(self):
        result = [item for item in self.__session.fetchall()]
        if result == None:
            return None
        desc = self.__session.description

        assRes = []
        for item in result:
            dict = {}
            for (name, value) in zip(desc, item):
                dict[name[0]] = value
            assRes.append(dict)
        return assRes
# Extract information config  from config.json file at the root folder
