from database import Account, Student
import auth

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

def retrieve_account(field: str, data: str) -> tuple:
    """
    xinyu
    check if account exists
    if false raise attribute error
    if true return a dictionary of account_id, username, password, salt
    """
    record = student_account.retrieve(field, data)
    if record is None:
        raise AttributeError("Account does not exist.")
    account_id, username, password, salt = record
    record_dict = {'account_id': account_id, 'username': username, 'password': password, 'salt': salt}
    return record_dict
    

def delete_account(field: str, data: str):
    """
    xinyu
    check if account exists
    if false raise attribute error
    if true delete account from student_account and student_account_backup
    """
    if student_account.retrieve("username", username) is None:
        raise AttributeError("Account does not exist.")
    student_account.delete(field, data)
    student_account_backup.delete(field, data)

def login(username: str , password: str) -> bool:
    # checks for valid username and password is already done 

    data = student_account.retrieve("username", username)
    # account not found
    if data is None:
        return False

    account_id, database_username, database_password, database_salt = data
    # salting and hashing of password implemented 
    return auth.check_password(password, database_password, database_salt)

# instantiating table objects
student_profile = Student('meow.db')
student_profile_backup = Student('backup.db')

def create_profile(name, _class, email, account_id):
    """
    insert date into student_profile and student_profile_backup
    """
    student_profile.insert(name, _class, email, account_id)
    student_profile_backup.insert(name, _class, email, account_id)

def retrieve_profile(student_id: str):
    """
    check if profile exist using student_id
    if false raise attribute error
    if true return profile in dict
    """
    record = student_profile.retrieve(student_id)
    if record is None:
        raise AttributeError("Profile does not exist.")
    student_id, name, _class, email, account_id = record
    record_dict = {'student_id': student_id, 'name': name, 'class': _class, 'email': email, 'account_id': account_id}
    return record_dict

def delete_profile(student_id: str):
    """
    check if profile exist using student_id
    if false raise attribute error
    if true delete profile from student_profile and student_profile_backup
    """
    if student_profile.retrieve(student_id) is None:
        raise AttributeError("Profile does not exist.")
    student_profile.delete(student_id)
    student_profile_backup.delete(student_id)