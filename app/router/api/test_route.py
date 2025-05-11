from fastapi import APIRouter,Depends,status
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.session import get_db
from fastapi import status
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy import join
from sqlalchemy import and_, or_
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.get("/apitest",name="apitest")
def testf(db:Session = Depends(get_db)):
    try:
        return "hello uuuuuuuuu"
    except Exception as e:
        print(f"Exception error {e}")
