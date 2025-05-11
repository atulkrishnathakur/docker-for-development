'''
from fastapi.security import APIKeyHeader
from fastapi import Security
from passlib.context import CryptContext
from config.logconfig import loglogger
from config.loadenv import envconst
from fastapi import Depends, status
from config.message import auth_message
from exception.custom_exception import CustomException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# https://fastapi.tiangolo.com/tutorial/header-params/#declare-header-parameters

header_scheme = APIKeyHeader(name=envconst.API_KEY_HEADER_NAME)

async def get_api_key(api_key: str = Security(header_scheme)):
    if not api_key:
        raise CustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            status=False,
            message=auth_message.INCORRECT_CREDENTIALS,
            data=[]
        )
    return api_key

'''