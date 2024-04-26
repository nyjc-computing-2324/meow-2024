from database import Account, Student, CCA, Activity, StudentActivity, StudentCCA
import auth
import os
import psycopg2
import sqlite3

def sqlite_conn(uri):
    return sqlite3.connect(uri)

def postgres_conn(uri):
    return psycopg2.connect(uri)

def get_uri(env: str = ""):
    """identifies and returns the uri/database name based on app screts of the repl"""
    env = env or os.getenv("ENVIRONMENT", default = "")
    if env in ["main", "dev"]:
        uri = os.getenv("DATABASE_URL")
    elif env == "qa":
        uri = ":memory:"
    else:
        uri = "meow.db"
    return uri

def conn_factory(env, uri):
    """Returns a connection getter: a function that returns a connection when called"""
    def get_conn():
        _env = env or os.getenv("ENVIRONMENT", default = "")
        if _env in ["main", "dev"]:
            conn = postgres_conn(uri)
        elif _env == "qa":
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

# cca_info = CCA("meow.db")
# cca_info_backup = CCA("backup.db")
# cca_info_testing = CCA("test.db")

# activity_info = Activity("meow.db")
# activity_info_backup = Activity("backup.db")
# activity_info_testing = Activity("test.db")

# student_activity = StudentActivity('meow.db')
# student_activity_backup = StudentActivity('backup.db')
# student_activity_testing = StudentActivity('test.db')

# student_cca = StudentCCA('meow.db')
# student_cca_backup = StudentCCA('backup.db')
# student_cca_testing = StudentCCA('test.db')

# instantiating table objects
account = get_account()
student_profile = get_student()

# FOR ACCOUNT TABLE
def create_account(username: str, password: str):
    """
    if username already exists, attribute error is raised
    else data is inserted into account and account_backup
    """
    # check for repeated username
    if account.retrieve(username, "username") is not None:
        raise AttributeError("Username already exists")
    password, salt = auth.create_hash(password)
    account.insert({'username': username, 'password': password, 'salt': salt})

def login(username: str , password: str) -> bool:
    # checks for valid username and password is already done 

    data = account.retrieve(username, "username")
    # account not found
    if data is None:
        return False

    account_id, database_username, database_password, database_salt = data
    # salting and hashing of password implemented 
    return auth.check_password(password, database_password, database_salt)

def username_taken(username) -> bool:
    #checks if the username is already in use
    data = account.retrieve(username, "username")
    if data is None:
        return True
    return False

def update_account(pk_name: str, pk, field: str, data):
    """
    if account does not exists, attribute error is raised
    else account updated in account and account_backup
    field can only be "username", "password" or "salt"
    pk_name can only be "account_id" or "username"
    if username already exists and is to be updated, attribute error is raised
    """
    if account.retrieve(pk, pk_name) is None:
        raise AttributeError("Account does not exist")
    if field == "username" and account.retrieve(data, "username") is not None:
        raise AttributeError("Username already exist")
    account.update(pk, pk_name, field, data)
    account_backup.update(pk, pk_name, field, data)

def retrieve_account(pk_name: str, pk) -> dict:
    """
    obtain information for an account
    if account does not exists, attribute error is raised
    else a dictionary of account_id, username, password, salt is returned
    pk_name can only be "account_id" or "username"
    """
    record = account.retrieve(pk, pk_name)
    if record is None:
        raise AttributeError("Account does not exist")
    account_id, username, password, salt = record
    return {'account_id': account_id, 'username': username, 'password': password, 'salt': salt}

def delete_account(pk_name: str, pk):
    """
    if account does not exists, attribute error is raised
    else delete account from account and account_backup
    pk_name can only be "account_id" or "username"
    """
    if account.retrieve(pk, pk_name) is None:
        raise AttributeError("Account does not exist")
    account.delete(pk, pk_name)
    account_backup.delete(pk, pk_name)


# FOR STUDENT TABLE
def create_profile(name, _class, email, account_id):
    """
    if account_id does not exist in account table, attribute error is raised
    else data is inserted into student_profile and student_profile_backup
    """
    if account.retrieve(account_id, "account_id") is None:
        raise AttributeError("Invalid account id")
    student_profile.insert(name, _class, email, account_id)
    student_profile_backup.insert(name, _class, email, account_id)

def update_profile(student_id: int, field: str, data):
    """
    if profile does not exists, attribute error is raised
    if account_id does not exist in account table, attribute error is raised
    else account updated in account and account_backup
    field can only be "account_id", "name", "class" or "email"
    """
    if student_profile.retrieve(student_id) is None:
        raise AttributeError("Student profile does not exist")
    if field == "account_id" and account.retrieve(data, "account_id") is None:
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
    return {'student_id': student_id, 'name': name, 'class': _class, 'email': email, 'account_id': account_id}

def delete_profile(student_id: int):
    """
    if account does not exists, attribute error is raised
    else delete account from student_profile and student_profile_backup
    """
    if student_profile.retrieve(student_id) is None:
        raise AttributeError("Profile does not exist.")
    student_profile.delete(student_id)
    student_profile_backup.delete(student_id)


# FOR CCA TABLE
def create_cca(name: str, type: str):
    """
    if name already exists, attribute error is raised
    type must be of 'sports', 'performing arts', 'uniform group',
    'clubs and societies' or 'others'
    if type is invalid, raise attribute error
    else data is inserted into cca_info and cca_info_backup
    """
    if cca_info.retrieve("name", name) is not None:
        raise AttributeError('Name already exists.')
    if type not in ['sports', 'performing arts', 'uniform group', 'clubs and societies', 'others']:
        raise AttributeError(f'Invalid type {type}')
    cca_info.insert(name, type)
    cca_info_backup.insert(name, type)
    
def update_cca(pk_name: str, pk, field: str, data):
    """
    if name already exists, attribute error is raised
    pk_name can only be "cca_id" or "name"
    if cca does not exists, attribute error is raised
    else cca updated in cca_info and cca_info_backup
    """
    if cca_info.retrieve(pk, pk_name) is None:
        raise AttributeError('CCA record does not exist')
    if pk_name == "name" and cca_info.retrieve("name", pk) is not None:
        raise AttributeError('Name already exists.')
    cca_info.update(pk, pk_name, field, data)
    cca_info_backup.update(pk, pk_name, field, data)
    
def retrieve_cca(pk_name: str, pk) -> dict:
    """
    obtain information for a cca
    if cca does not exists, attribute error is raised
    else a dictionary of cca_id, name, type is returned
    """
    record = cca_info.retrieve(pk, pk_name)
    if record is None:
        raise AttributeError('CCA record does not exist')
    cca_id, name, type = record
    record_dict = {'cca_id': cca_id, 'name': name, 'type': type}
    return record_dict
    
def delete_cca(pk_name: str, pk) -> None:
    """
    if cca does not exists, attribute error is raised
    else delete cca from cca_info and cca_info_backup
    """
    if cca_info.retrieve(pk, pk_name) is None:
        raise AttributeError('CCA record does not exist')
    cca_info.delete(pk, pk_name)
    cca_info_backup.delete(pk, pk_name)
    
# FOR ACTIVITY TABLE
def create_activity(name: str, date: str, location: str, organiser_id: int):
    """
    if organiser_id does not exist in student table, attribute error is raised
    else data is inserted into activity_info and activity_info_backup
    """
    if student_profile.retrieve(organiser_id) is None:
        raise AttributeError('Invalid student id.')
    activity_info.insert(name, date, location, organiser_id)
    activity_info_backup.insert(name, date, location, organiser_id)

def update_activity(activity_id: int, field: str, data):
    """
    if activity does not exists, attribute error is raised
    if organiser_id does not exist in student table, attribute error is raised
    else activity updated in activity_info and activity_info_backup
    """
    if activity_info.retrieve(activity_id) is None:
        raise AttributeError('Activity does not exist.')
    if field == "organiser_id" and student_profile.retrieve(data) is None:
        raise AttributeError('Invalid student id.')
    activity_info.update(activity_id, field, data)
    activity_info_backup.update(activity_id, field, data)

def retrieve_activity(activity_id: int) -> dict:
    """
    retrieve information for an activity
    if activity does not exists, attribute error is raised
    else a dictionary of activity_id, name, date, location, organiser_id is returned
    """
    record = activity_info.retrieve(activity_id)
    if record is None:
        raise AttributeError('Activity does not exist')
    activity_id, name, date, location, organiser_id = record
    return {'activity_id': activity_id, 'name': name, 'date': date, 'location': location, 'organiser_id': organiser_id} 
    
def delete_activity(activity_id: int):
    """
    if activity does not exists, attribute error is raised
    else delete activity from activity_info and activity_info_backup
    """
    if activity_info.retrieve(activity_id) is None:
        raise AttributeError('Activity does not exist')
    activity_info.delete(activity_id)
    activity_info_backup.delete(activity_id)


# FOR STUDENT ACTIVITY
def create_studentactivity(student_id: int, activity_id: int) -> None:
    """
    if student_id does not exist in student table, attribute error is raised
    if activity_id does not exist in activity table, attribute error is raised
    else data is inserted into student_activity and student_activity_backup
    """
    if student_profile.retrieve(student_id) is None:
        raise AttributeError("Invalid student id.")
    if activity_info.retrieve(activity_id) is None:
        raise AttributeError("Invalid activity id.")
    student_activity.insert({"student_id": student_id, "activity_id": activity_id})
    student_activity_backup.insert({"student_id": student_id, "activity_id": activity_id})

def retrieve_studentactivity(pk_name: str, pk: int) -> list[tuple]:
    """
    obtain information for an student activity
    if combination with the pk does not exists, attribute error is raised
    else a list of tuple of (student_id, activity_id) is returned
    """
    record = student_activity.retrieve_all(pk, pk_name)
    if record is None:
        raise AttributeError(f"No record for this {pk_name}.")
    return record

def delete_studentactivity(student_id: int, activity_id: int) -> None:
    """
    if student-activity combination does not exists, attribute error is raised
    else delete account from student_activity and student_activity_backup
    """
    record = student_activity.retrieve_all("student_id", student_id)
    if record is None:
        raise AttributeError("Student activity does not exist.")
    exists = False
    index = 0
    while not exists:
        if index >= len(record):
            raise AttributeError("Student activity does not exist.")
        _student_id, _activity_id = record[index]
        if activity_id == _activity_id:
            exists = True
        index += 1
    student_activity.delete(student_id, activity_id)
    student_activity_backup.delete(student_id, activity_id)


# FOR STUDENT CCA 
def create_studentcca(student_id: int, cca_id: int, role: str):
    """
    if student_id does not exist in student table, attribute error is raised
    if cca_id does not exist in cca table, attribute error is raised
    else data is inserted into student_cca and student_cca_backup
    """
    if student_profile.retrieve(student_id) is None:
        raise AttributeError("Invalid student id.")
    if cca_info.retrieve(cca_id) is None:
        raise AttributeError("Invalid cca id.")
    student_cca.insert(student_id, cca_id, role)
    student_cca_backup.insert(student_id, cca_id, role)

def update_studentcca(student_id: int, cca_id: int, new: str):
    """
    if student-cca combination does not exists, attribute error is raised
    else student cca updated in student_cca and student_cca_backup
    """
    if student_cca.retrieve_one(student_id, cca_id) is None:
        raise AttributeError("Student-cca combination does not exist.")
    student_cca.update(student_id, cca_id, new)
    student_cca_backup.update(student_id, cca_id, new)

def retrieve_one_studentcca(student_id: int, cca_id: int) -> dict:
    """
    obtain information for a student cca record
    if student-cca combination does not exists, attribute error is raised
    else a dict of student_id, cca_id, role is returned
    """
    record = student_cca.retrieve_one(student_id, cca_id)
    if record is None:
        raise AttributeError("Student-cca combination does not exist.")
    student_id, cca_id, role = record
    return {"student_id": student_id, "cca_id": cca_id, "role": role}

def retrieve_all_studentcca(pk_name: str, pk: int) -> list[tuple]:
    """
    obtain information for multiple student cca records
    if combination with the pk does not exists, attribute error is raised
    else a list of tuple of (student_id, cca_id) is returned
    """
    record = student_cca.retrieve_all(pk, pk_name)
    if record is None:
        raise AttributeError(f"No record for this {pk_name}.")
    return record

def delete_studentcca(student_id: int, cca_id: int):
    """
    if student-cca combination does not exists, attribute error is raised
    else delete account from student_cca and student_cca_backup
    """
    if student_cca.retrieve_one(student_id, cca_id) is None:
        raise AttributeError("Student-cca combination does not exist.")
    student_cca.delete(student_id, cca_id)
    student_cca_backup.delete(student_id, cca_id)