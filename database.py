import sqlite3
import auth

class Table:
    """parent class for all subsequent tables"""

    def __init__(self, pk: int, database_name: str):
        "create a table upon initialisation of the class"
        self.pk = pk
        self.database_name = database_name

    def insert(self):
        """insert new records into the database"""
        raise NotImplementedError

    def update(self):
        """update existing records in the database"""
        raise NotImplementedError

    def retrieve(self):
        """find existing records in the database"""
        raise NotImplementedError

    def delete(self, pk: int):
        """remove existing records in the database"""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    DELETE FROM "{self.table_name}"
                    WHERE "{self.pk}" = ?;
                    """
            params = (pk,)
            cursor.execute(query, params)
            conn.commit()

# class JunctionTable(Table):

#     def __init__(self):

class Account(Table):
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
                """
                CREATE TABLE IF NOT EXISTS "account"(
                "account_id" INTEGER,
                "username" TEXT NOT NULL UNIQUE,
                "password" TEXT NOT NULL,
                "salt" BYTES NOT NULL,
                PRIMARY KEY ("account_id")
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
            query = """
                    INSERT INTO "account" ("username", "password", "salt") VALUES (?, ?, ?);
                    """
            params = (username, password, salt)
            cursor.execute(query, params)
            conn.commit()
            #conn.close() called automatically
        
    def update(self, account_id: int, field: str, new):
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
            conn.commit()
        #conn.close() called automatically
        return True

    def _valid_field_else_error(self, field) -> None:
        if field not in self.fields:
            raise AttributeError(f"Invalid field '{field}'")

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
            #conn.close() called automatically

class Student(Table):

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
            #conn.close() called automatically

    def insert(self, name: str, _class: int, email: str, account_id: int):
        """
        insert new records into the database
        checks for valid account_id should already be done
        yu xi
        """
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = """
                INSERT INTO "student"("name", "class", "email", "account_id") 
                VALUES (?, ?, ?, ?);
            """
            params = (name, _class, email, account_id)
            cursor.execute(query, params)
            conn.commit()
            #conn.close() called automatically

    def update(self, student_id: int, field: str, new):
        """
        update existing records in the database
        field can only be "account_id" "name" "class" or "email"
        return False if inputs are wrong
        return True if inputs are correct
        checks for valid account_id should already be done
        xinyu
        """
        if field not in ['account_id','name', 'class','email']:
            return False
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                    UPDATE "student" 
                    SET {field} = ? 
                    WHERE "student_id" = ? 
                    """
            params = (new, student_id)
            cursor.execute(query, params)
            conn.commit()
            #conn.close() called automatically
            return True


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
                    WHERE {field} = ?;
                    """
            params = (data,)
            cursor.execute(query, params)
            record = cursor.fetchone()
            conn.commit()
            #conn.close() called automatically
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

class CCA(Table):

    def __init__(self):
        """
        create a table upon initialisation of the class
        cca_id for pk
        jae zen
        """

        with sqlite3.connect('meow.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS "activity" (
                    "cca_id" INTEGER PRIMARY KEY,
                    "name" TEXT NOT NULL,
                    "type" TEXT, 
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
            query = """
                INSERT INTO 'cca' ("name", "type") VALUES (?, ?);
            """
            params = (name, type)
            cursor.execute(query, params)
            conn.commit()
            # conn.close() is called automatically
    
    def update(self, cca_id: int, field: str, new: str):
        """
        update existing records in the database
        yu xi
        """
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                UPDATE 'cca'
                SET {field} = ?
                WHERE cca_id = ? ;                
            """
            params = (new, cca_id)
            cursor.execute(query, params)
            conn.commit()
            # conn.close() is called automatically
        return T

    def retrieve(self, cca_id: int):
        """
        find existing records in the database
        yu xi
        """
        with sqlite3.connect('meow.db') as conn:
            cursor = conn.cursor()
            query = """
                SELECT *
                FROM 'cca' ;
                WHERE 'cca_id' = ? ;
            """
            params = (cca_id,)
            cursor.execute(query, params)
            conn.commit()
            # conn.close() is called automatically

    def delete(self, cca_id: int):
        """remove existing records in the database"""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = """
                    DELETE FROM "cca"
                    WHERE "cca_id" = ?;
                    """
            params = (cca_id,)
            cursor.execute(query, params)
            conn.commit()

class Activity(Table):

    def __init__(self):
        """
        create a table upon initialisation of the class
        activity_id for pk
        jae zen
        """

        with sqlite3.connect('meow.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS "activity" (
                    "student_id" INTEGER PRIMARY KEY,
                    "name" TEXT NOT NULL,
                    "date" TEXT, 
                    "location" TEXT,
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
            
            query = """
                INSERT INTO "activity"("name", "date", "location", "organiser_id")
                VALUES( ?, ?, ?, ? );
                """
            params = (name, date, location, organiser_id)
            cursor.execute(query, params)
            conn.commit()
            #conn.close() called automatically

    def update(self, account_id: int, field: str, new: str):
        """
        update existing records in the database
        field can only be "organiser_id" "name" "date" or "location"
        return False if inputs are wrong
        return True if inputs are correct
        checks for valid organiser_id should already be done
        xinyu
        """
        if field not in ['organiser_id','name', 'date','location']:
            return False
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            
            query = f"""
                UPDATE "activity"
                SET {field} = ?
                where "activity_id" = ?
                """
            params = (new, activity_id)
            cursor.execute(query, params)
            conn.commit
            #conn.close() called automatically
        return True

    def retrieve(self, account_id: int):
        """
        find existing records in the database
        xinyu
        """
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor
            query = f"""
                SELECT *
                FROM "activity"
                where {field} = ?
            """
            params = (account_id,)
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
            query = """
                    DELETE FROM "account"
                    WHERE "account_id" = ?;
                    """
            params = (account_id,)
            cursor.execute(query, params)
            conn.commit()

class StudentActivity(Table):

    def __init__(self):
        """
        create a table upon initialisation of the class
        (student_id, activity_id) for pk

        This class has no .update() method.
        To "update", instead use .remove() and .insert()
        """
        raise NotImplementedError

    def insert(self, student_id: int, activity: int):
        """insert new records into the database"""
        raise NotImplementedError

    def retrieve(self, student_id: int, activity_id: int):
        """find existing records in the database"""
        raise NotImplementedError

    def delete(self, student_id: int, activity_id: int):
        """remove existing records in the database"""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = """
                    DELETE FROM "student_activity"
                    WHERE "student_id" = ?, 
                    "activity_id" = ?;
                    """
            param = (student_id, activity_id)
            cursor.execute(query, param)
            conn.commit()


# instantiating table objects
student_account = Account("meow.db")
student_account_backup = Account("backup.db")

def create_account(username: str, password: str):
    # checks for valid username and password is already done 
    # check for repeated username
    if student_account.retrieve("username", username) is None:
        password, salt = auth.create_hash(password)
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
