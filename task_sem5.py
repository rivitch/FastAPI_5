'''Задание
Необходимо создать API для управления списком пользователей. Создайте класс User с полями id, name, email и password.
API должен содержать следующие конечные точки:
— GET /users — возвращает список пользователей.
— GET /users/{id} — возвращает пользователя с указанным идентификатором.
— POST /users — добавляет нового пользователя.
— PUT /users/{id} — обновляет пользователя с указанным идентификатором.
— DELETE /users/{id} — удаляет пользователя с указанным идентификатором.
Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа. Для этого использовать библиотеку Pydantic.
---
Задание по желанию
Создайте HTML шаблон для отображения списка пользователей. Шаблон должен содержать заголовок страницы, таблицу со списком пользователей и кнопку для добавления нового пользователя.'''


#import os,  sys
import logging   # для async def read_root() импортирование логгирования
import uvicorn  # ASGI сервер для запуска приложения
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel  # импортируем функцию создания базовой модели для создания класса User

logging.basicConfig(level=logging.INFO)  #   - создание базовой конфигурации
logger = logging.getLogger(__name__)     #   - для логирования вывода

app = FastAPI()

class User(BaseModel):     # Класс User с полями id, name, email и password. 
    id: int
    name: Optional[str]
    email: Optional[str] 
    password: Optional[str]

class UserInput(BaseModel):     
    name: Optional[str]
    email: Optional[str]  
    password: Optional[str]

users = [] # Список пользователей. # User(id = 0, name ='New0', email = 'for id_0', password = '')

@app.get("/users/")
async def get_users():    # Маршрут для получения списка задач (метод GET).
    logger.info('Отработан GET запрос на получение списка пользователей.')
    return users

@app.get("/users/{id}")
async def read_user(id: int):
    if len(users)<id:
        raise HTTPException(status_code=404, detail="User not found")
    logger.info('Отработан GET запрос на получение одного пользователя.')   
    return users[id-1]

@app.post("/users/", response_model=list[User])   # Маршрут для добавления нового пользователя (метод POST)
async def new_user(user: UserInput):
    user = User(
            id=len(users) + 1,
            name=user.name,
            email=user.email,
            password=user.password
            )
    users.append(user)
    logger.info('Отработан POST запрос. Пользователь успешно добавлен.')
    return users
    
@app.delete("/users/{id}", response_model=str)
async def delete_i(id: int): # , new_user: UserInput
    for user in users:
        if user.id == id:
            users.remove(user)
            logger.info(f'Отработан DELETE запрос на удаление пользователя {id}.')
            return f'Пользователь {id} удален' 
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{id}", response_model=UserInput)
def edit_task(id: int, new_user: UserInput):
    for user in users:
        if user.id == id:
            user.name = new_user.name
            user.email = new_user.email
            user.password = new_user.password
            logger.info(f'Отработан PUT запрос на изменение пользователя {id}.')
            return user  
    raise HTTPException(status_code=404, detail="Task not found")
    
"""основа"""
if __name__ == '__main__': 
    uvicorn.run("task_sem5:app", host="127.0.0.1", port=8000, reload=True)    