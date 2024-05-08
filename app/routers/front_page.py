from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates("templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    """
    Redirect the user to /docs when visiting the root path
    """
    # return RedirectResponse("docs")
    # return templates.TemplateResponse("layout.html", {"request": request})
    return templates.TemplateResponse(
        request=request, name="index.html", context={"meow": "meow"}
    )

