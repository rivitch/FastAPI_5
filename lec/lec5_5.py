#Автоматическая документация по API
#1.Интерактивная документация Swagger

import logging   # для async def read_root() импортирование логгирования
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel  # импортируем функцию создания базовой модели для создания класса Item
from fastapi.openapi.utils import get_openapi

logging.basicConfig(level=logging.INFO)  # для async def read_root()    - создание базовой конфигурации
logger = logging.getLogger(__name__)     # для async def read_root()    - логгирования для вывода в 23 строке

# app = FastAPI()
app = FastAPI(openapi_url="/openapi.json")

class Item(BaseModel):
    name: str
    description: Optional[str] = None  # описание - опционально тип строка, может не передаваться
    price: float
    tax: Optional[float] = None  # опционально тип float, может не передаваться

@app.get("/{item_id}")
async def read_root():
    logger.info('Отработал GET запрос.')
    return f'item'

@app.post("/items/")  # POST запрос отправляем новые данные на сервера
async def create_item(item: Item):
    logger.info('Отработал POST запрос.')
    return item 

@app.put("/items/{item_id}")  # PUT-запрос изменяем данные на сервере
async def update_item(item_id: str, item: Item):
    logger.info(f'Отработал PUT запрос для item id = {item_id}.')
    return {"item_id": item_id, "item": item} 

@app.delete("/items/{item_id}") # DELETE-запрос удаляем данные на сервере
async def delete_item(item_id: str):
    logger.info(f'Отработал DELETE запрос для item id = {item_id}.')
    return {"item_id": item_id} 

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
    title="Custom title",
    version="1.0.0",
    description="This is a very custom OpenAPI schema",
    routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapi