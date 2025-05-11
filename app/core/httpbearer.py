from fastapi import Security
from app.config.logconfig import loglogger
from app.config.loadenv import envconst
from fastapi import Depends, status
from app.config.message import auth_message
from app.exception.custom_exception import CustomException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated

# https://fastapi.tiangolo.com/reference/security/#fastapi.security.HTTPBearer

http_bearer = HTTPBearer() 
async def get_api_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]):
    api_key = credentials.credentials
    if not api_key:
        raise CustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            status=False,
            message=auth_message.INCORRECT_CREDENTIALS,
            data=[]
        )
    return api_key