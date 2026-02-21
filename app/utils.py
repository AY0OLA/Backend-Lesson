from pwdlib import PasswordHash

passwords = PasswordHash.recommended()

def hash(password: str):
    return passwords.hash(password)

def verify(plain_password: str, hashed_password: str):
    return passwords.verify(plain_password, hashed_password)