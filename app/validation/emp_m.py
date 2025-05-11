from pydantic import (BaseModel,Field, model_validator, EmailStr, ModelWrapValidatorHandler, ValidationError, AfterValidator,BeforeValidator,PlainValidator, ValidatorFunctionWrapHandler)
from typing import List
from app.exception.custom_exception import CustomException
from fastapi import status,Depends
from app.config.message import empm_message
from app.config.constants import constants
from typing_extensions import Annotated
from app.database.model_functions import emp_m

class BaseEmpSchema(BaseModel):
    emp_name: str = Field(example="Atul")
    email: EmailStr = Field(example="atul@comsysapp.com")
    mobile: str | None = Field(example="000000")
    status: int | None = Field(default=1)

class EmpSchemaIn(BaseEmpSchema):
    password: str = Field(example="aa")
    confirm_password:str = Field(example="aa")
    
    def duplicate_email_checker(db,email):
        empmObj = emp_m.get_data_by_email(db,email)
        if(empmObj is not None):
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status=constants.STATUS_BAD_REQUEST,
                message=empm_message.EMAIL_DUPLICATE,
                data=[]
            )

    @model_validator(mode='after')
    def check_passwords_match(self):
        pw1 = self.password
        pw2 = self.confirm_password
        if(pw1 is None):
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status=constants.STATUS_BAD_REQUEST,
                message=empm_message.EMP_M_PASS_REQUIRED,
                data=[]
            )
        elif(pw2 is None):
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status=constants.STATUS_BAD_REQUEST,
                message=empm_message.EMP_M_C_PASS_REQUIRED,
                data=[]
            )
        elif pw1 != pw2:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status=constants.STATUS_BAD_REQUEST,
                message=empm_message.PASS_NOT_MATCH,
                data=[]
            )
        return self

'''
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
'''   

class EmpDataResponse(BaseModel):
    id: int = Field(example=1)
    emp_name: str = Field(example="abcd")
    email: EmailStr = Field(example="atul@comsysapp.com") 
    mobile: str | None = Field(example="000000")
    status: int = Field(example=1)

class EmpSchemaOut(BaseModel):
    status_code:int = Field(example=1)
    status:bool = Field(example=True)
    message:str | None = None
    data: list[EmpDataResponse] | None = []

class EmpInDB(BaseEmpSchema):
    hashed_password: str

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