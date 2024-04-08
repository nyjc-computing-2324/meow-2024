import sqlite3

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

# class JunctionTable(Table):

#     def __init__(self):

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
        field can only be "username" or "password"
        return False if inputs are wrong
        return True if inputs are correct
        checks for repeated username should already be done
        """
        if field not in ['username', 'password', 'salt']:
            raise Exception('field entered incorrectly')
                
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
        return True

    

    def retrieve(self, field: str, data) -> tuple:
        """
        find existing records in the database
        field can only be "account_id" or "username"
        error raised if field entered incorrectly 
        """
        if field not in ['username', 'password', 'salt']:
            raise Exception('field entered incorrectly')
        
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
        error raised if field entered incorrectly 
        """

        if field not in ['username', 'password', 'salt']:
            raise Exception('field entered incorrectly')
            
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
        field can only be "account_id" "name" "class" or "email"
        return False if inputs are wrong
        return True if inputs are correct
        checks for valid account_id should already be done
        raise error if field entered incorrectly
        xinyu
        """
        if field not in ['account_id','name', 'class','email']:
            return False
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
                    WHERE {field} == ?;
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
            query = f"""
                    DELETE FROM {self.table_name}
                    WHERE "student_id" = ?;
                    """
            param = (student_id,)
            cursor.execute(query, param)
            conn.commit()

class CCA(Table):
    table_name: str = "cca"
    fields = ["cca_id", "name", "type"]
    
    def __init__(self):
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
                    "cca_id" INTEGER PRIMARY KEY,
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
        yu xi
        """
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            query = f"""
                UPDATE {self.table_name}
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
            query = f"""
                SELECT *
                FROM {self.table_name} ;
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
            query = f"""
                    DELETE FROM {self.table_name}
                    WHERE "cca_id" = ?;
                    """
            params = (cca_id,)
            cursor.execute(query, params)
            conn.commit()

class Activity(Table):
    table_name: str = "activity"
    fields = ["student_id", "name", "date", "location"]

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
                    "student_id" INTEGER PRIMARY KEY,
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
                INSERT INTO {self.table_name}("name", "date", "location", "organiser_id")
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
                UPDATE {self.table_name}
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
                FROM {self.table_name}
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
            query = f"""
                    DELETE FROM {self.table_name}
                    WHERE "account_id" = ?;
                    """
            params = (account_id,)
            cursor.execute(query, params)
            conn.commit()

class StudentActivity:

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