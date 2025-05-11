from fastapi import HTTPException, Response, Request
from fastapi.responses import JSONResponse, ORJSONResponse

class CustomException(HTTPException):
    def __init__(self, status_code: int, status:bool | None=None, message:str | None=None, data:list | None=None):
        self.status_code = status_code
        self.status = status
        self.message = message
        self.data = data

async def unicorn_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status_code":exc.status_code,"status":exc.status,"message":exc.message,"data":exc.data},
    )
