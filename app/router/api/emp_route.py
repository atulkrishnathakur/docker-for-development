from fastapi import APIRouter,Depends,status,File,UploadFile,BackgroundTasks
from sqlalchemy.orm import Session
from app.database.session import get_db
from sqlalchemy import (select,insert,update,delete,join,and_, or_ )
from app.validation.emp_m import EmpSchemaIn,EmpSchemaOut,Status422Response,Status400Response
from fastapi.responses import JSONResponse, ORJSONResponse
from app.database.model_functions.emp_m import save_new_empm,update_image_empm, get_emp_by_id
from app.exception.custom_exception import CustomException
from app.config.message import empm_message
from app.config.logconfig import loglogger
import os
from typing import Annotated
from app.validation.emp_m import EmpSchemaOut
from app.core.auth import getCurrentActiveEmp
from datetime import datetime
from app.config.jinja2_config import jinjatemplates
from weasyprint import HTML
from app.config.loadenv import envconst
from app.config.fastapi_mail_config import send_email, mailconf

router = APIRouter()

@router.post(
    "/emp-m-save",
    response_model=EmpSchemaOut,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": Status422Response},
        status.HTTP_400_BAD_REQUEST: {"model": Status400Response}
    },
    name="empmsave"
    )
def empSave(empm: EmpSchemaIn, db:Session = Depends(get_db)):
    # I keep duplicate_email_checker function outside of try block because duplicate_email_checker function raise an exception. If duplicate_email_checker keep inside function then Exception class will except it because Exception is parrent class.
    # Main point is raise keyword use the outside of try block.
    EmpSchemaIn.duplicate_email_checker(db,empm.email)
    try:
        insertedData = save_new_empm(db=db, empm=empm)
        http_status_code = status.HTTP_200_OK
        datalist = list()
        
        datadict = {}
        datadict['id'] = insertedData.id
        datadict['emp_name'] = insertedData.emp_name
        datadict['email'] = insertedData.email
        datadict['status'] = insertedData.status
        datadict['mobile'] = insertedData.mobile
        datalist.append(datadict)
        response_dict = {
            "status_code": http_status_code,
            "status":True,
            "message":empm_message.SAVE_SUCCESS,
            "data":datalist
        }
        response_data = EmpSchemaOut(**response_dict) 
        response = JSONResponse(content=response_data.dict(),status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(response_data.dict()))
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

@router.post(
    "/emp-m-upload-profile",
    response_model=EmpSchemaOut,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": Status422Response},
        status.HTTP_400_BAD_REQUEST: {"model": Status400Response}
    },
    name="empmuploadprofile"
    )
def empUploadProfile(
    loginEmp: Annotated[EmpSchemaOut, Depends(getCurrentActiveEmp)],
    file: UploadFile,
    db:Session = Depends(get_db)
    ):
    try:
        loginEmpId = loginEmp.id
        UPLOAD_DIRECTORY = "./app/uploads/" # Ensure the directory exists 
        os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
        fileNameReq = file.filename
        splitFileTpl = os.path.splitext(fileNameReq)
        
        fileNameWithoutExtension = splitFileTpl[0]
        extension = splitFileTpl[1]
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        newFileName = f"{fileNameWithoutExtension}_{current_datetime}{extension}"
        file_location = os.path.join(UPLOAD_DIRECTORY,newFileName)

        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        
        update_image_empm(db,loginEmpId,newFileName)
        http_status_code = status.HTTP_200_OK
        datalist = list()
        response_dict = {
            "status_code": http_status_code,
            "status":True,
            "message":"profile successfully uploaded",
            "data":datalist
        }
        response_data = EmpSchemaOut(**response_dict) 
        response = JSONResponse(content=response_data.dict(),status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(response_data.dict()))
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

@router.post(
    "/get-emp-registration-details",
    response_model=EmpSchemaOut,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": Status422Response},
        status.HTTP_400_BAD_REQUEST: {"model": Status400Response}
    },
    name="getempregistrationdetails"
    )
def generateEmpRegistrationDetails(
    background_tasks:BackgroundTasks,
    loginEmp: Annotated[EmpSchemaOut, Depends(getCurrentActiveEmp)],
    db:Session = Depends(get_db)
    ):
    try:
        GENERATED_PDF_DIR = './app/generated_pdf/'
        loginEmpId = loginEmp.id
        empmObj = get_emp_by_id(db,loginEmpId)
        template = jinjatemplates.get_template("generate_emp_details.html")
        profileUrl = f"{envconst.BASE_URL}/api/uploads/{empmObj.Empm.image}"
        profileDate = empmObj.Empm.created_at.strftime("%d-%B-%Y %H:%M:%S")
        html_content = template.render(
            empname=empmObj.Empm.emp_name,
            empemail=empmObj.Empm.email,
            empmobile=empmObj.Empm.mobile,
            createdAt=profileDate,
            profile_image=profileUrl
        )
        pdf = HTML(string=html_content).write_pdf()

        # Ensure the static directory exists
        os.makedirs(GENERATED_PDF_DIR, exist_ok=True)
        currentDatetime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        pdfFileName = f"emp_{currentDatetime}_.pdf"
        pdf_path = os.path.join(GENERATED_PDF_DIR, pdfFileName)

        # Save the PDF to the static directory
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(pdf)

        http_status_code = status.HTTP_200_OK
        datalist = list()
        response_dict = {
            "status_code": http_status_code,
            "status":True,
            "message":"pdf successfully generated",
            "data":datalist
        }
        response_data = EmpSchemaOut(**response_dict) 
        response = JSONResponse(content=response_data.dict(),status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(response_data.dict()))

        body = """<h1>Check the attachement for profile details</h1> """
        subject = "Profile details"
        toemail = ['atulkkk@yopmail.com']
        ccemail = ['atulcc@yopmail.com']
        bccemail = ['atulbcc@yopmail.com']
        emailBody = body
        attachmentsList = [pdf_path]
        send_email(
            background_tasks=background_tasks,
            emaiSubject=subject,
            emailTo=toemail,
            emailBody=emailBody,
            ccemail=ccemail,
            bccemail=bccemail,
            attachmentsList=attachmentsList
            )

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
