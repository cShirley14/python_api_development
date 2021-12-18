from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta

from sqlalchemy.orm.session import Session

from app import models
from app.config import Settings
from . import schemas, database
from fastapi.security import OAuth2PasswordBearer

# SECRET_KEY
# Algorithm
# Expiry Time

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

settings = Settings()

# if settings.secret_key == None or settings.algorithm == None or settings.expiry_time == None:
#     with open('config.yaml', 'r') as file:
#         raw_yml = yaml.load(file, Loader=yaml.SafeLoader)
#         SECRET_KEY = raw_yml["secretkey"]
#         ALGORITHM = raw_yml["algorithm"]
#         ACCESS_TOKEN_EXPIRE_MINUTES = raw_yml["tokenexpiry"]

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=settings.expiry_time)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")
        
        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user

