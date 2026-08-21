from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()

def hashpass(password:str):
    return pwd_context.hash(password)

def hashverify(input_password:str, hashed_password:str):
    return pwd_context.verify(input_password, hashed_password)