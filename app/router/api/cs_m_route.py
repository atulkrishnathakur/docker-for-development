from fastapi import APIRouter,Depends,status,HTTPException,Path
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.session import get_db
from sqlalchemy import (select,insert,update,delete,join,and_, or_ )
from fastapi.encoders import jsonable_encoder
from app.validation.cs_m import CsmSave,CsmResponse,CsmUpdate,id_checker
from app.validation.emp_m import EmpSchemaOut
from fastapi.responses import JSONResponse, ORJSONResponse
from app.database.model_functions.cs_m import (save_new_cs,get_all_data,get_all_active_data,get_data_by_id,update_by_id,soft_delete)
from app.exception.custom_exception import CustomException
from pydantic import (BaseModel,Field, model_validator, EmailStr, ModelWrapValidatorHandler, ValidationError, AfterValidator,BeforeValidator,PlainValidator, ValidatorFunctionWrapHandler)
from app.config.message import csmmessage
from app.config.logconfig import loglogger
from app.core.auth import getCurrentActiveEmp

router = APIRouter()

@router.post("/csm-save", response_model=CsmResponse, name="csmsave")
def csmSave(current_user: Annotated[EmpSchemaOut, Depends(getCurrentActiveEmp)],csm: CsmSave, db:Session = Depends(get_db)):
    # I keep cs_grpm_id_check_db function outside of try block because cs_grpm_id_check_db function raise an exception. If cs_grpm_id_check_db keep inside function then Exception class will except it because Exception is parrent class.
    # Main point is raise keyword use the outside of try block.
    CsmSave.cs_grpm_id_check_db(db,csm.cs_grp_m_id)
    try:        
        insertedData = save_new_cs(db=db, csm=csm)
        http_status_code = status.HTTP_200_OK
        datalist = list()
        
        datadict = {}
        datadict['id'] = insertedData.id
        datadict['cs_m_name'] = insertedData.cs_m_name
        datadict['cs_m_code'] = insertedData.cs_m_code
        datadict['cs_grp_m_id'] = insertedData.cs_grp_m_id
        datadict['status'] = insertedData.status
        datalist.append(datadict)
        response_dict = {
            "status_code": http_status_code,
            "status":True,
            "message":csmmessage.CS_SAVE_MESSAGE,
            "data":datalist
        }
        response_data = CsmResponse(**response_dict) 
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