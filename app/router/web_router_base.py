from fastapi import APIRouter
from app.router.web import web_route_test

web_router = APIRouter()

web_router.include_router(web_route_test.router)