import sqlite3


def quote_join(list_of_str: list[str], enquote: bool = False) -> str:
    """
    takes in a list of str
    e.g. ['hello', 'bye']
    if enquote == False, returns 'hello, bye'
    if enquote == True, returns '"hello", "bye"'
    
    
    """
    if enquote:
        return ", ".join([f'"{str_}"' for str_ in list_of_str])_
    else:
        return ", ".join(list_of_str)

class Table:
    """parent class for all subsequent tables"""
    table_name: str
    pk_name: str    #stands for primary key name
    fields = []

    def __init__(self, database_name: str):
        """create a table upon initialisation of the class"""
        self.database_name = database_name

    def _valid_field_else_error(self, field) -> None:
        """checks if given fields are found in the table"""
        if field not in self.fields:
            raise AttributeError(f"Invalid field '{field}'")
    
    def insert(self):
        """insert new records into the database"""
        raise NotImplementedError

    def update(self, pk: int, field: str, new: str):
        """update existing records in the database"""
        self._valid_field_else_error(field)
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()            
            query = f"""
                    UPDATE {self.table_name} 
                    SET {field} = ? 
                    WHERE {self.pk_name} = ? 
                    """
            params = (new, pk)
            cursor.execute(query, params)
            conn.commit()
            #conn.close() called automatically
        
    def retrieve(self, pk: int):
        """find existing records in the database"""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    SELECT *
                    FROM {self.table_name}
                    WHERE {self.pk_name} = ?;
                    """
            params = (pk,)
            cursor.execute(query, params)
            record = cursor.fetchone()
            conn.commit()
            return record

    def delete(self, pk: int):
        """remove existing records in the database"""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    DELETE FROM {self.table_name}
                    WHERE {self.pk_name} = ?;
                    """
            params = (pk,)
            cursor.execute(query, params)
            conn.commit()

class JunctionTable(Table):
    pk1_name: str
    pk2_name: str
    fields: list[str]

    def __init__(self):
        # self.database_name
        return
        
        

    def insert(self, record: dict):
        """
        inserts the record into the junction table
        
        Checks for redundancies should already be done
        i.e. insert({"student_id": 5. "cca_id": 3})
        should not be called if {"student_id": 5. "cca_id": 3} 
        already exists in the database, do the check beforehand.

        record argument that is passed should have:
        keys of type str referring to the fields
        values of type str referring to the values to be put in the cells

        """
        # check that all fields in record is valid
        for field in record:
            self._valid_field_else_error(field)
        # check that record has all fields required
        for field in self.fields:
            if field not in record:
                raise AttributeError(f"field {field} not in record argument")
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            # formatting the query
            fieldstr = quote_join(self.fields, enquote = True)
            qnmarks = quote_join(["?"] * len(self.fields))
            query = f"""
                    INSERT INTO {self.table_name} ({fieldstr}) VALUES ({qnmarks});
                    """
            params = tuple(record.values())
            cursor.execute(query, params)
            conn.commit()
            #conn.close() called automatically        
        
    def retrieve(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    
        

class Account(Table):
    table_name: str = "account"
    fields = ["account_id", "username", "password", "salt"]

    def __init__(self, database_name: str):
        """
        create a table upon initialisation of the class
        account id for primary key
        """
        self.database_name = database_name
        with sqlite3.connect(database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                "account_id" INTEGER PRIMARY KEY,
                "username" TEXT NOT NULL UNIQUE,
                "password" TEXT NOT NULL,
                "salt" BYTES NOT NULL
                );
                """
            )
            conn.commit()
            #conn.close() called automatically

    def insert(self, username: str, password: str, salt: bytes):
        """
        insert new records into the database
        checks for repeated username should already be done
        """
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    INSERT INTO {self.table_name} ("username", "password", "salt") VALUES (?, ?, ?);
                    """
            params = (username, password, salt)
            cursor.execute(query, params)
            conn.commit()
            #conn.close() called automatically
        
    def update(self, account_id: int, field: str, new):
        """
        update existing records in the database
        field can only be "username", "password" or "salt"
        raises Attributes error if field is invalid
        checks for repeated username should already be done if username is being updated
        """
        self._valid_field_else_error(field)            
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()            
            query = f"""
                    UPDATE {self.table_name} 
                    SET {field} = ? 
                    WHERE "account_id" = ? 
                    """
            params = (new, account_id)
            cursor.execute(query, params)
            conn.commit()
            #conn.close() called automatically

    def retrieve(self, field: str, data) -> tuple:
        """
        find existing records in the database
        field can only be "account_id" or "username"
        raises Attributes error if field is invalid
        """
        if field not in ['account_id', 'username']:
            raise AttributeError(f"Invalid field '{field}'")
        
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    SELECT *
                    FROM {self.table_name}
                    WHERE {field} = ?;
                    """
            params = (data,)
            cursor.execute(query, params)
            record = cursor.fetchone()
            conn.commit()
            #conn.close() called automatically
            return record

    def delete(self, field: str, data):
        """
        remove existing records in the database
        field can only be "account_id" or "username"
        raises Attributes error if field is invalid
        """
        if field not in ['account_id', 'username']:
            raise AttributeError(f"Invalid field '{field}'")
            
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    DELETE FROM {self.table_name}
                    WHERE {field} = ?;
                    """
            param = (data,)
            cursor.execute(query, param)
            conn.commit()
            #conn.close() called automatically

class Student(Table):
    table_name: str = "student"
    pk_name: str = "student_id"
    fields = ["student_id", "name", "class", "email", "account_id"]

    def __init__(self, database_name):
        """
        create a table upon initialisation of the class
        student_id for pk
        yu xi
        """
        self.database_name = database_name
        with sqlite3.connect(database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    {self.pk_name} INTEGER PRIMARY KEY,
                    "name" TEXT NOT NULL,
                    "class" INTEGER NOT NULL, 
                    "email" TEXT NOT NULL,
                    "account_id" INTEGER NOT NULL UNIQUE,
                    FOREIGN KEY ("account_id") REFERENCES account("account_id")
                );
                """
            )
            conn.commit()
            #conn.close() called automatically

    def insert(self, name: str, _class: int, email: str, account_id: int):
        """
        insert new records into the database
        checks for valid account_id should already be done
        yu xi
        """
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                INSERT INTO {self.table_name}("name", "class", "email", "account_id") 
                VALUES (?, ?, ?, ?);
            """
            params = (name, _class, email, account_id)
            cursor.execute(query, params)
            conn.commit()
            #conn.close() called automatically

    def update(self, student_id: int, field: str, new):
        """
        update existing records in the database
        field can only be "account_id", "name", "class" or "email"
        checks for valid account_id should already be done
        raises Attributes error if field is invalid
        """

        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    UPDATE {self.table_name} 
                    SET {field} = ? 
                    WHERE "student_id" = ? 
                    """
            params = (new, student_id)
            cursor.execute(query, params)
            conn.commit()
            #conn.close() called automatically

    def retrieve(self, student_id: int):
        """
        find existing records in the database
        xinyu
        """
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    SELECT *
                    FROM "student"
                    WHERE {self.pk_name} == ?;
                    """
            params = (student_id,)
            cursor.execute(query, params)
            record = cursor.fetchone()
            conn.commit()
            #conn.close() called automatically
            return record         

    def delete(self, student_id: int):
        """remove existing records in the database"""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    DELETE FROM {self.table_name}
                    WHERE {self.pk_name} = ?;
                    """
            param = (student_id,)
            cursor.execute(query, param)
            conn.commit()

class CCA(Table):
    table_name: str = "cca"
    pk_name: str = "cca_id"
    fields = ["cca_id", "name", "type"]
    
    def __init__(self, database_name):
        """
        create a table upon initialisation of the class
        cca_id for pk
        jae zen
        """
        self.database_name = database_name
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    {self.pk_name} INTEGER PRIMARY KEY,
                    "name" TEXT NOT NULL,
                    "type" TEXT NOT NULL, 
                );
                """
            )
            conn.commit()
            #conn.close() called automatically


    def insert(self, name: str, type: str):
        """
        insert new records into the database
        yu xi
        """
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                INSERT INTO {self.table_name} ("name", "type") VALUES (?, ?);
            """
            params = (name, type)
            cursor.execute(query, params)
            conn.commit()
            # conn.close() is called automatically
    
    def update(self, cca_id: int, field: str, new: str):
        """
        update existing records in the database
        field can only be "name" or "type"
        raises Attributes error if field is invalid
        yu xi
        """
        self._valid_field_else_error(field)
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                UPDATE {self.table_name}
                SET {field} = ?
                WHERE {self.pk_name} = ? ;                
            """
            params = (new, cca_id)
            cursor.execute(query, params)
            conn.commit()
            # conn.close() is called automatically

    def retrieve(self, cca_id: int):
        """
        find existing records in the database
        yu xi
        """
        with sqlite3.connect('meow.db') as conn:
            cursor = conn.cursor()
            query = f"""
                SELECT *
                FROM {self.table_name} ;
                WHERE {self.pk_name} = ? ;
            """
            params = (cca_id,)
            cursor.execute(query, params)
            conn.commit()
            # conn.close() is called automatically

    def delete(self, cca_id: int):
        """remove existing records in the database"""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    DELETE FROM {self.table_name}
                    WHERE {self.pk_name} = ?;
                    """
            params = (cca_id,)
            cursor.execute(query, params)
            conn.commit()

class Activity(Table):
    table_name: str = "activity"
    pk_name = "activity_id"
    fields = ["activity_id", "name", "date", "location", "organiser_id"]

    def __init__(self, database_name):
        """
        create a table upon initialisation of the class
        activity_id for pk
        jae zen
        """
        self.database_name = database_name
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    {self.pk_name} INTEGER PRIMARY KEY,
                    "name" TEXT NOT NULL,
                    "date" TEXT NOT NULL, 
                    "location" TEXT NOT NULL,
                    FOREIGN KEY ("organiser_id") REFERENCES account("student_id")
                );
                """
            )
            conn.commit()
            #conn.close() called automatically

    def insert(self, name: str, date: str, location: str, organiser_id: int):
        """
        insert new records into the database
        checks for repeated organiser_id should already be done
        """
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()            
            query = f"""
                INSERT INTO {self.table_name} ("name", "date", "location", "organiser_id")
                VALUES( ?, ?, ?, ? );
                """
            params = (name, date, location, organiser_id)
            cursor.execute(query, params)
            conn.commit()
            #conn.close() called automatically

    def update(self, activity_id: int, field: str, new: str):
        """
        update existing records in the database
        field can only be "organiser_id" "name" "date" or "location"
        checks for valid organiser_id should already be done
        raises Attributes error if field is invalid
        xinyu
        """
        self._valid_field_else_error(field)
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                UPDATE {self.table_name}
                SET {field} = ?
                WHERE {self.pk_name} = ?;
                """
            params = (new, activity_id)
            cursor.execute(query, params)
            conn.commit()
            #conn.close() called automatically

    def retrieve(self, activity_id: int):
        """
        find existing records in the database
        xinyu
        """
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                SELECT *
                FROM {self.table_name}
                WHERE {self.pk_name} = ?;
                """
            params = (activity_id,)
            cursor.execute(query, params)
            record = cursor.fetchone()
            conn.commit()
            #conn.close() called automatically
            return record

    def delete(self, account_id: int):
        """
        remove existing records in the database
        STANLEY DID THIS THANK ME
        """
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    DELETE FROM {self.table_name}
                    WHERE {self.pk_name} = ?;
                    """
            params = (account_id,)
            cursor.execute(query, params)
            conn.commit()

class StudentActivity:

    table_name: str = "studentactivity"
    pk1_name: str = "student_id"
    pk2_name: str = "activity_id"
    fields = ["activity_id", "student_id"]
    
    def __init__(self, database_name):
        """
        create a table upon initialisation of the class
        (student_id, activity_id) for pk

        This class has no .update() method.
        To "update", instead use .remove() and .insert()
        """
        self.database_name = database_name
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    {self.pk1_name} INTEGER PRIMARY KEY,
                    {self.pk2_name} INTEGER PRIMARY KEY
                );
                """
            )
            conn.commit()
            #conn.close() called automatically

    def insert(self, student_id: int, activity_id: int):
        """insert new records into the database"""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                INSERT INTO {self.database_name} ({self.pk1_name}, {self.pk2_name}) VALUES (?,?);
            """
            params = (activity_id, student_id)
            cursor.execute(query, params)
            conn.commit()
            #conn.close() is called automatically

    def retrieve(self, student_id: int, activity_id: int):
        """find existing records in the database"""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                SELECT *
                FROM {self.database_name}
                WHERE {self.pk1_name} = ? AND 
                      {self.pk2_name} = ?;
            """
            params = (student_id, activity_id)
            cursor.execute(query, params)
            record = cursor.fetchall()
            conn.commit()
            #conn.close() is called automatically
        return record

    def delete(self, student_id: int, activity_id: int):
        """remove existing records in the database"""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    DELETE FROM {self.database_name}
                    WHERE {self.pk1_name} = ? AND
                          {self.pk2_name} = ?;
                    """
            param = (student_id, activity_id)
            cursor.execute(query, param)
            conn.commit()

class StudentCCA:

    table_name: str = "studentcca"
    pk1_name: str = "cca_id"
    pk2_name: str = "student_id"
    fields = ["cca_id", "student_id", "role"]
    
    def __init__(self, database_name):
        """
        create a table upon initialisation of the class
        (student_id, activity_id) for pk
    
        This class has no .update() method.
        To "update", instead use .remove() and .insert()
        """
        self.database_name = database_name
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    {self.pk1_name} INTEGER PRIMARY KEY,
                    {self.pk2_name} INTEGER PRIMARY KEY,
                    "role" TEXT
                );
                """
            )
            conn.commit()
            #conn.close() called automatically
    
        def insert(self, cca_id: int, student_id: int, role: str):
            """insert new records into the database"""
            with sqlite3.connect(self.database_name) as conn:
                cursor = conn.cursor()
                query = f"""
                    INSERT INTO {self.database_name} ({self.pk1_name}, {self.pk2_name}, "role") VALUES (?,?,?);
                """
                params = (activity_id, student_id, role)
                cursor.execute(query, params)
                conn.commit()
                #conn.close() is called automatically

        def retrieve(self, cca_id: int, student_id: int, role: str):
            """find existing records in the database"""
            with sqlite3.connect(self.database_name) as conn:
                cursor = conn.cursor()
                query = f"""
                    SELECT *
                    FROM {self.database_name}
                    WHERE {self.pk1_name} = ? AND 
                          {self.pk2_name} = ?;
                """
                params = (student_id, activity_id)
                cursor.execute(query, params)
                record = cursor.fetchall()
                conn.commit()
                #conn.close() is called automatically
            return record

        def delete(self, cca_id: int, student_id: int):
            """remove existing records in the database"""
            with sqlite3.connect(self.database_name) as conn:
                cursor = conn.cursor()
                query = f"""
                        DELETE FROM {self.database_name}
                        WHERE {self.pk1_name} = ? AND
                              {self.pk2_name} = ?;        
                        """
                param = (student_id, activity_id, role)
                cursor.execute(query, param)
                conn.commit()