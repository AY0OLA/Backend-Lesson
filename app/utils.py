from pwdlib import PasswordHash

passwords = PasswordHash.recommended()

def hash(password: str):
    return passwords.hash(password)