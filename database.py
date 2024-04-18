import sqlite3


def quote_join(list_of_str: list[str], enquote: bool = False) -> str:
    """
    takes in a list of str
    e.g. ['hello', 'bye']
    if enquote == False, returns 'hello, bye'
    if enquote == True, returns '"hello", "bye"'
    """
    if enquote:
        return ", ".join([f'"{str_}"' for str_ in list_of_str])

    return ", ".join(list_of_str)


class Table:
    """parent class for all subsequent tables"""
    table_name: str
    pk_name: str  #stands for primary key name
    fields: list[str]

    # def __init__(self, get_conn):
    #     self.get_conn = get_conn

    def __init__(self, database_name: str):
        """create a table upon initialisation of the class"""
        self.database_name = database_name

    def _valid_field_else_error(self, field) -> None:
        """checks if given fields are found in the table"""
        if field not in self.fields:
            raise AttributeError(f"Invalid field '{field}'")

    def insert(self, record: dict) -> None:
        """
        inserts the record into the junction table

        Checks for redundancies should already be done
        i.e. if pk == 5 already exists in the table,
        dont insert another record with pk == 5

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
            fieldstr = quote_join(self.fields, enquote=True)
            qnmarks = quote_join(["?"] * len(self.fields))
            query = f"""
                    INSERT INTO {self.table_name} ({fieldstr}) VALUES ({qnmarks});
                    """
            # formatting the params
            params = (record[self.fields[0]], )
            for field in self.fields[1:]:
                params += (record[field], )
            cursor.execute(query, params)
            conn.commit()
            #conn.close() called automatically

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
            params = (pk, )
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
            params = (pk, )
            cursor.execute(query, params)
            conn.commit()


class JunctionTable(Table):
    pk1_name: str
    pk2_name: str
    fields: list[str]

    def insert(self, record: dict) -> None:
        """
        inserts the record into the junction table
        
        Checks for redundancies should already be done
        i.e. insert({"student_id": 5. "activity_id": 3})
        should not be called if {"student_id": 5. "activity_id": 3} 
        already exists in the database, do the check beforehand.

        record argument that is passed should have:
        keys of type str referring to the fields
        values of the correct type referring to the values to be put in the cells
        """
        if sorted(record) != sorted(self.fields):
            raise AttributeError("Wrong record format, wrong fields")
        # # check that all fields in record is valid
        # for field in record:
        #     self._valid_field_else_error(field)
        # # check that record has all fields required
        # for field in self.fields:
        #     if field not in record:
        #         raise AttributeError(f"field {field} not in record argument")
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            # formatting the query
            fieldstr = quote_join(self.fields, enquote=True)
            qnmarks = quote_join(["?"] * len(self.fields))
            query = f"""
                    INSERT INTO {self.table_name} ({fieldstr}) VALUES ({qnmarks});
                    """
            # formatting the params
            params = (record[self.fields[0]], )
            for field in self.fields[1:]:
                params += (record[field], )
            cursor.execute(query, params)
            conn.commit()
<<<<<<< HEAD
            #conn.close() called automatically

    def delete(self, pk1_value, pk2_value):
        """remove existing records in the database"""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    DELETE FROM {self.table_name}
                    WHERE {self.pk1_name} = ?
                    AND
                    {self.pk2_name} = ?;
                    """
            param = (pk1_value, pk2_value)
            cursor.execute(query, param)
            conn.commit()
=======
>>>>>>> b7789a2 (studentcca refactoring, commenting out code to rely on parent class junctiontable)

    def retrieve_all(self, pk_name: str, pk: int) -> list[tuple]:
        """
        find existing records in the database
        pk_name can only be "student_id" or "cca_id"
        retrieves all data regarding the student or cca

        e.g. using a StudentCCA object:
        .retrieve_all("cca_id", 3)
        returns
        [(5, 3, "member"), (7. 3, "president"), (10, 3, "member")]
        """
        self._valid_field_else_error(pk_name)
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    SELECT *
                    FROM {self.database_name}
                    WHERE {pk_name} = ?;
                    """
            params = (pk, )
            cursor.execute(query, params)
            record = cursor.fetchall()
            conn.commit()
            #conn.close() is called automatically
        return record

<<<<<<< HEAD
=======
    def delete(self, pk1_value: int, pk2_value: int) -> None:
        """remove existing records in the database using composite primary keys """
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    DELETE FROM {self.table_name}
                    WHERE {self.pk1_name} = ?
                    AND
                    {self.pk2_name} = ?;
                    """
            param = (pk1_value, pk2_value)
            cursor.execute(query, param)
            conn.commit()
>>>>>>> b7789a2 (studentcca refactoring, commenting out code to rely on parent class junctiontable)

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
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                "account_id" INTEGER PRIMARY KEY,
                "username" TEXT NOT NULL UNIQUE,
                "password" TEXT NOT NULL,
                "salt" BYTES NOT NULL
                );
                """)
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

    def update(self, pk_name: str, pk, field: str, new):
        """
        update existing records in the database
        field can only be "username", "password" or "salt"
        pk_name can only be "account_id" or "username"
        raises Attributes error if field is invalid
        checks for repeated username should already be done if username is being updated
        """
        self._valid_field_else_error(field)
        if pk_name not in ['account_id', 'username']:
            raise AttributeError(f"Invalid pk_name '{pk_name}'")

        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    UPDATE {self.table_name} 
                    SET {field} = ? 
                    WHERE {pk_name} = ? 
                    """
            params = (new, pk)
            cursor.execute(query, params)
            conn.commit()
            #conn.close() called automatically

    def retrieve(self, pk_name: str, pk) -> tuple:
        """
        find existing records in the database
        pk_name can only be "account_id" or "username"
        raises Attributes error if field is invalid
        """
        if pk_name not in ['account_id', 'username']:
            raise AttributeError(f"Invalid pk_name '{pk_name}'")

        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    SELECT *
                    FROM {self.table_name}
                    WHERE {pk_name} = ?;
                    """
            params = (pk, )
            cursor.execute(query, params)
            record = cursor.fetchone()
            conn.commit()
            #conn.close() called automatically
            return record

    def delete(self, pk_name: str, pk):
        """
        remove existing records in the database
        pk_name can only be "account_id" or "username"
        raises Attributes error if field is invalid
        """
        if pk_name not in ['account_id', 'username']:
            raise AttributeError(f"Invalid pk_name '{pk_name}'")

        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    DELETE FROM {self.table_name}
                    WHERE {pk_name} = ?;
                    """
            param = (pk, )
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
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    {self.pk_name} INTEGER PRIMARY KEY,
                    "name" TEXT NOT NULL,
                    "class" INTEGER NOT NULL, 
                    "email" TEXT NOT NULL,
                    "account_id" INTEGER NOT NULL UNIQUE,
                    FOREIGN KEY ("account_id") REFERENCES account("account_id")
                );
                """)
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
        self._valid_field_else_error(field)
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
            params = (student_id, )
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
            param = (student_id, )
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
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    {self.pk_name} INTEGER PRIMARY KEY,
                    "name" TEXT NOT NULL,
                    "type" TEXT NOT NULL, 
                );
                """)
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
            params = (cca_id, )
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
            params = (cca_id, )
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
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    {self.pk_name} INTEGER PRIMARY KEY,
                    "name" TEXT NOT NULL,
                    "date" TEXT NOT NULL, 
                    "location" TEXT NOT NULL,
                    FOREIGN KEY ("organiser_id") REFERENCES account("student_id")
                );
                """)
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
            params = (activity_id, )
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
            params = (account_id, )
            cursor.execute(query, params)
            conn.commit()


class StudentActivity(JunctionTable):

    table_name: str = "studentactivity"
    pk1_name: str = "student_id"
    pk2_name: str = "activity_id"
    fields = ["student_id", "activity_id"]

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
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    {self.pk1_name} INTEGER,
                    {self.pk2_name} INTEGER,
                    PRIMARY KEY ({self.pk1_name}, {self.pk2_name}),
                    FOREIGN KEY ({self.pk1_name}) REFERENCES student("student_id"),
                    FOREIGN KEY ({self.pk2_name}) REFERENCES activity("activity_id")
                );
                """)
            conn.commit()
            #conn.close() called automatically

    def insert(self, student_id: int, activity_id: int):
        """insert new records into the database"""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                INSERT INTO {self.table_name} ({self.pk1_name}, {self.pk2_name}) VALUES (?,?);
            """
            params = (student_id, activity_id)
            cursor.execute(query, params)
            conn.commit()
            #conn.close() is called automatically

    def retrieve(self, pk_name: str, pk: int):
        """
        find existing records in the database
        pk_name can only be "student_id" or "activity_id"
        retrieves all data regarding the student or activity
        """
        self._valid_field_else_error(pk_name)
        with sqlite3.connect(self.table_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    SELECT *
                    FROM {self.table_name}
                    WHERE {pk_name} = ?;
                    """
            params = (pk, )
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
                    DELETE FROM {self.table_name}
                    WHERE {self.pk1_name} = ? AND {self.pk2_name} = ?;
                    """
            param = (student_id, activity_id)
            cursor.execute(query, param)
            conn.commit()


class StudentCCA(JunctionTable):

    table_name: str = "studentcca"
    pk1_name: str = "student_id"
    pk2_name: str = "cca_id"
    fields = ["student_id", "cca_id", "role"]

    def __init__(self, database_name):
        """
        create a table upon initialisation of the class
        (cca_id, student_id) for pk
        """
        self.database_name = database_name
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    {self.pk1_name} INTEGER,
                    {self.pk2_name} INTEGER,
                    "role" TEXT NOT NULL,
                    PRIMARY KEY ({self.pk1_name}, {self.pk2_name}),
                    FOREIGN KEY ({self.pk1_name}) REFERENCES student("student_id"),
                    FOREIGN KEY ({self.pk2_name}) REFERENCES cca("cca_id")
                );
                """)
            conn.commit()
<<<<<<< HEAD
            #conn.close() called automatically

    def insert(self, student_id: int, cca_id: int, role: str):
        """insert new records into the database"""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                INSERT INTO {self.table_name} ({self.pk1_name}, {self.pk2_name}, "role") VALUES (?,?,?);
            """
            params = (student_id, cca_id, role)
            cursor.execute(query, params)
            conn.commit()
            #conn.close() is called automatically
=======
    
    # def insert(self, student_id: int, cca_id: int, role: str):
    #     """insert new records into the database"""
    #     with sqlite3.connect(self.database_name) as conn:
    #         cursor = conn.cursor()
    #         query = f"""
    #             INSERT INTO {self.table_name} ({self.pk1_name}, {self.pk2_name}, "role") VALUES (?, ?, ?);
    #         """
    #         params = (student_id, cca_id, role)
    #         cursor.execute(query, params)
    #         conn.commit()
>>>>>>> b7789a2 (studentcca refactoring, commenting out code to rely on parent class junctiontable)

    def update(self, student_id: int, cca_id: int, new: str):
        """
        update existing records in the database
        only role could be updated
        To "update" student_id or cca_id, instead use .remove() and .insert()
        """
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    UPDATE {self.table_name} 
                    SET "role" = ? 
                    WHERE {self.pk1_name} = ? AND {self.pk2_name};
                    """
            params = (new, student_id, cca_id)
            cursor.execute(query, params)
            conn.commit()

<<<<<<< HEAD
    def retrieve(self, pk_name: int, pk: int):
        """
        find existing records in the database
        pk_name can only be "student_id" or "cca_id"
        retrieves all data regarding the student or cca
        """
        self._valid_field_else_error(pk_name)
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    SELECT *
                    FROM {self.table_name}
                    WHERE {pk_name} = ?;
                    """
            params = (pk, )
            cursor.execute(query, params)
            record = cursor.fetchall()
            conn.commit()
            #conn.close() is called automatically
        return record

    def delete(self, student_id: int, cca_id: int):
        """remove existing records in the database"""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    DELETE FROM {self.table_name}
                    WHERE {self.pk1_name} = ? AND {self.pk2_name} = ?;        
                    """
            params = (student_id, cca_id)
            cursor.execute(query, params)
            conn.commit()
=======
    # def retrieve_all(self, pk_name: str, pk: int) -> list[tuple]:
    #     """
    #     find existing records in the database
    #     pk_name can only be "student_id" or "cca_id"
    #     retrieves all data regarding the student or cca
    #     """
    #     self._valid_field_else_error(pk_name)
    #     with sqlite3.connect(self.database_name) as conn:
    #         cursor = conn.cursor()
    #         query = f"""
    #                 SELECT *
    #                 FROM {self.table_name}
    #                 WHERE {pk_name} = ?;
    #                 """
    #         params = (pk,)
    #         cursor.execute(query, params)
    #         record = cursor.fetchall()
    #         conn.commit()
    #     return record

    # def delete(self, student_id: int, cca_id: int):
    #     """remove existing records in the database"""
    #     with sqlite3.connect(self.database_name) as conn:
    #         cursor = conn.cursor()
    #         query = f"""
    #                 DELETE FROM {self.table_name}
    #                 WHERE {self.pk1_name} = ? AND {self.pk2_name} = ?;      
    #                 """
    #         params = (student_id, cca_id)
    #         cursor.execute(query, params)
    #         conn.commit()
>>>>>>> b7789a2 (studentcca refactoring, commenting out code to rely on parent class junctiontable)
