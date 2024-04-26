import sqlite3
from typing import Callable

def init_tables(conn):
    """creates the table for all table in database"""
    
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "account" (
        "account_id" INTEGER PRIMARY KEY,
        "username" TEXT NOT NULL UNIQUE,
        "password" TEXT NOT NULL,
        "salt" BYTES NOT NULL
        );
        """
        )
    conn.commit()
    #conn.close() called automatically

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "student" (
            "student_id" INTEGER PRIMARY KEY,
            "name" TEXT NOT NULL,
            "class" INTEGER NOT NULL, 
            "email" TEXT NOT NULL,
            "account_id" INTEGER NOT NULL UNIQUE,
            FOREIGN KEY ("account_id") REFERENCES account("account_id")
        );
        """
    )
    conn.commit()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "cca" (
            "cca_id" INTEGER PRIMARY KEY,
            "name" TEXT NOT NULL,
            "type" TEXT NOT NULL 
        );
        """
    )
    conn.commit()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "activity" (
            "activity_id" INTEGER PRIMARY KEY,
            "name" TEXT NOT NULL,
            "date" TEXT NOT NULL, 
            "location" TEXT NOT NULL,
            "organiser_id" INTEGER,
            FOREIGN KEY ("organiser_id") REFERENCES account("student_id")
        );
        """
    )
    conn.commit()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "studentactivity" (
            "student_id" INTEGER NOT NULL,
            "activity_id" INTEGER NOT NULL,
            PRIMARY KEY ("student_id", "activity_id"),
            FOREIGN KEY ("student_id") REFERENCES student("student_id"),
            FOREIGN KEY ("activity_id") REFERENCES activity("activity_id")
        );
        """
    )
    conn.commit()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "studentcca" (
            "student_id" INTEGER,
            "cca_id" INTEGER,
            "role" TEXT NOT NULL,
            PRIMARY KEY ("student_id", "cca_id"),
            FOREIGN KEY ("student_id") REFERENCES student("student_id"),
            FOREIGN KEY ("cca_id") REFERENCES cca("cca_id")
        );
        """
    )
    conn.commit()

def init_tables(conn):
    """creates the table for all table in database"""
    
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "account" (
        "account_id" INTEGER PRIMARY KEY,
        "username" TEXT NOT NULL UNIQUE,
        "password" TEXT NOT NULL,
        "salt" BYTES NOT NULL
        );
        """
        )
    conn.commit()
    #conn.close() called automatically

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "student" (
            "student_id" INTEGER PRIMARY KEY,
            "name" TEXT NOT NULL,
            "class" INTEGER NOT NULL, 
            "email" TEXT NOT NULL,
            "account_id" INTEGER NOT NULL UNIQUE,
            FOREIGN KEY ("account_id") REFERENCES account("account_id")
        );
        """
    )
    conn.commit()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "cca" (
            "cca_id" INTEGER PRIMARY KEY,
            "name" TEXT NOT NULL,
            "type" TEXT NOT NULL 
        );
        """
    )
    conn.commit()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "activity" (
            "activity_id" INTEGER PRIMARY KEY,
            "name" TEXT NOT NULL,
            "date" TEXT NOT NULL, 
            "location" TEXT NOT NULL,
            "organiser_id" INTEGER,
            FOREIGN KEY ("organiser_id") REFERENCES account("student_id")
        );
        """
    )
    conn.commit()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "studentactivity" (
            "student_id" INTEGER NOT NULL,
            "activity_id" INTEGER NOT NULL,
            PRIMARY KEY ("student_id", "activity_id"),
            FOREIGN KEY ("student_id") REFERENCES student("student_id"),
            FOREIGN KEY ("activity_id") REFERENCES activity("activity_id")
        );
        """
    )
    conn.commit()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "studentcca" (
            "student_id" INTEGER,
            "cca_id" INTEGER,
            "role" TEXT NOT NULL,
            PRIMARY KEY ("student_id", "cca_id"),
            FOREIGN KEY ("student_id") REFERENCES student("student_id"),
            FOREIGN KEY ("cca_id") REFERENCES cca("cca_id")
        );
        """
    )
    conn.commit()

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
    get_conn: Callable
    pk_name: str  #stands for primary key name
    fields: list[str]

    # def __init__(self, get_conn):
    #     self.get_conn = get_conn

    def __init__(self, get_conn: Callable):
        """create a table upon initialisation of the class"""
        self.get_conn = get_conn

    def _valid_field_else_error(self, field) -> None:
        """checks if given fields are found in the table"""
        if field not in self.fields:
            raise AttributeError(f"Invalid field '{field}'")

    def _execute_query(
        self,
        query: str, params: tuple | None,
        *,
        commit: bool = False,
        fetch: bool = False
    ):
        conn = self.get_conn()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        assert not (commit and fetch), "commit and fetch are both True"
        if fetch:
            record = cursor.fetchone()
            return record
        if commit:
            conn.commit()

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
        # formatting the query
        fieldstr = quote_join(list(record.keys()), enquote=True)
        qnmarks = quote_join(["?"] * len(record))
        query = f"""
                INSERT INTO {self.table_name} ({fieldstr}) VALUES ({qnmarks});
                """
        # formatting the params
        # params = (record[self.fields[0]], )
        # for field in self.fields[1:]:
        #     params += (record[field], )
        self._execute_query(query, tuple(record.values()), commit=True)
        
    def update(self, pk: int, field: str, new: str):
        """update existing records in the database"""
        self._valid_field_else_error(field)
        query = f"""
                UPDATE {self.table_name} 
                SET {field} = ? 
                WHERE {self.pk_name} = ? 
                """
        params = (new, pk)
        self._execute_query(query, params, commit=True)

    def retrieve(self, pk: int, pk_name: str = ""):
        """find existing records in the database"""
        if pk_name == "":
            pk_name = self.pk_name
        query = f"""
                SELECT *
                FROM {self.table_name}
                WHERE {pk_name} = ?;
                """
        params = (pk,)
        record = self._execute_query(query, params, fetch=True)
        return record

    def delete(self, pk: int):
        """remove existing records in the database"""
        query = f"""
                DELETE FROM {self.table_name}
                WHERE {self.pk_name} = ?;
                """
        params = (pk, )
        self._execute_query(query, params, commit=True)


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
            #conn.close() called automatically

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



class Account(Table):
    table_name: str = "account"
    fields = ["account_id", "username", "password", "salt"]

    def __init__(self, get_conn: Callable):
        """
        create a table upon initialisation of the class
        account id for primary key
        """
        super().__init__(get_conn)
        self._execute_query(f"""
           CREATE TABLE IF NOT EXISTS {self.table_name} (
           "account_id" INTEGER PRIMARY KEY,
           "username" TEXT NOT NULL UNIQUE,
           "password" TEXT NOT NULL,
           "salt" BYTES NOT NULL
           );
        """, params=None, commit=True)

    # def insert(self, username: str, password: str, salt: bytes):
    #     """
    #     insert new records into the database
    #     checks for repeated username should already be done
    #     """
    #     with sqlite3.connect(self.database_name) as conn:
    #         cursor = conn.cursor()
    #         query = f"""
    #                 INSERT INTO {self.table_name} ("username", "password", "salt") VALUES (?, ?, ?);
    #                 """
    #         params = (username, password, salt)
    #         cursor.execute(query, params)
    #         conn.commit()
    #         #conn.close() called automatically

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

    def retrieve(self, pk: int, pk_name: str) -> tuple:
        """
        find existing records in the database
        pk_name can only be "account_id" or "username"
        raises Attributes error if field is invalid
        """
        if pk_name not in ['account_id', 'username']:
            raise AttributeError(f"Invalid pk_name '{pk_name}'")
        record = self._execute_query(f"""
            SELECT *
            FROM {self.table_name}
            WHERE {pk_name} = ?;
            """,
            params=(pk,),
            fetch=True
        )
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


class Student(Table):
    table_name: str = "student"
    pk_name: str = "student_id"
    fields = ["student_id", "name", "class", "email", "account_id"]

    def __init__(self, get_conn: Callable):
        """
        create a table upon initialisation of the class
        student_id for pk
        """
        super().__init__(get_conn)
        self._execute_query(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                {self.pk_name} INTEGER PRIMARY KEY,
                "name" TEXT NOT NULL,
                "class" INTEGER NOT NULL, 
                "email" TEXT NOT NULL,
                "account_id" INTEGER NOT NULL UNIQUE,
                FOREIGN KEY ("account_id") REFERENCES account("account_id")
            );
        """, params=None, commit=True)

    def insert(self, record: dict):
        """
        insert new records into the database
        checks for valid account_id should already be done
        """
        # check that record has all fields required
        for field in self.fields:
            if field not in record:
                raise AttributeError(f"field {field} not in record argument")
        super().insert(record)
    #     with sqlite3.connect(self.database_name) as conn:
    #         cursor = conn.cursor()
    #         query = f"""
    #             INSERT INTO {self.table_name}("name", "class", "email", "account_id") 
    #             VALUES (?, ?, ?, ?);
    #         """
    #         params = (name, _class, email, account_id)
    #         cursor.execute(query, params)
    #         conn.commit()
    #         #conn.close() called automatically

    # def update(self, student_id: int, field: str, new):
    #     """
    #     update existing records in the database
    #     field can only be "account_id", "name", "class" or "email"
    #     checks for valid account_id should already be done
    #     raises Attributes error if field is invalid
    #     """
    #     self._valid_field_else_error(field)
    #     with sqlite3.connect(self.database_name) as conn:
    #         cursor = conn.cursor()
    #         query = f"""
    #                 UPDATE {self.table_name} 
    #                 SET {field} = ? 
    #                 WHERE "student_id" = ? 
    #                 """
    #         params = (new, student_id)
    #         cursor.execute(query, params)
    #         conn.commit()
    #         #conn.close() called automatically

    # def retrieve(self, student_id: int):
    #     """
    #     find existing records in the database
    #     """
    #     with sqlite3.connect(self.database_name) as conn:
    #         cursor = conn.cursor()
    #         query = f"""
    #                 SELECT *
    #                 FROM "student"
    #                 WHERE {self.pk_name} == ?;
    #                 """
    #         params = (student_id, )
    #         cursor.execute(query, params)
    #         record = cursor.fetchone()
    #         conn.commit()
    #         #conn.close() called automatically
    #         return record

    # def delete(self, student_id: int):
    #     """remove existing records in the database"""
    #     with sqlite3.connect(self.database_name) as conn:
    #         cursor = conn.cursor()
    #         query = f"""
    #                 DELETE FROM {self.table_name}
    #                 WHERE {self.pk_name} = ?;
    #                 """
    #         param = (student_id, )
    #         cursor.execute(query, param)
    #         conn.commit()



class CCA(Table):
    table_name: str = "cca"
    fields = ["cca_id", "name", "type"]

    def __init__(self, database_name):
        """
        create a table upon initialisation of the class
        cca_id for pk
        """
        self.database_name = database_name
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    "cca_id" INTEGER PRIMARY KEY,
                    "name" TEXT NOT NULL UNQIUE,
                    "type" TEXT NOT NULL, 
                );
                """)
            conn.commit()
            #conn.close() called automatically

    def insert(self, name: str, type: str):
        """
        insert new records into the database
        checks for repeated name should already be done
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

    def update(self, pk_name: str, pk, field: str, new: str):
        """
        update existing records in the database
        pk_name can only be "cca_id" or "name"
        field can only be "name" or "type"
        raises Attributes error if field is invalid
        checks for repeated name should already be done
        """
        self._valid_field_else_error(field)
        if pk_name not in ['cca_id', 'name']:
            raise AttributeError(f'Invalid pk_name {pk_name}')
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                UPDATE {self.table_name}
                SET {field} = ?
                WHERE {pk_name} = ?;
            """
            params = (new, pk)
            cursor.execute(query, params)
            conn.commit()

    def retrieve(self, pk_name: str, pk):
        """
        find existing records in the database
        pk_name can only be "cca_id" or "name"
        """
        if pk_name not in ['cca_id', 'name']:
            raise AttributeError(f'Invalid pk_name {pk_name}')
        with sqlite3.connect('meow.db') as conn:
            cursor = conn.cursor()
            query = f"""
                SELECT *
                FROM {self.table_name} ;
                WHERE {pk_name} = ? ;
            """
            params = (pk, )
            cursor.execute(query, params)
            record = cursor.fetchone()
            conn.commit()
            # conn.close() is called automatically
            return record

    def delete(self, pk_name: str, pk):
        """
        remove existing records in the database
        pk_name can only be "cca_id" or "name"
        """
        if pk_name not in ['cca_id', 'name']:
            raise AttributeError(f'Invalid pk_name {pk_name}')
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    DELETE FROM {self.table_name}
                    WHERE {pk_name} = ?;
                    """
            params = (pk, )
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
                    "organiser_id" INTEGER, 
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
        """find existing records in the database"""
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
        """remove existing records in the database"""
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

    # def insert(self, student_id: int, activity_id: int):
    #     """insert new records into the database"""
    #     with sqlite3.connect(self.database_name) as conn:
    #         cursor = conn.cursor()
    #         query = f"""
    #             INSERT INTO {self.table_name} ({self.pk1_name}, {self.pk2_name}) VALUES (?, ?);
    #         """
    #         params = (student_id, activity_id)
    #         cursor.execute(query, params)
    #         conn.commit()
    #         #conn.close() is called automatically

    # def retrieve_all(self, pk_name: str, pk: int):
    #     """
    #     find existing records in the database
    #     pk_name can only be "student_id" or "activity_id"
    #     retrieves all data regarding the student or activity
    #     """
    #     self._valid_field_else_error(pk_name)
    #     with sqlite3.connect(self.table_name) as conn:
    #         cursor = conn.cursor()
    #         query = f"""
    #                 SELECT *
    #                 FROM {self.table_name}
    #                 WHERE {pk_name} = ?;
    #                 """
    #         params = (pk, )
    #         cursor.execute(query, params)
    #         record = cursor.fetchall()
    #         conn.commit()
    #         #conn.close() is called automatically
    #     return record

    # def delete(self, student_id: int, activity_id: int):
    #     """remove existing records in the database"""
    #     with sqlite3.connect(self.database_name) as conn:
    #         cursor = conn.cursor()
    #         query = f"""
    #                 DELETE FROM {self.table_name}
    #                 WHERE {self.pk1_name} = ? AND {self.pk2_name} = ?;
    #                 """
    #         param = (student_id, activity_id)
    #         cursor.execute(query, param)
    #         conn.commit()


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
    
    def insert(self, student_id: int, cca_id: int, role: str):
        """insert new records into the database"""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                INSERT INTO {self.table_name} ({self.pk1_name}, {self.pk2_name}, "role") VALUES (?, ?, ?);
            """
            params = (student_id, cca_id, role)
            cursor.execute(query, params)
            conn.commit()

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

    def retrieve_one(self, student_id: int, cca_id: int):
        """
        retrieves the record regarding the particular student and cca
        mainly used for finding the record concerning both the student and cca 
        (e.g. role)
        """
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    SELECT *
                    FROM {self.database_name}
                    WHERE "student_id" = ? AND "cca_id" = ?;
                    """
            params = (student_id, cca_id)
            cursor.execute(query, params)
            record = cursor.fetchone()
            conn.commit()
        return record

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
