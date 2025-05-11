from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse
from app.config.jinja2_config import jinjatemplates

router = APIRouter()

@router.get("/web-test", response_class=HTMLResponse)
async def read_item(request: Request):
    mname="Atul"
    return jinjatemplates.TemplateResponse(
        request=request, name="test.html", context={"mname": mname}
    )