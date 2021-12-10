from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer

import yaml

# SECRET_KEY
# Algorithm
# Expiry Time

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

with open('config.yaml', 'r') as file:
    raw_yml = yaml.load(file, Loader=yaml.SafeLoader)
    SECRET_KEY = raw_yml["secretkey"]
    ALGORITHM = raw_yml["algorithm"]
    ACCESS_TOKEN_EXPIRE_MINUTES = raw_yml["tokenexpiry"]

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("users_id")
        
        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
