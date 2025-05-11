from datetime import datetime, timedelta, timezone
from datetime import timedelta
from typing import Optional
from app.config.loadenv import envconst
import jwt

blacklist = set()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, envconst.SECRET_KEY, algorithm=envconst.ALGORITHM)
    return encoded_jwt