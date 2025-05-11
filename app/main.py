from fastapi import FastAPI
from fastapi import FastAPI,Depends, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from app.router.router_base import api_router
from app.router.web_router_base import web_router
from app.exception.custom_exception import CustomException,unicorn_exception_handler
from app.middlewares.authchekermiddleware import AuthCheckerMiddleware
from app.config.static_mount import mount_uploaded_files, mount_generated_pdf

def include_router(app):
    app.include_router(api_router)
    app.include_router(web_router)

def start_application():
    app = FastAPI(
        DEBUG=True,
        title="docker for development",
        summary="This is a fastapi project",
        description="This is fastapi project with sqlalchemy",
        version="1.0.0",
        openapi_url="/docker-for-development.json",
        docs_url="/docker-for-development-docs",
        redoc_url="/docker-for-development-redoc",
        root_path="/api",
        root_path_in_servers=True,
        )
        
    mount_uploaded_files(app)
    mount_generated_pdf(app)    
    include_router(app)
    return app

app = start_application()
app.add_exception_handler(CustomException,unicorn_exception_handler)
app.add_middleware(AuthCheckerMiddleware, some_attribute="example_attribute")
