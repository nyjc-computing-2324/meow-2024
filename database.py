import sqlite3
import auth.py

class Table:
    """parent class for all subsequent tables"""

    def __init__(self):
        "create a table upon initialisation of the class"
        pass

    def insert(self):
        """insert new records into the database"""
        raise NotImplementedError

    def update(self):
        """update existing records in the database"""
        raise NotImplementedError

    def retrieve(self):
        """find existing records in the database"""
        raise NotImplementedError

    def delete(self):
        """remove existing records in the database (Vincent)"""
        raise NotImplementedError

class Account:

    def __init__(self, database_name: str):
        """
        create a table upon initialisation of the class
        account id for primary key
        """
        self.database_name = database_name
        self.not_null = ["username", "password", "salt"]
        with sqlite3.connect(database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS "account"(
                "account_id" INTEGER,
                "username" TEXT NOT NULL UNIQUE,
                "password" TEXT NOT NULL,
                "salt" TEXT NOT NULL
                PRIMARY KEY ("account_id")
                );
                """
            )
            conn.commit()

    def insert(self, data: dict):
        """
        insert new records into the database
        data must contain username: str, password: str, salt: str
        checks for repeated username should already be done
        """
        keys = data.keys()
        for key in self.not_null:
            if key not in keys:
                return False
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = """
                    INSERT INTO "account" ("username", "password", "salt") VALUES (?, ?, ?);
                    """
            params = (data["username"], data["password"], data["salt"])
            cursor.execute(query, params)
            conn.commit()
        return True
        
    def update(self, account_id: int, field: str, new: str):
        """
        update existing records in the database
        field can only be "username" or "password"
        return False if inputs are wrong
        return True if inputs are correct
        checks for repeated username should already be done
        """
        if field not in ['username', 'password', 'salt']:
            return False
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()            
            query = f"""
                    UPDATE "account" 
                    SET {field} = ? 
                    WHERE "account_id" = ? 
                    """
            params = (new, account_id)
            cursor.execute(query, params)
        return True

    def retrieve(self, field: str, data) -> tuple:
        """
        find existing records in the database
        field can only be "account_id" or "username"
        """
            
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    SELECT *
                    FROM "account"
                    WHERE {field} == ?;
                    """
            params = (data,)
            cursor.execute(query, params)
            record = cursor.fetchone()
            conn.commit()
            return record

    def delete(self, field: str, data):
        """
        remove existing records in the database
        field can only be "account_id" or "username"
        """
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    DELETE FROM "account"
                    WHERE {field} = ?;
                    """
            param = (data,)
            cursor.execute(query, param)
            conn.commit()

class Student:

    def __init__(self, database_name):
        """
        create a table upon initialisation of the class
        student_id for pk
        yu xi
        """
        self.database_name = database_name
        self.not_null = ["name", "account_id"]
        with sqlite3.connect(database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS "student" (
                    "student_id" INTEGER PRIMARY KEY,
                    "name" TEXT NOT NULL,
                    "class" INTEGER, 
                    "email" TEXT,
                    "account_id" INTEGER NOT NULL UNIQUE
                    FOREIGN KEY ("account_id") REFERENCES account("account_id")
                );
                """
            )
            conn.commit()
            #conn.close() called automatically

    def insert(self, data: dict):
        """
        insert new records into the database
        data can contain name: str, _class: int, email: str, account_id: int
        data must contain name: str, account_id: int
        yu xi
        """
        keys = data.keys()
        for key in self.not_null:
            if key not in keys:
                return False
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            for field in keys:
                query = f"""
                    INSERT INTO "student"({field}) VALUES (?);
                """
                params = (data[field],)
                cursor.execute(query, params)
            conn.commit()
            #conn.close() called automatically
        return True

    def update(self, student_id: int, field: str, new):
        """
        update existing records in the database
        field can only be "account_id" "name" "class" or "email"
        return False if inputs are wrong
        return True if inputs are correct
        checks for valid account_id should already be done
        xinyu
        """
        
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            if field not in ['account_id','name', 'class','email']:
                return False

            query = f"""
                    UPDATE "student" 
                    SET {field} = ? 
                    WHERE "student_id" = ? 
                    """
            params = (new, student_id)
            cursor.execute(query, params)


    def retrieve(self, field: str, data):
        """
        find existing records in the database
        field can only be "account_id" "class" or "email"
        xinyu
        """

        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    SELECT *
                    FROM "student"
                    WHERE {field} == ?;
                    """
            params = (data,)
            cursor.execute(query, params)
            record = cursor.fetchone()
            conn.commit()
            return record
            

    def delete(self, student_id: int):
        """remove existing records in the database"""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = """
                    DELETE FROM "student"
                    WHERE "student_id" = ?;
                    """
            param = (student_id,)
            cursor.execute(query, param)
            conn.commit()

class CCA:

    def __init__(self):
        """
        create a table upon initialisation of the class
        cca_id for pk
        """
        pass

    def insert(self, name: str, type: str):
        """insert new records into the database"""
        raise NotImplementedError

    def update(self, cca_id: int, field: str, new: str):
        """update existing records in the database"""
        raise NotImplementedError

    def retrieve(self, cca_id: int):
        """find existing records in the database"""
        raise NotImplementedError

    def delete(self, cca_id: int):
        """remove existing records in the database"""
        raise NotImplementedError

class Activity:

    def __init__(self):
        """
        create a table upon initialisation of the class
        activity_id for pk
        """
        pass

    def insert(self, name: str, date: str, location: str, organiser_id: int):
        """insert new records into the database"""
        raise NotImplementedError

    def update(self, account_id: int, field: str, new: str):
        """update existing records in the database"""
        raise NotImplementedError

    def retrieve(self, account_id: int):
        """find existing records in the database"""
        raise NotImplementedError

    def delete(self, account_id: int):
        """remove existing records in the database"""
        raise NotImplementedError
        
# instantiating table objects
student_account = Account("meow.db")
student_account_backup = Account("backup.db")

def create_account(username: str, password: str):
    # checks for valid username and password is already done 
    # check for repeated username
    if student_account.retrieve("username", username) is None:
        password, salt = auth.create_hash(password)
        salt = str(salt)
        student_account.insert(username, password, salt)
        student_account_backup.insert(username, password, salt)

def login(username: str , password: str) -> bool:
    # checks for valid username and password is already done 
    
    data = student_account.retrieve("username", username)
    # account not found
    if data is None:
        return False
    
    account_id, database_username, database_password, database_salt = data
    # salting and hashing of password implemented 
    return auth.check_password(password, database_password, database_salt)
