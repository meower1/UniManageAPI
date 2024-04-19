from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates("app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    """
    Redirect the user to /docs when visiting the root path
    """
    return templates.TemplateResponse(request=request, name="index.html")
