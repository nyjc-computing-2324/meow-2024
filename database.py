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
        """remove existing records in the database (Vincent)"""
        raise NotImplementedError

class Account(Table):

        def __init__(self):
            """
            create a table upon initialisation of the class
            account id/*username* for pk
            """
            pass

        def insert(self, username: str, password: str):
            """insert new records into the database"""
            raise NotImplementedError

        def update(self, username: str, field: str, new: str):
            """update existing records in the database"""
            raise NotImplementedError

        def retrieve(self, username: str):
            """find existing records in the database"""
            raise NotImplementedError

        def delete(self, username: str):
            """remove existing records in the database"""
            raise NotImplementedError