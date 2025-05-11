from pydantic import (BaseModel,Field, model_validator, EmailStr, ModelWrapValidatorHandler, ValidationError, AfterValidator,BeforeValidator,PlainValidator, ValidatorFunctionWrapHandler)
from typing import List
from app.exception.custom_exception import CustomException
from fastapi import status,Depends
from app.config.constants import constants
from typing_extensions import Annotated
from app.database.model_functions import emp_m
from app.config.message import auth_message

class AuthCredentialIn(BaseModel):
    email:str = Field(example="hhjjj@yyeyeyeywww.com")
    password: str = Field(example="aa")

    def check_email_exist(db,email):
        if(not email):
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status=constants.STATUS_BAD_REQUEST,
                message="Email Required",
                data=[]
            )

        empmObj = emp_m.get_data_by_email(db,email)
        if(empmObj is None):
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status=constants.STATUS_BAD_REQUEST,
                message=auth_message.EMAIL_NOT_EXIST,
                data=[]
            )

def dataResponseStatusChecker(value: int)-> int:
    # https://docs.pydantic.dev/latest/concepts/validators/
    if value != 0 and value != 1:
        raise CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            status=constants.STATUS_BAD_REQUEST,
            message="only 0 and 1 will be get in response",
            data=[]
        )    
    return value

class EmpDataResponse(BaseModel):
    id: int = Field(example=1)
    emp_name: str = Field(example="abcd")
    email: EmailStr = Field(example="atul@sssssss.com") 
    mobile: str | None = Field(example="000000")
    status: Annotated[int, Field(example=1), PlainValidator(dataResponseStatusChecker)]

class AuthOut(BaseModel):
    status_code:int | None = None
    status:bool | None = None
    message:str | None = None
    access_token: str
    token_type: str
    data: list[EmpDataResponse] | None = None

class Logout(BaseModel):
    message: str | None = None
    status: bool | None = None
    status_code: int | None = None

class Status422Response(BaseModel):
    status_code:int = Field(default=422)
    status:bool = Field(default=False)
    message:str | None = "Not Processable data"
    data:list | None = []

class Status400Response(BaseModel):
    status_code:int = Field(default=400)
    status:bool = Field(default=False)
    message:str | None = "Bad request"
    data:list | None = []

class Status401Response(BaseModel):
    status_code:int = Field(default=401)
    status:bool = Field(default=False)
    message:str | None = "Unauthorized"
    data:list | None = []

class TokenData(BaseModel):
    email: str | None = None