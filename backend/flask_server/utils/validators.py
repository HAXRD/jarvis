import re

def validate_email(email):
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(email_pattern, email))

def validate_password(password):
    # At least 8 characters, with letters and numbers
    return len(password) >= 8 and re.search(r"[A-Za-z]", password) and re.search(r"[0-9]", password)