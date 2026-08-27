import jwt
from datetime import datetime, timedelta, timezone
from jwt import InvalidTokenError
import os
from dotenv import load_dotenv
from . import schemas
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
expiration_token_time = 30

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expiration_token_time)
    to_encode.update({"exp":expire})
    encoded_token = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM )
    return encoded_token
    

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("id")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id = str(id))
    except InvalidTokenError:
        raise credentials_exception
    return token_data


def get_current_user(token:str = Depends(oauth2_scheme )):
    credentials_exception = HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Not Authenticated", headers={"WWW-AUTHENTICATE":"Bearer"})
    return verify_access_token(token, credentials_exception)