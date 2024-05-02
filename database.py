import sqlite3
from typing import Callable


def init_tables(get_conn: Callable):
    """creates the table for all table in database"""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS "account" (
        "account_id" INTEGER PRIMARY KEY,
        "username" TEXT NOT NULL UNIQUE,
        "password" TEXT NOT NULL,
        "salt" BYTES NOT NULL
        );
        CREATE TABLE IF NOT EXISTS "student" (
            "student_id" INTEGER PRIMARY KEY,
            "name" TEXT NOT NULL,
            "class" INTEGER NOT NULL, 
            "email" TEXT NOT NULL,
            "account_id" INTEGER NOT NULL UNIQUE,
            "number" INTEGER,
            "about" TEXT,
            FOREIGN KEY ("account_id") REFERENCES account("account_id")
        );
        CREATE TABLE IF NOT EXISTS "cca" (
            "cca_id" INTEGER PRIMARY KEY,
            "name" TEXT NOT NULL UNIQUE,
            "type" TEXT NOT NULL 
        );
        CREATE TABLE IF NOT EXISTS "activity" (
            "activity_id" INTEGER PRIMARY KEY,
            "name" TEXT NOT NULL UNIQUE,
            "date" TEXT NOT NULL, 
            "location" TEXT NOT NULL,
            "organiser_id" INTEGER,
            FOREIGN KEY ("organiser_id") REFERENCES account("student_id")
        );
        CREATE TABLE IF NOT EXISTS "studentactivity" (
            "student_id" INTEGER NOT NULL,
            "activity_id" INTEGER NOT NULL,
            PRIMARY KEY ("student_id", "activity_id"),
            FOREIGN KEY ("student_id") REFERENCES student("student_id"),
            FOREIGN KEY ("activity_id") REFERENCES activity("activity_id")
        );
        CREATE TABLE IF NOT EXISTS "studentcca" (
            "student_id" INTEGER,
            "cca_id" INTEGER,
            "role" TEXT NOT NULL,
            "year" INTEGER NOT NULL,
            "status" TEXT NOT NULL,
            PRIMARY KEY ("student_id", "cca_id"),
            FOREIGN KEY ("student_id") REFERENCES student("student_id"),
            FOREIGN KEY ("cca_id") REFERENCES cca("cca_id")
        );
        """
    )
    conn.commit()
    conn.close()

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
    unique_field: str  #used to obtain the primary key

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
        fetch: bool = False,
        fetchall: bool = False
    ):
        """executes the query based on the connection, given query and params"""
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
        if fetchall:
            record = cursor.fetchall()
            return record
        if commit:
            conn.commit()
        conn.close()

    def insert(self, record: dict) -> None:
        """
        inserts the record into the junction table

        Checks for redundancies should already be done
        i.e. if unqiue field name == panda already exists in the table,
        dont insert another record with name == panda

        record argument that is passed should have:
        keys of type str referring to the fields
        values of corresponding types referring to the values to be put in the cells
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
        self._execute_query(query, tuple(record.values()), commit=True)
        
    def update(self, pk: int, field: str, new: str) -> None:
        """update existing records in the database"""
        self._valid_field_else_error(field)
        query = f"""
                UPDATE {self.table_name} 
                SET {field} = ? 
                WHERE {self.pk_name} = ? 
                """
        params = (new, pk)
        self._execute_query(query, params, commit=True)

    def retrieve(self, pk: int) -> tuple | None:
        """find existing records in the database"""
        query = f"""
                SELECT *
                FROM {self.table_name}
                WHERE {self.pk_name} = ?;
                """
        params = (pk,)
        record = self._execute_query(query, params, fetch=True)
        return record

    def retrieve_primary_key(self, unique_field) -> int | None:
        """obtain primary key using unique field in the table"""
        query = f"""
                SELECT *
                FROM {self.table_name}
                WHERE {self.unique_field} = ?;
                """
        params = (unique_field,)
        record = self._execute_query(query, params, fetch=True)
        if record is not None:
            primary_key, *rest = record
            return primary_key
        return record

    def delete(self, pk: int):
        """remove existing records in the database"""
        query = f"""
                DELETE FROM {self.table_name}
                WHERE {self.pk_name} = ?;
                """
        params = (pk, )
        self._execute_query(query, params, commit=True)

    def get_all_entries(self):
        """gets all entries in the table"""
        query = f"""
                SELECT *
                FROM {self.table_name}
                """
        record = self._execute_query(query, (), fetchall=True)
        return record

class JunctionTable(Table):
    table_name: str
    pk1_name: str
    pk2_name: str
    fields: list[str]

    def retrieve_all(self, pk_name: str, pk: int) -> list[tuple] | None:
        """
        find existing records in the database
        retrieves all data regarding the student or cca

        e.g. using a StudentCCA object:
        .retrieve_all("cca_id", 3)
        returns
        [(5, 3, "member"), (7. 3, "president"), (10, 3, "member")]
        """
        self._valid_field_else_error(pk_name)
        
        query = f"""
                SELECT *
                FROM {self.table_name}
                WHERE {pk_name} = ?;
                """
        params = (pk, )
        return self._execute_query(query, params, fetchall=True)

    def delete(self, pk1_value: int, pk2_value: int) -> None:
        """remove existing records in the database using composite primary keys """
        query = f"""
                DELETE FROM {self.table_name}
                WHERE {self.pk1_name} = ?
                AND
                {self.pk2_name} = ?;
                """
        param = (pk1_value, pk2_value)
        self._execute_query(query, param, commit=True)

class Account(Table):
    table_name = "account"
    pk_name = "account_id"
    fields = ["account_id", "username", "password", "salt"]
    unique_field = "username"

class Student(Table):
    table_name = "student"
    pk_name = "student_id"
    fields = ["student_id", "name", "class", "email", "number", "about", "account_id"]
    unique_field = "account_id"

class CCA(Table):
    table_name = "cca"
    pk_name = "cca_id"
    fields = ["cca_id", "name", "type"]
    unique_field = "name"

class Activity(Table):
    table_name: str = "activity"
    pk_name = "activity_id"
    fields = ["activity_id", "name", "date", "location", "organiser_id"]
    unique_field = "name"

class StudentActivity(JunctionTable):
    
    table_name: str = "studentactivity"
    pk1_name: str = "student_id"
    pk2_name: str = "activity_id"
    fields = ["student_id", "activity_id"]

class StudentCCA(JunctionTable):

    table_name: str = "studentcca"
    pk1_name: str = "student_id"
    pk2_name: str = "cca_id"
    fields = ["student_id", "cca_id", "role", "year", "status"]

    def update(self, student_id: int, cca_id: int, field: str, data):
        """
        update existing records in the database
        field can only be "role", "year", "status"
        To "update" student_id or cca_id, instead use .remove() and .insert()
        """
        super()._valid_field_else_error(field)
        query = f"""
                UPDATE {self.table_name} 
                SET {field} = ? 
                WHERE {self.pk1_name} = ? AND {self.pk2_name};
                """
        params = (data, student_id, cca_id)
        self._execute_query(query, params)

    def retrieve_one(self, student_id: int, cca_id: int):
        """
        retrieves the record regarding the particular student and cca
        mainly used for finding the record concerning both the student and cca 
        (e.g. role)
        """
        query = f"""
                SELECT *
                FROM {self.table_name}
                WHERE "student_id" = ? AND "cca_id" = ?;
                """
        params = (student_id, cca_id)
        return self._execute_query(query, params)