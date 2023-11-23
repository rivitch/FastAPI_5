# Динамический HTML через шаблонизатор Jinja (56:25)

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="./lec/templates")

@app.get("/{name}", response_class=HTMLResponse)
async def read_item(request: Request, name: str):
    return templates.TemplateResponse("item.html", {"request": request, "name": name})