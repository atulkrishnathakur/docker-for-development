from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse, ORJSONResponse, HTMLResponse
from fastapi import Depends, status, HTTPException, Request, Header
from app.router.router_base import api_router
from app.exception.custom_exception import CustomException
from app.config.message import auth_message
import re

# https://fastapi.tiangolo.com/tutorial/middleware/

class AuthCheckerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, some_attribute: str):
        super().__init__(app)
        self.some_attribute = some_attribute
    # url_path_for("route name here")
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        excluded_paths = [
            "/docker-for-development-docs",
            "/api/docker-for-development.json",
            "/api"+api_router.url_path_for("login"),
            "/api"+api_router.url_path_for("apitest"),
            "/api/uploads/.*",
            "/api/pdf/.*"
            ]

        if any(re.match(path, request.url.path) for path in excluded_paths):
            return await call_next(request)

        if request.url.path not in excluded_paths and (token is None or not token.startswith("Bearer ")) :
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status_code":status.HTTP_401_UNAUTHORIZED,
                    "status":False,
                    "message":auth_message.LOGIN_REQUIRED,
                    "data":[]
                    },
            )
        response = await call_next(request)
        return response
