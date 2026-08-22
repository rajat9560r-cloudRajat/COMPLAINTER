import jwt
from datetime import datetime, timedelta
from jwt import InvalidTokenError
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
expiration_token_time = 30

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=expiration_token_time)
    to_encode.update({"exp":expire})
    encoded_token = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM )
    return encoded_token
    




