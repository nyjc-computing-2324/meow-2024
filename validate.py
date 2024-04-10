import string

def username_isvalid(username) -> bool:
    """
    xinyu
    checks username during registration for these criteria:
    1. all char are ascii printable char
    """
    return all(char in string.printable for char in username)


def password_isvalid(password) -> bool:
    """
    xinyu
    checks password during registration for these criteria:
    1. all char are ascii printable char except tab
    2. at least 8 char, 1 upper, 1 lower, 1 number
    """
    if not all(char in string.printable for char in password):
        return False
    
    if not len(password) >= 8:
        return False
        
    if not any(char in string.ascii_lowercase for char in password):
        return False

    if not any(char in string.ascii_uppercase for char in password):
        return False
        
    if not any(char in string.digits for char in password):
        return False

    if "    " in password:
        return False
        
    return True