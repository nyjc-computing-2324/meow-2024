from database import Account
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

