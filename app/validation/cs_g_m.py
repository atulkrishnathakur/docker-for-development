from pydantic import (BaseModel,Field, model_validator, EmailStr, ModelWrapValidatorHandler, ValidationError, AfterValidator,BeforeValidator,PlainValidator, ValidatorFunctionWrapHandler)
from app.exception.custom_exception import CustomException
from typing import List
from typing_extensions import Annotated
from typing import Any
from fastapi import status
from app.config.message import csgrpmessage
from app.config.constants import constants

def cs_grp_name_checker(value: str) -> str:
    # https://docs.pydantic.dev/latest/concepts/validators/
    if value == "":
        raise CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            status=constants.STATUS_BAD_REQUEST,
            message=csgrpmessage.CS_GRP_NAME,
            data=[]
        )
    return value

def cs_grp_status_checker(value: int) -> int:
    # https://docs.pydantic.dev/latest/concepts/validators/
    if value != 0 and value != 1:
        raise CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            status=constants.STATUS_BAD_REQUEST,
            message=csgrpmessage.CS_GRP_STATUS,
            data=[]
        )
    return value

class CsgmSave(BaseModel):
    cs_grp_name: Annotated[str, PlainValidator(cs_grp_name_checker), Field(default="Python3",example="Python", title="The description of the item", max_length=300)]
    cs_grp_code: str | None = None
    status: Annotated[int | None, Field(default=1), PlainValidator(cs_grp_status_checker)]

def dataResponseStatusChecker(value: int)-> int:
    # https://docs.pydantic.dev/latest/concepts/validators/
    if value != 0 and value != 1:
        raise CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            status=constants.STATUS_BAD_REQUEST,
            message=csgrpmessage.CS_GRP_STATUS_RES,
            data=[]
        )    
    return value

def id_checker(id)->int:
    if id == "0" or id == 0 or id == None:
        raise CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            status=constants.STATUS_BAD_REQUEST,
            message=csgrpmessage.CS_GRP_ID_REQ,
            data=[]
        )
    if not id.isdigit():
        raise CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            status=constants.STATUS_BAD_REQUEST,
            message=csgrpmessage.CS_GRP_ID_REQ,
            data=[]
        )
    return id
        
class CsgmDataResponse(BaseModel):
    id: int = Field(example=1)
    cs_grp_name: str = Field(example="python")
    cs_grp_code: str | None = Field(example="py0011")
    status: Annotated[int, Field(example=1), PlainValidator(dataResponseStatusChecker)]

class CsgmResponse(BaseModel):
    status_code:int = Field(example=1)
    status:bool = Field(example=True)
    message:str | None = None
    data: list[CsgmDataResponse] | None = None

class CsgmUpdate(BaseModel):
    cs_grp_name: Annotated[str, PlainValidator(cs_grp_name_checker), Field(default="Python3",example="Python", title="The description of the item", max_length=300)]
    cs_grp_code: str | None = None

class Status422Response(BaseModel):
    status_code:int = Field(example=422)
    status:bool = Field(example=True)
    message:str | None = "Not Processable data"
    data:list | None = []