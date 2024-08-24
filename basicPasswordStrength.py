import re

def check_password_strength(password):
    
    if len(password) < 8:
        return "Weak password: Less than 8 characters."

    if not re.search(r'\d', password):
        return "Please use digits in your password."

    if not re.search(r'[A-Z]', password):
        return "Please use both lowercase and upper characters in your password."

    if not re.search(r'[a-z]', password):
        return "Please use both lowercase and upper characters in your password.."

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Please use special characters in your password."

    return "Strong password."

password = input("Enter a password to check its strength: ")
print(check_password_strength(password))
