from fastapi import APIRouter,Depends,status,HTTPException,Path,Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.session import get_db
from sqlalchemy import (select,insert,update,delete,join,and_, or_ )
from fastapi.encoders import jsonable_encoder
from app.validation.cs_g_m import CsgmSave,CsgmResponse,CsgmUpdate,id_checker,Status422Response
from app.validation.emp_m import EmpSchemaOut
from fastapi.responses import JSONResponse, ORJSONResponse
from app.database.model_functions.cs_grp_m import (save_new_cs_group,get_all_data,get_all_active_data,get_data_by_id,update_by_id,soft_delete)
from app.exception.custom_exception import CustomException
from pydantic import (BaseModel,Field, model_validator, EmailStr, ModelWrapValidatorHandler, ValidationError, AfterValidator,BeforeValidator,PlainValidator, ValidatorFunctionWrapHandler)
from app.config.message import csgrpmessage
from app.config.logconfig import loglogger
from app.core.auth import getCurrentActiveEmp

router = APIRouter()

@router.post(
    "/cs-g-m-save",
    response_model=CsgmResponse,
    name="csgmsave"
    )
def csgmSave(
    current_user: Annotated[EmpSchemaOut, Depends(getCurrentActiveEmp)],
    csgm: CsgmSave,
    db:Session = Depends(get_db)
    ):
    try:
        insertedData = save_new_cs_group(db=db, csgm=csgm)
        http_status_code = status.HTTP_200_OK
        datalist = list()
        
        datadict = {}
        datadict['id'] = insertedData.id
        datadict['cs_grp_name'] = insertedData.cs_grp_name
        datadict['cs_grp_code'] = insertedData.cs_grp_code
        datadict['status'] = insertedData.status
        datalist.append(datadict)
        response_dict = {
            "status_code": http_status_code,
            "status":True,
            "message":csgrpmessage.CS_GRP_SAVE_MESSAGE,
            "data":datalist
        }
        # by help of jsonable_encode we are sending response in json with pydantic validation
        #response = JSONResponse(content=jsonable_encoder(response_dict),status_code=http_status_code)
        #response = JSONResponse(content=response_dict,status_code=http_status_code)
        response_data = CsgmResponse(**response_dict) 
        response = JSONResponse(content=response_data.dict(),status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(response_data.dict()))
        return response
    except Exception as e:
        http_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        data = {
            "status_code": http_status_code,
            "status":False,
            "message":e.errors()
        }
        response = JSONResponse(content=data,status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(data))
        return response

@router.get(
    "/cs-g-m-list",
    response_model=CsgmResponse,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": Status422Response}
        },
        name="csgmlist"
        )
def getCsgmList(
    current_user: Annotated[EmpSchemaOut, Depends(getCurrentActiveEmp)],
    db:Session = Depends(get_db)
    ):
    try:
        allDbData = get_all_data(db=db)
        http_status_code = status.HTTP_200_OK
        datalist = list()
        
        for dbdata in allDbData:
            datadict = {}
            datadict['id'] = dbdata.Csgrpm.id
            datadict['cs_grp_name'] = dbdata.Csgrpm.cs_grp_name
            datadict['cs_grp_code'] = dbdata.Csgrpm.cs_grp_code
            datadict['status'] = dbdata.Csgrpm.status
            datalist.append(datadict)
            response_dict = {
                "status_code": http_status_code,
                "status":True,
                "message":csgrpmessage.CS_GRP_LIST_MESSAGE,
                "data":datalist
            }
        response_data = CsgmResponse(**response_dict) 
        response = JSONResponse(content=response_data.dict(),status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(response_data.dict()))
        return response
    except Exception as e:
        http_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        data = {
            "status_code": http_status_code,
            "status":False,
            "message":e.errors()
        }
        response = JSONResponse(content=data,status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(data))
        return response

@router.get(
    "/cs-g-m-active-list",
    response_model=CsgmResponse,
    name="csgmactivelist"
    )
def getCsgmList(
    current_user: Annotated[EmpSchemaOut, Depends(getCurrentActiveEmp)],
    db:Session = Depends(get_db)
    ):
    try:
        allDbData = get_all_active_data(db=db)
        http_status_code = status.HTTP_200_OK
        datalist = list()
        
        for dbdata in allDbData:
            datadict = {}
            datadict['id'] = dbdata.Csgrpm.id
            datadict['cs_grp_name'] = dbdata.Csgrpm.cs_grp_name
            datadict['cs_grp_code'] = dbdata.Csgrpm.cs_grp_code
            datadict['status'] = dbdata.Csgrpm.status
            datalist.append(datadict)
            response_dict = {
                "status_code": http_status_code,
                "status":True,
                "message":csgrpmessage.CS_GRP_ACTIVE_LIST_MESSAGE,
                "data":datalist
            }
        response_data = CsgmResponse(**response_dict) 
        response = JSONResponse(content=response_data.dict(),status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(response_data.dict()))
        return response
    except Exception as e:
        http_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        data = {
            "status_code": http_status_code,
            "status":False,
            "message":e.errors()
        }
        response = JSONResponse(content=data,status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(data))
        return response

@router.post("/cs-g-m-update/{id}", response_model=CsgmResponse, name="csgmupdate")
def csgmUpdate(
    current_user: Annotated[EmpSchemaOut, Depends(getCurrentActiveEmp)],
    csgm: CsgmUpdate,
    id:int = Depends(id_checker),
    db:Session = Depends(get_db)
    ):
    try:
        updatedData = update_by_id(db=db,csgm=csgm,id=id)
        http_status_code = status.HTTP_200_OK
        datalist = list()

        datadict = {}
        datadict['id'] = updatedData.Csgrpm.id
        datadict['cs_grp_name'] = updatedData.Csgrpm.cs_grp_name
        datadict['cs_grp_code'] = updatedData.Csgrpm.cs_grp_code
        datadict['status'] = updatedData.Csgrpm.status
        datalist.append(datadict)
        response_dict = {
            "status_code": http_status_code,
            "status":True,
            "message":csgrpmessage.CS_GRP_UPDATE_MESSAGE,
            "data":datalist
        }

        response_data = CsgmResponse(**response_dict) 
        response = JSONResponse(content=response_data.dict(),status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(response_data.dict()))
        return response

    except Exception as e:
        http_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        data = {
            "status_code": http_status_code,
            "status":False,
            "message":e.errors()
        }
        response = JSONResponse(content=data,status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(data))
        return response

@router.post("/cs-g-m-soft-delete/{id}", response_model=CsgmResponse, name="csgmsoftdelete")
def csgmDelete(
    current_user: Annotated[EmpSchemaOut, Depends(getCurrentActiveEmp)],
    id:int = Depends(id_checker),
    db:Session = Depends(get_db)
    ):
    try:
        deletedData = soft_delete(db=db,id=id)
        http_status_code = status.HTTP_200_OK
        datalist = list()

        response_dict = {
            "status_code": http_status_code,
            "status":True,
            "message":csgrpmessage.DELETE_SUCCESS,
            "data":datalist
        }

        response_data = CsgmResponse(**response_dict) 
        response = JSONResponse(content=response_data.dict(),status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(response_data.dict()))
        return response
    except Exception as e:
        http_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        data = {
            "status_code": http_status_code,
            "status":False,
            "message":e.errors()
        }
        response = JSONResponse(content=data,status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(data))
        return response
