import sqlite3

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

    def __init__(self):
        """
        create a table upon initialisation of the class
        account id for primary key
        """

        with sqlite3.connect("meow.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS "account"(
                "account_id" INTEGER,
                "username" TEXT NOT NULL UNIQUE,
                "password" TEXT NOT NULL,
                PRIMARY KEY ("account_id")
                );
                """
            )
            conn.commit()

    def insert(self, username: str, password: str):
        """
        insert new records into the database
        checks for repeated username should already be done
        """
        with sqlite3.connect('meow.db') as conn:
            cursor = conn.cursor()
            query = """
                    INSERT INTO "account" ("username", "password") VALUES (?, ?);
                    """
            params = (username, password)
            cursor.execute(query, params)
            conn.commit()
        
    def update(self, account_id: str, field: str, new: str):
        """
        update existing records in the database
        field can only be "username" or "password"
        return False if inputs are wrong
        return True if inputs are correct
        checks for repeated username should already be done
        """

        with sqlite3.connect('meow.db') as conn:
            cursor = conn.cursor()
            if field not in ['username', 'password']:
                return False
            
            query = f"""
                    UPDATE "account" 
                    SET {field} = ? 
                    WHERE "account_id" = ? 
                    """
            params = (new, account_id)
            cursor.execute(query, params)

    def retrieve(self, field: str, data) -> tuple:
        """
        find existing records in the database
        field can only be "account_id" or "password"
        """
            
        with sqlite3.connect('meow.db') as conn:
            cursor = conn.cursor()
            query = f"""
                    SELECT *
                    FROM "Account"
                    WHERE {field} == ?;
                    """
            params = (data,)
            cursor.execute(query, params)
            record = cursor.fetchone()
            conn.commit()
            return record

    def delete(self, account_id: int):
        """remove existing records in the database"""
        with sqlite3.connect('meow.db') as conn:
            cursor = conn.cursor()
            query = """
                    DELETE FROM "Account"
                    WHERE "account_id" = ?;
                    """
            param = (account_id,)
            cursor.execute(query, param)
            conn.commit()

class Student:

    def __init__(self):
        """
        create a table upon initialisation of the class
        student_id for pk
        """
        pass

    def insert(self, name: str, _class: int, email: str, account_id: int):
        """insert new records into the database"""
        raise NotImplementedError

    def update(self, student_id: int, field: str, new: str):
        """update existing records in the database"""
        raise NotImplementedError

    def retrieve(self, field: str, data):
        """find existing records in the database"""
        raise NotImplementedError

    def delete(self, student_id: int):
        """remove existing records in the database"""
        raise NotImplementedError

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
student_account = Account()

def create_account(username: str, password: str):
    # checks for valid username and password is already done 
    # check for repeated username
    if student_account.retrieve("username", username) is None:
        student_account.insert(username, password)

def login(username: str , password: str) -> bool:
    # checks for valid username and password is already done 
    
    data = student_account.retrieve("username", username)
    # account not found
    if data is None:
        return False
    
    account_id, database_username, database_password = data
    # salting and hashing of password not yet implemented
    return database_password == password
