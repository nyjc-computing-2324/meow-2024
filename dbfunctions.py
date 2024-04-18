from database import Account, Student, CCA, Activity, StudentActivity, StudentCCA
import auth

# instantiating table objects
student_account = Account("meow.db")
student_account_backup = Account("backup.db")
student_account_testing = Account("test.db")

student_profile = Student('meow.db')
student_profile_backup = Student('backup.db')
student_profile_testing = Student('test.db')

cca_info = CCA("meow.db")
cca_info_backup = CCA("backup.db")
cca_info_testing = CCA("test.db")

activity_info = Activity("meow.db")
activity_info_backup = Activity("backup.db")
activity_info_testing = Activity("test.db")

student_activity = StudentActivity('meow.db')
student_activity_backup = StudentActivity('backup.db')
student_activity_testing = StudentActivity('test.db')

student_cca = StudentCCA('meow.db')
student_cca_backup = StudentCCA('backup.db')
student_cca_testing = StudentCCA('test.db')

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


# FOR CCA TABLE
def create_cca(name: str, type: str):
    """
    data is inserted into cca_info and cca_info_backup
    """
    cca_info.insert(name, type)
    cca_info_backup.insert(name, type)

def update_cca(cca_id: int, field: str, data):
    """
    """
    if cca_info.retrieve(cca_id) is None:
        raise AttributeError('CCA does not exist')
    cca_info.update(cca_id, field, data)
    cca_info_backup.update(cca_id, field, data)
    
def retrieve_cca(cca_id: int):
    """
    """
    if cca_info.retrieve(cca_id) is None:
        raise AttributeError('CCA does not exist')
    record = cca_info.retrieve(cca_id)
    cca_id, name, type = record
    record_dict = {'cca_id': cca_id, 'name': name, 'type': type}
    return record_dict
    

    

def delete_cca(cca_id: int):
    """
    """
    if cca_info.retrieve(cca_id) is None:
        raise AttributeError('CCA does not exist')
    cca_info.delete(cca_id)
    cca_info_backup.delete(cca_id)
    

# FOR ACTIVITY TABLE
def create_activity():
    pass

def update_activity():
    pass

def retrieve_activity():
    pass

def delete_activity():
    pass

# FOR STUDENT ACTIVITY
def create_studentactivity(student_id: int, activity_id: int):
    if student_profile.retrieve("student_id", student_id) is None:
        raise AttributeError("Invalid student id")
    if activity_info.retrieve("activity_id", activity_id) is None:
        raise AttributeError("Invalid activity id")
    student_activity.insert(student_id, activity_id)
    student_activity_backup.insert(student_id, activity_id)

def retrieve_studentactivity(pk_name: str, pk: int):
    pass

def delete_studentactivity(student_id: int, activity_id: int):
    pass

# FOR STUDENT CCA 
def create_studentcca(student_id: int, cca_id: int, role: str):
    if student_profile.retrieve("student_id", student_id) is None:
        raise AttributeError("Invalid student id")
    if cca_info.retrieve("cca_id", cca_id) is None:
        raise AttributeError("Invalid cca id")
    student_cca.insert(student_id, cca_id, role)
    student_cca_backup.insert(student_id, cca_id, role)

def update_studentcca(student_id: int, cca_id: int, new: str):
    pass

def retrieve_studentcca(pk_name: int, pk: int):
    pass

def delete_studentcca(student_id: int, cca_id: int):