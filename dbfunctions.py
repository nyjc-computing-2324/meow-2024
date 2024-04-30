from database import Account, Student, CCA, Activity, StudentActivity, StudentCCA, init_tables
import auth
import os
import psycopg2
import sqlite3

def sqlite_conn(uri):
    """establish a connection with sqlite"""
    return sqlite3.connect(uri)

def postgres_conn(uri):
    """establish a connection with postgres"""
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

def get_student_activity(env: str = "") -> StudentActivity:
    """returns an instance of StudentActivity with an appropriate db conn"""
    uri = get_uri(env)
    return StudentActivity(conn_factory(env, uri))

def get_student_cca(env: str = "") -> StudentCCA:
    """returns an instance of StudentCCA with an appropriate db conn"""
    uri = get_uri(env)
    return StudentCCA(conn_factory(env, uri))

# instantiating table objects
account = get_account()
student = get_student()
cca = get_cca()
activity = get_activity()
student_activity = get_student_activity()
student_cca = get_student_cca()

# FOR ACCOUNT TABLE
def create_account(username: str, password: str) -> None:
    """
    if username already exists, attribute error is raised
    else data is inserted into account table
    """
    # check for repeated username
    if account.retrieve_primary_key(username) is not None:
        raise AttributeError("Username already exists")
    password, salt = auth.create_hash(password)
    account.insert({'username': username, 'password': password, 'salt': salt})

def login(username: str , password: str) -> bool:
    # checks for valid username and password is already done 
    account_id = account.retrieve_primary_key(username)
    # account not found
    if account_id is None:
        return False
    data = account.retrieve(account_id)

    account_id, database_username, database_password, salt = data
    # salting and hashing of password implemented 
    return auth.check_password(password, database_password, salt)

def username_taken(username: str) -> bool:
    """checks if the username is already in use"""
    account_id = account.retrieve_primary_key(username)
    if account_id is None:
        return True
    return False

def update_account(username: str, field: str, data) -> None:
    """
    if username does not exist in account table, attribute error is raised
    if new username given already exists, attribute error is raised
    else account updated in account table
    field can only be "username", "password" or "salt"
    """
    account_id = account.retrieve_primary_key(username)
    if account_id is None:
        raise AttributeError("No account linked to username")
    if field == "username" and username_taken(data):
        raise AttributeError("Username already exist")
    account.update(account_id, field, data)

def retrieve_account(username: str) -> dict:
    """
    retrieve information for an account
    if username does not exist in account table, attribute error is raised
    else a dictionary of account_id, username, password, salt is returned
    """
    account_id = account.retrieve_primary_key(username)
    if account_id is None:
        raise AttributeError("No account linked to username")
    record = account.retrieve(account_id)
    account_id, database_username, password, salt = record
    return {'account_id': account_id, 'username': database_username, 'password': password, 'salt': salt}

def delete_account(username) -> None:
    """
    if username does not exist in account table, attribute error is raised
    else delete account from account table
    """
    account_id = account.retrieve_primary_key(username)
    if account_id is None:
        raise AttributeError("No account linked to username")
    account.delete(account_id)


# FOR STUDENT TABLE
def create_profile(name, _class, email, number, about, username) -> None:
    """
    if account_id does not exist in account table, attribute error is raised
    if username already exists as a foreign key in student table,
    attribute error is raised
    else data is inserted into student table
    """
    account_id = account.retrieve_primary_key(username)
    if account_id is None:
        raise AttributeError("No account linked to username")
    if student.retrieve_primary_key(account_id) is not None:
        raise AttributeError("Username already exists as a foriegn key in student table")
    student.insert({'name': name, 'class': _class, 'email': email, 'number': number, 'about': about, 'account_id': account_id})

def update_profile(username: str, field: str, data) -> None:
    """
    if profile does not exists in student table, attribute error is raised
    if username does not exist in account table, attribute error is raised
    if new username does not exist in account table for updates to account_id,
    attribute error is raised
    if new username already exists as a foreign key in student table,
    attribute error is raised
    else profile updated in student table
    field can only be "account_id", "name", "class" or "email"
    if field is account_id, pass in new username as data
    """
    account_id = account.retrieve_primary_key(username)
    if account_id is None:
        raise AttributeError("No account linked to username")
    student_id = student.retrieve_primary_key(account_id)
    if student_id is None:
        raise AttributeError("Student profile does not exist")
    
    if field == "account_id":
        new_account_id = account.retrieve_primary_key(data)
        if new_account_id is None:
            raise AttributeError("No account linked to new username")
        if student.retrieve_primary_key(new_account_id) is not None:
            raise AttributeError("Username already exists as a foriegn key in student table")

    print(student_id, field, data)
    student.update(student_id, field, data)

def retrieve_profile(username: str) -> dict:
    """
    retrieve information for an account
    if profile does not exists in student table, attribute error is raised
    if username does not exist in account table, attribute error is raised
    else a dictionary of student_id, name, class, email, account_id is returned
    """
    account_id = account.retrieve_primary_key(username)
    if account_id is None:
        raise AttributeError("No account linked to username")
    student_id = student.retrieve_primary_key(account_id)
    if student_id is None:
        raise AttributeError("Student profile does not exist")
    record = student.retrieve(student_id)
    student_id, name, _class, email, account_id, number, about = record
    return {'student_id': student_id, 'name': name, 'class': _class, 'email': email, 'number': number, 'about': about, 'account_id': account_id, 'username': username}

def delete_profile(username: str) -> None:
    """
    if profile does not exists in student table, attribute error is raised
    if username does not exist in account table, attribute error is raised
    else delete profile from student table
    """
    account_id = account.retrieve_primary_key(username)
    if account_id is None:
        raise AttributeError("No account linked to username")
    student_id = student.retrieve_primary_key(account_id)
    if student_id is None:
        raise AttributeError("Student profile does not exist")
    student.delete(student_id)


# FOR CCA TABLE
def create_cca(name: str, type: str) -> None:
    """
    if name already exists in cca table, attribute error is raised
    type must be of 'sports', 'performing arts', 'uniform group',
    'clubs and societies' or 'others'
    if type is invalid, attribute error is raised
    else data is inserted into cca table
    """
    if cca.retrieve_primary_key(name) is not None:
        raise AttributeError("Name already exists")
    if type not in ['sports', 'performing arts', 'uniform group', 'clubs and societies', 'others']:
        raise AttributeError(f'Invalid type {type}')
    cca.insert({'name': name, 'type': type})

def update_cca(name: str, field: str, data) -> None:
    """
    if cca does not exists in cca table, attribute error is raised
    if new username given already exists, attribute error is raised
    else cca updated in cca table
    field can only be "username", "password" or "salt"
    """
    cca_id = cca.retrieve_primary_key(name)
    if cca_id is None:
        raise AttributeError("No info linked to name")
    if field == "name" and cca.retrieve_primary_key(data):
        raise AttributeError("Name already exist")
    cca.update(cca_id, field, data)

def retrieve_cca(name: str) -> dict:
    """
    retrieve information for a cca
    if cca does not exists in cca table, attribute error is raised
    else a dictionary of cca_id, name, type is returned
    """
    cca_id = cca.retrieve_primary_key(name)
    if cca_id is None:
        raise AttributeError("No info linked to name")
    record = cca.retrieve(cca_id)
    cca_id, name, type = record
    return {'cca_id': cca_id, 'name': name, 'type': type}

def delete_cca(name: str) -> None:
    """
    if cca does not exists in cca table, attribute error is raised
    else delete cca from cca table
    """
    cca_id = cca.retrieve_primary_key(name)
    if cca_id is None:
        raise AttributeError("No info linked to name")
    cca.delete(cca_id)
    
# FOR ACTIVITY TABLE
def create_activity(name: str, date: str, location: str, username: str) -> None:
    """
    if organiser_id(username) does not exist in student table, attribute error is raised
    if username already exists as a foreign key in activity table,
    attribute error is raised
    else data is inserted into activity table
    """
    account_id = account.retrieve_primary_key(username)
    if account_id is None:
        raise AttributeError("No account linked to username")
    organiser_id = student.retrieve_primary_key(account_id)
    if organiser_id is None:
        raise AttributeError("Student profile does not exist")
    if activity.retrieve_primary_key(account_id) is not None:
        raise AttributeError("Username already exists as a foriegn key in activity table")
    activity.insert({'name': name, 'date': date, 'location': location, 'organiser_id': organiser_id})

def update_activity(name: str, field: str, data) -> None:
    """
    if activity does not exists in activity table, attribute error is raised
    
    if new name given already exists, attribute error is raised
    
    if new username does not exist in account table for updates to account_id,
    attribute error is raised
    if profile does not exist for new username in student table for updates to 
    account_id, attribute error is raised
    if new username already exists as a foreign key in activity table,
    attribute error is raised
    
    else activity updated in activity table
    field can only be "name", "type" or "organiser_id"
    if field is organiser_id, pass in new username as data
    """
    activity_id = activity.retrieve_primary_key(name)
    if activity_id is None:
        raise AttributeError("No activity linked to name")
        
    if field == "name" and activity.retrieve_primary_key(data) is not None:
        raise AttributeError("Username already exists")
    
    if field == "organiser_id":
        new_account_id = student.retrieve_primary_key(data)
        if new_account_id is None:
            raise AttributeError("No account linked to new username")
        new_organiser_id = student.retrieve_primary_key(new_account_id)
        if new_organiser_id is None:
            raise AttributeError("Student profile does not exist for new username")
        if activity.retrieve_primary_key(new_organiser_id) is not None:
            raise AttributeError("Username already exists as a foriegn key in avtivity table")
    activity.update(activity_id, field, data)

def retrieve_activity(name: str) -> dict:
    """
    retrieve information for an activity
    if activity does not exist in activity table, attribute error is raised
    else a dictionary of activity_id, name, date, location, organiser_id is returned
    """
    activity_id = activity.retrieve_primary_key(name)
    if activity_id is None:
        raise AttributeError("No activity linked to name")
    record = activity.retrieve(activity_id)
    activity_id, name, date, location, organiser_id = record
    return {'activity_id': activity_id, 'name': name, 'date': date, 'location': location, 'organiser_id': organiser_id} 

def delete_activity(name: str) -> None:
    """
    if activity does not exists, attribute error is raised
    else delete activity from activity_info and activity_info_backup
    """
    activity_id = activity.retrieve_primary_key(name)
    if activity_id is None:
        raise AttributeError('Activity does not exist')
    activity.delete(activity_id)


# FOR STUDENT ACTIVITY - TO UPDATE DELETE AND CREATE NEW RECORD
def create_studentactivity(username: str, activity_name: str) -> None:
    """
    if profile does not exists in student table, attribute error is raised
    if username does not exist in account table, attribute error is raised
    if activity does not exists in activity table, attribute error is raised
    else data is inserted into student_activity table
    """
    account_id = account.retrieve_primary_key(username)
    if account_id is None:
        raise AttributeError("No account linked to username")
    student_id = student.retrieve_primary_key(account_id)
    if student_id is None:
        raise AttributeError("Student profile does not exist")

    activity_id = activity.retrieve_primary_key(activity_name)
    if activity_id is None:
        raise AttributeError("No activity linked to name")

    student_activity.insert({"student_id": student_id, "activity_id": activity_id})

def retrieve_studentactivity(field: str, unique_field) -> list[list[dict]]:
    """
    retrieve information for all student activity regarding the student or activity
    field can only be "name" or "username" representing activity and student respectively
    
    if profile does not exists in student table, attribute error is raised
    if username does not exist in account table, attribute error is raised
    if activity does not exists in activity table, attribute error is raised
    
    else a list of list of dictionary is returned
    [[{student data}, {activity data}], [{student data}, {activity data}], ...]
    """
    if field.lower() == "name": 
        activity_id = activity.retrieve_primary_key(unique_field)
        if activity_id is None:
            raise AttributeError("No activity linked to name")
        records = student_activity.retrieve_all("activity_id", activity_id)
        
    elif field.lower() == "username":
        account_id = account.retrieve_primary_key(unique_field)
        if account_id is None:
            raise AttributeError("No account linked to username")
        student_id = student.retrieve_primary_key(account_id)
        if student_id is None:
            raise AttributeError("Student profile does not exist")
        records = student_activity.retrieve_all("account_id", account_id)

    else:
        raise AttributeError(f"Invalid field {field}")
        
    if records is None:
        raise AttributeError(f"No record for field {field}.")
    new_record = []
    for record in records:
        student_id, activity_id = record
        new_record.append([student.retrieve(student_id), activity.retrieve(activity_id)])
    return new_record

def delete_studentactivity(username: str, activity_name: str) -> None:
    """
    if profile does not exists in student table, attribute error is raised
    if username does not exist in account table, attribute error is raised
    if activity does not exists in activity table, attribute error is raised
    if student-activity combination does not exists, attribute error is raised
    else delete account from student_activity table
    """
    account_id = account.retrieve_primary_key(username)
    if account_id is None:
        raise AttributeError("No account linked to username")
    student_id = student.retrieve_primary_key(account_id)
    if student_id is None:
        raise AttributeError("Student profile does not exist")

    activity_id = activity.retrieve_primary_key(activity_name)
    if activity_id is None:
        raise AttributeError("No activity linked to name")
    
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


# FOR STUDENT CCA 
def create_studentcca(username: str, cca_name: str, role: str):
    """
    if profile does not exists in student table, attribute error is raised
    if username does not exist in account table, attribute error is raised
    if cca does not exist in cca table, attribute error is raised
    else data is inserted into student_cca table
    """
    account_id = account.retrieve_primary_key(username)
    if account_id is None:
        raise AttributeError("No account linked to username")
    student_id = student.retrieve_primary_key(account_id)
    if student_id is None:
        raise AttributeError("Student profile does not exist")

    cca_id = cca.retrieve_primary_key(cca_name)
    if cca_id is None:
        raise AttributeError("No cca linked to name")
        
    student_cca.insert({'student_id': student_id, 'cca_id': cca_id, 'role': role})
    
def update_studentcca(username: str, cca_name: str, new_role: str):
    """
    if profile does not exists in student table, attribute error is raised
    if username does not exist in account table, attribute error is raised
    if cca does not exist in cca table, attribute error is raised
    if student-cca combination does not exist in studentcca table, 
    attribute error is raised
    else role updated in student_cca table
    """
    account_id = account.retrieve_primary_key(username)
    if account_id is None:
        raise AttributeError("No account linked to username")
    student_id = student.retrieve_primary_key(account_id)
    if student_id is None:
        raise AttributeError("Student profile does not exist")

    cca_id = cca.retrieve_primary_key(cca_name)
    if cca_id is None:
        raise AttributeError("No cca linked to name")

    if student_cca.retrieve_one(student_id, cca_id) is None:
        raise AttributeError("Student-cca combination does not exist.")
    
    student_cca.update(student_id, cca_id, new_role)

def retrieve_one_studentcca(username: str, cca_name: str) -> dict:
    """
    retrieve information for a student cca record
    
    if profile does not exists in student table, attribute error is raised
    if username does not exist in account table, attribute error is raised
    if cca does not exist in cca table, attribute error is raised
    if student-cca combination does not exist in studentcca table, 
    attribute error is raised
    
    else a dict of student_id, cca_id, role is returned
    """
    account_id = account.retrieve_primary_key(username)
    if account_id is None:
        raise AttributeError("No account linked to username")
    student_id = student.retrieve_primary_key(account_id)
    if student_id is None:
        raise AttributeError("Student profile does not exist")

    cca_id = cca.retrieve_primary_key(cca_name)
    if cca_id is None:
        raise AttributeError("No cca linked to name")

    record = student_cca.retrieve_one(student_id, cca_id)
    if record is None:
        raise AttributeError("Student-cca combination does not exist.")
    student_id, cca_id, role = record
    return {"student_id": student_id, "cca_id": cca_id, "role": role}

def retrieve_all_studentcca(field: str, unique_field) -> list[list[dict]]:
    """
    obtain information for all student cca regarding the student or cca
    field can only be "name" or "username" representing cca or student respectively
    
    if profile does not exists in student table, attribute error is raised
    if username does not exist in account table, attribute error is raised
    if cca does not exist in cca table, attribute error is raised
    if student-cca combination does not exist in studentcca table, 
    attribute error is raised
    
    else a list of list of dictionary is returned
    [[{student data}, {cca data}], [{student data}, {cca data}], ...]
    """
    if field.lower() == "name": 
        cca_id = cca.retrieve_primary_key(unique_field)
        if cca_id is None:
            raise AttributeError("No activity linked to name")
        records = student_cca.retrieve_all("cca_id", cca_id)

    elif field.lower() == "username":
        account_id = account.retrieve_primary_key(unique_field)
        if account_id is None:
            raise AttributeError("No account linked to username")
        student_id = student.retrieve_primary_key(account_id)
        if student_id is None:
            raise AttributeError("Student profile does not exist")
        records = student_activity.retrieve_all("account_id", account_id)

    else:
        raise AttributeError(f"Invalid field {field}")

    if records is None:
        raise AttributeError(f"No record for field {field}.")
    new_record = []
    for record in records:
        student_id, cca_id = record
        new_record.append([student.retrieve(student_id), cca.retrieve(cca_id)])
    return new_record

def delete_studentcca(username: str, cca_name: str) -> None:
    """
    if profile does not exists in student table, attribute error is raised
    if username does not exist in account table, attribute error is raised
    if cca does not exist in cca table, attribute error is raised
    if student-cca combination does not exist in studentcca table, 
    attribute error is raised
    else delete account from student_cca table
    """
    account_id = account.retrieve_primary_key(username)
    if account_id is None:
        raise AttributeError("No account linked to username")
    student_id = student.retrieve_primary_key(account_id)
    if student_id is None:
        raise AttributeError("Student profile does not exist")

    cca_id = cca.retrieve_primary_key(cca_name)
    if cca_id is None:
        raise AttributeError("No cca linked to name")
        
    if student_cca.retrieve_one(student_id, cca_id) is None:
        raise AttributeError("Student-cca combination does not exist.")
        
    student_cca.delete(student_id, cca_id)