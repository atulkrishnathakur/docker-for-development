from pydantic import BaseModel, model_validator, EmailStr
from typing import List

class EmailSchema(BaseModel):
    email: List[EmailStr]
    subject: str
    body: str