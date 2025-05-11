from typing import Annotated
from fastapi import Depends, status
import jwt
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.model_functions.login import get_emp_for_login
from app.exception.custom_exception import CustomException
from fastapi import HTTPException, Response, Request
from app.core.hashing import HashData
from app.config.message import auth_message
from app.core.token import blacklist
from app.validation.emp_m import EmpSchemaOut
from app.validation.auth import TokenData
from app.config.loadenv import envconst
from app.core.httpbearer import get_api_token

def authenticate(email,password,db):
    dbempm = get_emp_for_login(db,email)
    if not dbempm:
        raise CustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            status=False,
            message=auth_message.INCORRECT_CREDENTIALS,
            data=[]
        )
        
    if not HashData.verify_password(password, dbempm.password):
        raise CustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            status=False,
            message=auth_message.INCORRECT_CREDENTIALS,
            data=[]
        )   
    return dbempm

async def getCurrentEmp(token: Annotated[str, Depends(get_api_token)], db: Annotated[Session, Depends(get_db)]):
    if token in blacklist:
        raise CustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            status=False,
            message=auth_message.LOGIN_REQUIRED,
            data=[]
        )
    else:
        payload = jwt.decode(token, envconst.SECRET_KEY, algorithms=[envconst.ALGORITHM])
        email: str = payload.get("email")
        token_data = TokenData(email=email)
        currentEmp = get_emp_for_login(db, email=token_data.email)
        return currentEmp

async def getCurrentActiveEmp(
    currentEmp: Annotated[EmpSchemaOut, Depends(getCurrentEmp)],
):
    if(currentEmp.status == 0):
        raise CustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            status=False,
            message=auth_message.LOGIN_REQUIRED,
            data=[]
        )
    return currentEmp