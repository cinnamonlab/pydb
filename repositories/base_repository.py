from dbadapter.dbconnect import DBConnect

class BaseRepository:
    ''' Base model that implement basic queries into function '''

    __db = None
    __tableName = None

    __selectQuery = "SELECT * FROM {table}"
    __insertQuery = "INSERT INTO {table} ({columns}) VALUES ({values})"
    __updateQuery = "UPDATE {table} SET {setData} WHERE {condition}"
    __deleteQuery = "DELETE FROM {table} WHERE {condition}"

    __defaultOrder = {"modified": "DESC"}

    __queries = []

    def __init__(self, db: DBConnect, tableName: str):
        '''
        Init Repository with table-name. DBConnect is created automatically.
        :param tableName: Name of table to access.
        '''
        self.__db = db
        self.__tableName = tableName

    # Transactions

    def begin_transaction(self):
        self.__queries.clear()

    def end_transaction(self):
        if len(self.__queries) == 0:
            return

        try:
            self.__db.startTransaction()
            for query in self.__queries:
                self.__db.execute(query)
        except Exception as error:
            print("Error on execute query: ", error)
            self.__db.rollbackTransaction()
        else:
            self.__db.commitTransaction()
        finally:
            self.__db.endTransaction()

    # Queries

    def get_objects(self, where={}, page=0, limit=20, orderBy=__defaultOrder):
        '''
        Get all objects, which matching condition {where}. Then sort by (orderBy} with {limit} at {page}.
        :param where: condition to query. Format {name: value} or {name: {value1, ...}}
        :param page: page number. Start from 0.
        :param limit: limit number. Default at 20.
        :param orderBy: condition to order. Format {name: ASC/DESC}
        :return: list of Object.
        '''

        objects = []
        try:
            self.__db.startTransaction()
            selectQuery = self.__parse_select_query(where=where, page=page, limit=limit, orderBy=orderBy)
            objects = self.__db.fetch(selectQuery)
        except Exception as error:
            print("Error on get objects: ", error)
        finally:
            self.__db.endTransaction()
            return objects

    def get_first_object(self, where={}, orderBy=__defaultOrder):
        '''
        Get first object matching condition {where} with {orderBy}.
        :param where: condition to query. Format {name: value} or {name: {value1, ...}}
        :param orderBy: condition to order. Format {name: ASC/DESC}
        :return: first Object or None.
        '''

        objects = []
        try:
            self.__db.startTransaction()
            selectQuery = self.__parse_select_query(where=where, orderBy=orderBy, page=0, limit=1)
            objects = self.__db.fetch(selectQuery)
        except Exception as error:
            print("Error on get first object: ", error)
        finally:
            self.__db.endTransaction()
            return next(iter(objects), None)

    def get_first_object_by_id(self, id):
        '''
        Get first object matching with {id}
        :param id: Id of object to select.
        :return: first Object or None.
        '''
        return self.get_first_object(where={"id": id})

    def update_object(self, setFields: dict, where: dict):
        '''
        Update object's data {setFields}, which matching condition {where}.
        :param setFields: fields to update. Format {name: update-value}
        :param where: condition to query. Format {name: value} or {name: {value1, ...}}
        :return: None
        '''

        updateQuery = self.__parse_update_query(setFields=setFields, where=where)
        self.__queries.append(updateQuery)

    def update_object_by_id(self, id, setFields: dict):
        '''
        Update object's data {setFields}, which matching with {id}.
        :param id: Id of record to update.
        :param setFields: fields to update. Format {name: update-value}
        :return: None
        '''

        updateQuery = self.__parse_update_query(setFields=setFields, where={"id": id})
        self.__queries.append(updateQuery)

    def insert_object(self, fields: dict):
        '''
        Insert new object's data {fields} into database.
        :param fields: fields to insert. Format {name: value}
        :return: None
        '''

        insertQuery = self.__parse_insert_query(fields=fields)
        self.__queries.append(insertQuery)

    def delete_object(self, where: dict):
        '''
        Delete object matching with condition {where}.
        :param where: condition to query. Format {name: value} or {name: {value1, ...}}
        :return: True/False
        '''

        deleteQuery = self.__parse_delete_query(where=where)
        self.__queries.append(deleteQuery)

    def delete_object_by_id(self, id):
        '''
        Delete object matching with {id}.
        :param id: Id of record to delete.
        :return: True/False
        '''

        deleteQuery = self.__parse_delete_query(where={"id": id})
        self.__queries.append(deleteQuery)

    # Parsers

    def __parse_select_query(self, where={}, page=0, limit=20, orderBy={}):
        # Check data before parsing
        if None in (where, page, limit, orderBy):
            raise ValueError("'None' input is not accepted.")

        # Parse `orderBy` data
        orderClauses = []
        for key, value in orderBy.items():
            if isinstance(key, str) == False:
                raise ValueError("Column '{}' must be a string.".format(key))
            if value not in {"ASC", "DESC"}:
                raise ValueError("Value of column '{}' must be 'ASC' or 'DESC'.".format(key))
            orderClauses.append("`{k}` {v}".format(k=key, v=value))

        # Create SELECT query
        selectQuery = self.__selectQuery.format(table=self.__tableName)
        # Attach WHERE query
        whereContent = self.__parse_where_content(where)
        if len(whereContent) > 0:
            selectQuery += " WHERE {}".format(whereContent)
        # Attach ORDER query
        if len(orderClauses) > 0:
            selectQuery += " ORDER BY {}".format(", ".join(orderClauses))
        # Attach LIMIT & OFFSET query
        selectQuery += " LIMIT {l} OFFSET {o}".format(l=limit, o=page*limit)

        return selectQuery

    def __parse_update_query(self, setFields: dict, where: dict):
        # Check data before parsing
        if None in (where, setFields):
            raise ValueError("'None' input is not accepted.")
        if  len(where) == 0:
            raise ValueError("Update query has empty `where`.")

        # Parse `setFields` data
        setClauses = []
        for key, value in setFields.items():
            if isinstance(key, str) == False:
                raise ValueError("Column '{}' must be a string.".format(key))
            if isinstance(value, dict) or isinstance(value, list) or isinstance(value, set):
                raise ValueError("Value of column '{}' must be a string/number.".format(key))
            setClauses.append("`{k}` = '{v}'".format(k=key, v=value))

        # Create UPDATE query
        setContent = " , ".join(setClauses)
        whereContent = self.__parse_where_content(where)
        updateQuery = self.__updateQuery.format(table=self.__tableName, setData=setContent, condition=whereContent)

        return updateQuery

    def __parse_insert_query(self, fields: dict):
        # Check data before parsing
        if fields is None or len(fields) == 0:
            raise ValueError("'None' input is not accepted.")

        for key, value in fields.items():
            if isinstance(key, str) == False:
                raise ValueError("Column '{}' must be a string.".format(key))
            if isinstance(value, dict) or isinstance(value, list) or isinstance(value, set):
                raise ValueError("Value of column '{}' must be a string/number.".format(key))

        # Parse `intoFields` data
        columnsClauses = ["`{}`".format(k) for k in fields.keys()]
        valueClauses = ["'{}'".format(v) for v in fields.values()]

        # Create INSERT query
        columnContent = " , ".join(columnsClauses)
        valueContent = " , ".join(valueClauses)
        insertQuery = self.__insertQuery.format(table=self.__tableName, columns=columnContent, values=valueContent)

        return insertQuery

    def __parse_delete_query(self, where: dict):
        # Check data before parsing
        if where is None:
            raise ValueError("'None' input is not accepted.")
        if  len(where) == 0:
            raise ValueError("Delete query has empty `where`.")

        whereContent = self.__parse_where_content(where)
        deleteQuery = self.__deleteQuery.format(table=self.__tableName, condition=whereContent)

        return deleteQuery

    def __parse_where_content(self, where: dict):
        # Parse `where` data
        whereContent = ""
        whereClauses = []
        for key, value in where.items():
            if isinstance(key, str) == False:
                raise ValueError("Column '{}' must be a string.".format(key))
            if isinstance(value, dict):
                raise ValueError("Value of column '{}' must be a string/number/list/set.".format(key))
            if isinstance(value, list) or isinstance(value, set):
                value = ', '.join(["'{}'".format(x) for x in value])
            else:
                value = "'{}'".format(value)
            whereClauses.append("`{k}` IN ({v})".format(k=key, v=value))

        whereContent = " AND ".join(whereClauses)
        return whereContent