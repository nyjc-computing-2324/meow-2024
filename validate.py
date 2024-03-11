def username_isvalid(username) -> bool:
    """
    checks username during registration for these criteria:
    1. tbc
    """
    raise NotImplementedError

def password_isvalid(username) -> bool:
    """
    checks password during registration for these criteria:
    1. tbc
    """
    raise NotImplementedError

def user_isvalid(username, password) -> bool:
    """
    checks if the username and password corresponds to a user in the 
    database, return False if it doesn't, otherwise return True
    """
    raise NotImplementedError