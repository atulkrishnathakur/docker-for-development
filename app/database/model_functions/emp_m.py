from app.database.model.emp_m import Empm
from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy import func
from app.core.hashing import HashData
from app.config.constants import constants
from app.database.dbconnection import engine
from app.config.logconfig import loglogger

def save_new_empm(db, empm):
    db_empm = Empm(
        emp_name=empm.emp_name,
        email=empm.email,
        mobile=empm.mobile,
        status=empm.status,
        password=HashData.create_password_hash(empm.password)
        )
    db.add(db_empm)
    db.commit()
    db.refresh(db_empm)
    return db_empm

def get_data_by_email(db,email):
    try:
        stmt = select(Empm).where(Empm.email == email)
        result = db.execute(stmt)
        data = result.first()
        return data
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

def update_image_empm(db,loginEmpId,newFileName):
    try:
        stmt = update(Empm).where(Empm.id == loginEmpId).values(image=newFileName)
        db.execute(stmt)
        db.commit()
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


def get_emp_by_id(db,id):
    try:
        stmt = select(Empm).where(Empm.id == id)
        result = db.execute(stmt)
        data = result.first()
        return data
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
