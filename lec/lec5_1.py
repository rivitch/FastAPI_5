
import logging   # для async def read_root() импортирование логгирования
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel  # импортируем функцию создания базовой модели для создания класса Item

logging.basicConfig(level=logging.INFO)  # для async def read_root()    - создание базовой конфигурации
logger = logging.getLogger(__name__)     # для async def read_root()    - логгирования для вывода в 19 строке

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None  # описание - опционально тип строка, может не передаваться
    price: float
    tax: Optional[float] = None  # опционально тип float, может не передаваться

# @app.get("/")
# async def root():   #   корутина
#     return {"message": "Hello World"} # Возвращается словарь, получаем json-объект с ключом message и значением Hello World

@app.get("/{item_id}")
async def read_root(item_id:int, item: Item):
    logger.info('Отработал GET запрос.')
    return {"item_id": item_id, "item": item} 
# #@app.get("/items/{item_id}")
# #     logger.info('Отработал GET запрос.')
# #     return item 
# async def read_item(item_id: str, item: Item):
#     logger.info('Отработал GET запрос для item id = {item_id}.')
#     return {"item_id": item_id, "item": item} 
# #---------

# # @app.get("/index/")  # GET-запрос получаем данные с сервера
# @app.get("/items/")  # GET-запрос получаем данные с сервера
# async def read_root(item: Item):
#     logger.info('Отработал GET запрос.')
#     return item 
#     # return {"Hello": "World"} 

@app.post("/items/")  # POST запрос отправляем новые данные на сервера
async def create_item(item: Item):
    logger.info('Отработал POST запрос.')
    return item 
# @app.post("/items/{item_id}")  # POST запрос отправляем новые данные на сервера
# async def create_item(item_id: str, item: Item):
#     logger.info('Отработал POST запрос для item id = {item_id}.')
#     return {"item_id": item_id, "item": item} 

@app.put("/items/{item_id}")  # PUT-запрос изменяем данные на сервере
async def update_item(item_id: str, item: Item):
    logger.info(f'Отработал PUT запрос для item id = {item_id}.')
    return {"item_id": item_id, "item": item} 

@app.delete("/items/{item_id}") # DELETE-запрос удаляем данные на сервере
async def delete_item(item_id: str):
    logger.info(f'Отработал DELETE запрос для item id = {item_id}.')
    return {"item_id": item_id}  

#create_item()

# # основа
# if __name__ == '__main__':
#     uvicorn.run("lec.lec5_1:app", host="127.0.0.1", port=8000, reload=True)      