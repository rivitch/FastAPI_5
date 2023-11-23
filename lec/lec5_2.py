#Создание конечных точек API
# 1. Определение конечных точек(КТ) API(маршрут, asins-функция)(41:50)

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse # для 2. Форматирования ответов API

app = FastAPI()

# @app.get("/")     # КТ 1                 
# async def read_root():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}") # КТ 2
# # items - S  в конце говорит о множественном числе
# async def read_item(item_id: int):
#     return {"item_id": item_id}

# (45:05)
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# (47:40)
@app.get("/users/{user_id}/orders/{order_id}")
async def read_item(user_id: int, order_id: int):
# обработка данных
    return {"user_id": user_id, "order_id": order_id}

# (50:05)
@app.get("/items/")     # Выборка из базы данных
async def read_item(skip: int = 5, limit: int = 10): # выборка - получить 10 записей начиная с 5 адреса(пропустив 5 записей)
    return {"skip": skip, "limit": limit}

# 2. Форматирование ответов API
#(52:15)


# ----
# допустимы оба стиля, но в проекте нужно придерживаться какогото одного единого

# @app.get("/", response_class=HTMLResponse)                     
# async def read_root():
#     return "<h1>Hello World</h1>"
@app.get("/message")
async def read_message():
    message = {"message": "Hello World"}
    return JSONResponse(content=message, status_code=200)
# ---- 
