import sqlite3

class Table():
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
        """remove existing records in the database"""
        raise NotImplementedError

class Account():

        def __init__(self):
            """
            create a table upon initialisation of the class
            account id for primary key
            jae zen
            """

            with sqlite3.connect("meow.db") as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS "Account"(
                    "account_id" <INTEGER> <PRIMARY KEY>,
                    "username" <TEXT> <NOT NULL>,
                    "password" <TEXT> <NOT NULL>
                    )
                    """
                )
                conn.commit()
                
            

        def insert(self, account_id: int, username: str, password: str):
            """insert new records into the database
               yu xi
            """
            with sqlite3.connect('meow.db') as conn:
                cursor = conn.cursor
                cursor.execute(
                    """
                    INSERT INTO "Account"(
                        "account_id",
                        "username",
                        "password"
                    ) VALUES (
                        account_id,
                        username,
                        password
                    );
                    """
                )
                conn.commit()
            
        def update(self, account_id: str, field: str, new: str):
            """update existing records in the database
               field can only be "username" or "password"
               return False if inputs are wrong
               return True if inputs are correct
            """

            with sqlite3.connect('meow.db') as conn:
                cursor = conn.cursor
                if field not in ['username', 'password']:
                    return False
                
                query = f"""
                        UPDATE "Account" 
                        SET {field} = ? 
                        WHERE "account_id" = ? 
                        """
            
                params = (new, account_id)
                cursor.execute(query, params)

                

                

            

        def retrieve(self, username: str):
            """find existing records in the database"""
            raise NotImplementedError

        def delete(self, username: str):
            """remove existing records in the database (Vincent)"""
            with sqlite3.connect('meow.db') as conn:
                cursor = conn.cursor()
                query = """
                        DELETE FROM "Account"
                        WHERE "username" = ?;
                        """
                param = (username,)
                cursor.execute(query, param)
                conn.commit()
                #conn.close is automatically called