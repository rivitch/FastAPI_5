# Задание №2
# 📌 Создать API для получения списка фильмов по жанру. Приложение должно
# иметь возможность получать список фильмов по заданному жанру.
# 📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
# 📌 Создайте класс Movie с полями id, title, description и genre.
# 📌 Создайте список movies для хранения фильмов.
# 📌 Создайте маршрут для получения списка фильмов по жанру (метод GET).
# 📌 Реализуйте валидацию данных запроса и ответа

import logging   # для async def read_root() импортирование логгирования
import uvicorn  # ASGI сервер для запуска приложения
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel  # импортируем функцию создания базовой модели для создания класса Movie

logging.basicConfig(level=logging.INFO)  # для async def read_root()    - создание базовой конфигурации
logger = logging.getLogger(__name__)     # для async def read_root()    - логгирования для вывода в 19 строке

app = FastAPI()  # 1b

  

class Genre(BaseModel):     # 1c Создайте класс Task с полями id, title, description и status. 
    id: int
    title: str


class Movie(BaseModel):     # 1c Создайте класс Task с полями id, title, description и status. 
    id: int
    title: str
    description: Optional[str]  # описание - опционально тип строка, может не передаваться
    genre: Genre

movies = [
    Movie(id = 1, title ='New1', description = 'for id_1', genre = Genre(id=1, title = 'fant' )), Movie(id = 2, title ='New2', description = 'for id_2', genre = Genre(id=2, title = 'komedy' ))
    ] 

@app.get("/")
async def get_main():
    return 'Movie base'

@app.get("/films/", response_model=list[Movie])
async def get_films(id_genre:int):    # Создайте маршрут для получения списка фильмов по жанру (метод GET).
    my_movies = [i for i in movies if i.genre.id == id_genre]
    logger.info('Отработал GET запрос на получение списка фильмов.')
    return my_movies
    
if __name__ == '__main__': 
    uvicorn.run("sem5_2:app", host="127.0.0.1", port=8000, reload=True)
