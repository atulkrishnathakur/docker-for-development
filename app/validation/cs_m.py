from pydantic import (BaseModel,Field, model_validator, EmailStr, ModelWrapValidatorHandler, ValidationError, AfterValidator,BeforeValidator,PlainValidator, ValidatorFunctionWrapHandler)
from app.exception.custom_exception import CustomException
from typing import List
from typing_extensions import Annotated
from typing import Any
from fastapi import status,Depends
from app.config.message import csmmessage
from app.config.constants import constants
from app.database.model_functions import cs_grp_m

def cs_name_checker(value: str) -> str:
    # https://docs.pydantic.dev/latest/concepts/validators/
    if value == "":
        raise CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            status=constants.STATUS_BAD_REQUEST,
            message=csmmessage.CS_NAME,
            data=[]
        )
    return value

def cs_status_checker(value: int) -> int:
    # https://docs.pydantic.dev/latest/concepts/validators/
    if value != 0 and value != 1:
        raise CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            status=constants.STATUS_BAD_REQUEST,
            message=csmmessage.CS_STATUS,
            data=[]
        )
    return value

def cs_grpm_id_checker(value:int)->int:
    if value == 0 or value == "" or value == None:
        raise CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            status=constants.STATUS_BAD_REQUEST,
            message=csmmessage.CS_GRP_M_ID_MESSAGE,
            data=[]
        )
    return value


class CsmSave(BaseModel):
    cs_m_name: Annotated[str, PlainValidator(cs_name_checker), Field(default="Python3",example="Python", title="The description of the item", max_length=300)]
    cs_m_code: str | None = None
    cs_grp_m_id: Annotated[int | None, Field(default=0), PlainValidator(cs_grpm_id_checker)]
    status: Annotated[int | None, Field(default=1), PlainValidator(cs_status_checker)]

    def cs_grpm_id_check_db(db,id):
        csgrpmObj = cs_grp_m.get_data_by_id(db,id)
        if(csgrpmObj is None):
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status=constants.STATUS_BAD_REQUEST,
                message=csmmessage.CS_GRP_M_ID_NOT_EXIST,
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

def id_checker(id)->int:
    if id == "0" or id == 0 or id == None:
        raise CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            status=constants.STATUS_BAD_REQUEST,
            message="Not acceptable value",
            data=[]
        )
    if not id.isdigit():
        raise CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            status=constants.STATUS_BAD_REQUEST,
            message="Only integer value will be accecept in id",
            data=[]
        )
    return id
        

class CsmDataResponse(BaseModel):
    id: int = Field(example=1)
    cs_m_name: str = Field(example="python")
    cs_m_code: str | None = Field(example="py0011")
    cs_grp_m_id: int | None = Field(example="1")
    status: Annotated[int, Field(example=1), PlainValidator(dataResponseStatusChecker)]

class CsmResponse(BaseModel):
    status_code:int = Field(example=1)
    status:bool = Field(example=True)
    message:str | None = None
    data: list[CsmDataResponse] | None = None

class CsmUpdate(BaseModel):
    cs_name: Annotated[str, PlainValidator(cs_name_checker), Field(default="Python3",example="Python", title="The description of the item", max_length=300)]
    cs_code: str | None = None