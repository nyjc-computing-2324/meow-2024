from database import Account, Student, CCA, Activity
import auth
import os
import psycopg2
import sqlite3

def sqlite_conn(uri):
    return sqlite3.connect(uri)

def postgres_conn(uri):
    return psycopg2.connect(uri)

def get_uri(env: str = ""):
    env = env or os.getenv("ENVIRONMENT", default = "")
    if env in ["main", "dev"]:
        uri = os.getenv("DATABASE_URL")
    elif env == "qa":
        uri = ":memory:"
    else:
        uri = "meow.db"

def conn_factory(env, uri):
    """Returns a connection getter: a function that returns a connection when called"""
    def get_conn():
        if env in ["main", "dev"]:
            conn = postgres_conn(uri)
        elif env == "qa":
            conn = sqlite_conn(uri)
        else:
            conn = sqlite_conn(uri)
        return conn
    return get_conn

def get_account(env: str = "") -> Account:
    """returns an instance of Account with an appropriate db conn"""
    uri = get_uri(env)
    return Account(conn_factory(env, uri))

def get_student(env: str = "") -> Student:
    """returns an instance of Student with an appropriate db conn"""
    uri = get_uri(env)
    return Student(conn_factory(env, uri))

def get_cca(env: str = "") -> CCA:
    """returns an instance of CCA with an appropriate db conn"""
    uri = get_uri(env)
    return CCA(conn_factory(env, uri))

def get_activity(env: str = "") -> Activity:
    """returns an instance of Activity with an appropriate db conn"""
    uri = get_uri(env)
    return Activity(conn_factory(env, uri))

# instantiating table objects
#student_account = get_account()
#student_profile = get_student()

# FOR ACCOUNT TABLE
def create_account(username: str, password: str):
    """
    if username already exists, attribute error is raised
    else data is inserted into student_account and student_account_backup
    """
    # check for repeated username
    if student_account.retrieve("username", username) is not None:
        raise AttributeError("Username already exists")
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

def update_account(pk_name: str, pk, field: str, data):
    """
    if account does not exists, attribute error is raised
    else account updated in student_account and student_account_backup
    field can only be "username", "password" or "salt"
    pk_name can only be "account_id" or "username"
    if username already exists and is to be updated, attribute error is raised
    """
    if student_account.retrieve(pk_name, pk) is None:
        raise AttributeError("Account does not exist")
    if field == "username" and student_account.retrieve("username", data) is not None:
        raise AttributeError("Username already exist")
    student_account.update(pk_name, pk, field, data)
    student_account_backup.update(pk_name, pk, field, data)

def retrieve_account(pk_name: str, pk) -> dict:
    """
    obtain information for an account
    if account does not exists, attribute error is raised
    else a dictionary of account_id, username, password, salt is returned
    pk_name can only be "account_id" or "username"
    """
    record = student_account.retrieve(pk_name, pk)
    if record is None:
        raise AttributeError("Account does not exist")
    account_id, username, password, salt = record
    record_dict = {'account_id': account_id, 'username': username, 'password': password, 'salt': salt}
    return record_dict

def delete_account(pk_name: str, pk):
    """
    if account does not exists, attribute error is raised
    else delete account from student_account and student_account_backup
    pk_name can only be "account_id" or "username"
    """
    if student_account.retrieve(pk_name, pk) is None:
        raise AttributeError("Account does not exist")
    student_account.delete(pk_name, pk)
    student_account_backup.delete(pk_name, pk)


# FOR STUDENT TABLE
def create_profile(name, _class, email, account_id):
    """
    if account_id does not exist in account table, attribute error is raised
    else data is inserted into student_profile and student_profile_backup
    """
    if student_account.retrieve("account_id", account_id) is None:
        raise AttributeError("Invalid account id")
    student_profile.insert(name, _class, email, account_id)
    student_profile_backup.insert(name, _class, email, account_id)

def update_profile(student_id: int, field: str, data):
    """
    if profile does not exists, attribute error is raised
    if account_id does not exist in account table, attribute error is raised
    else account updated in student_account and student_account_backup
    field can only be "account_id", "name", "class" or "email"
    """
    if student_profile.retrieve(student_id) is None:
        raise AttributeError("Student profile does not exist")
    if field == "account_id" and student_account.retrieve("account_id", data) is None:
        raise AttributeError("Invalid account id")
    student_profile.update(student_id, field, data)
    student_profile_backup.update(student_id, field, data)

def retrieve_profile(student_id: int):
    """
    obtain information for an account
    if account does not exists, attribute error is raised
    else a dictionary of student_id, name, class, email, account_id is returned
    """
    record = student_profile.retrieve(student_id)
    if record is None:
        raise AttributeError("Profile does not exist.")
    student_id, name, _class, email, account_id = record
    record_dict = {'student_id': student_id, 'name': name, 'class': _class, 'email': email, 'account_id': account_id}
    return record_dict

def delete_profile(student_id: int):
    """
    if account does not exists, attribute error is raised
    else delete account from student_profile and student_profile_backup
    """
    if student_profile.retrieve(student_id) is None:
        raise AttributeError("Profile does not exist.")
    student_profile.delete(student_id)
    student_profile_backup.delete(student_id)