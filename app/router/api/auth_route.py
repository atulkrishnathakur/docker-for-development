from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, FastAPI, status, Request, BackgroundTasks
from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.validation.auth import (AuthCredentialIn,AuthOut, Logout,Status422Response,Status400Response,Status401Response)
from fastapi.responses import JSONResponse, ORJSONResponse
from app.database.session import get_db
from app.config.logconfig import loglogger
from app.core.auth import authenticate
from app.core.token import create_access_token
from app.config.loadenv import envconst
from app.config.message import auth_message
from app.validation.email import EmailSchema
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig,MessageType
from app.config.fastapi_mail_config import send_email, mailconf

router = APIRouter()

@router.post(
    "/login",
    response_model=AuthOut,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": Status422Response},
        status.HTTP_400_BAD_REQUEST: {"model": Status400Response},
        status.HTTP_401_UNAUTHORIZED: {"model": Status401Response}
    },
    name="login"
    )

async def login(
    background_tasks: BackgroundTasks,
    credentials:AuthCredentialIn,
    db:Session = Depends(get_db)
    ):
    AuthCredentialIn.check_email_exist(db,credentials.email)
    authemp = authenticate(credentials.email, credentials.password, db)
    try:
        access_token_expires = timedelta(minutes=int(envconst.ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = create_access_token(
        data={"email": authemp.email}, expires_delta=access_token_expires
    )
        http_status_code = status.HTTP_200_OK
        datalist = list()
        datadict = {}
        datadict['id'] = authemp.id
        datadict['emp_name'] = authemp.emp_name
        datadict['email'] = authemp.email
        datadict['status'] = authemp.status
        datadict['mobile'] = authemp.mobile
        datalist.append(datadict)
        response_dict = {
            "status_code": http_status_code,
            "status":True,
            "message":auth_message.AUTH_SUCCESSFULL,
            "token_type":envconst.TOKEN_TYPE,
            "access_token":access_token,
            "data":datalist
        }
        response_data = AuthOut(**response_dict) 
        response = JSONResponse(content=response_data.dict(),status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(response_data.dict()))

        body = """<h1>Your have successfully Test</h1> """
        subject = "Your have successfully login"
        toemail = [authemp.email]
        ccemail = ['atulcc@yopmail.com']
        bccemail = ['atulbcc@yopmail.com']
        emailBody = body
        send_email(background_tasks=background_tasks,emaiSubject=subject,emailTo=toemail,emailBody=emailBody,ccemail=ccemail,bccemail=bccemail)
        return response
    except Exception as e:
        http_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        data = {
            "status_code": http_status_code,
            "status":False,
            "message":"Type:"+str(type(e))+", Message:"+str(e)
        }
        response = JSONResponse(content=data,status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(data))
        return response