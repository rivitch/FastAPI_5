# Задание №1
# 1a Создать API для управления списком задач. Приложение должно иметь возможность создавать, обновлять, удалять и получать список задач.
# 1b Создайте модуль приложения и настройте сервер и маршрутизацию.
# 1c Создайте класс Task с полями id, title, description и status.
# 1d Создайте список tasks для хранения задач.
# 1e Создайте маршрут для получения списка задач (метод GET).
# 1f Создайте маршрут для создания новой задачи (метод POST).
# 1j Создайте маршрут для обновления задачи (метод PUT).
# 1k Создайте маршрут для удаления задачи (метод DELETE).
# 1l Реализуйте валидацию данных запроса и ответа.

import logging   # для async def read_root() импортирование логгирования
import uvicorn  # ASGI сервер для запуска приложения
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel  # импортируем функцию создания базовой модели для создания класса Task

logging.basicConfig(level=logging.INFO)  # для async def read_root()    - создание базовой конфигурации
logger = logging.getLogger(__name__)     # для async def read_root()    - логгирования для вывода в 19 строке

app = FastAPI()  # 1b

class Task(BaseModel):     # 1c Создайте класс Task с полями id, title, description и status. 
    id: int
    title: str
    description: Optional[str]  # описание - опционально тип строка, может не передаваться
    status: bool

class TaskInput(BaseModel):    # 1c Создайте класс Task с полями id, title, description и status. 
    title: Optional[str]
    description: Optional[str]  # описание - опционально тип строка, может не передаваться
    status: Optional[bool]

tasks = [
    Task(id = 1, title ='New1', description = 'for id_1', status = True)
    ]                                                              # 1d Создайте список tasks для хранения задач.
#print(len(tasks))
# проверочник
@app.get("/tasks/")
async def get_tasks():    # 1e Создайте маршрут для получения списка задач (метод GET).
    logger.info('Отработал GET запрос на получение списка задач.')
    return tasks
    """или"""
    # message = "Hello World"
    # return f'{message}'

# @app.get("/task_id/{task_id}")
# async def read_item(task_id: int):
#     logger.info('Отработал GET запрос на получение одной задачи.')
#     return tasks[task_id-1]
@app.get("/task_id/{task_id}")
async def read_item(task_id: int):
    if len(tasks)<task_id:
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info('Отработал GET запрос на получение одной задачи.')   
    return tasks[task_id-1]

# @app.post("/tasks/")  # POST запрос отправляем новые данные на сервер
# async def create_tasks(task: TaskInput):
#     tasks.append(task)
#     logger.info('Отработал POST запрос. Задача успешно добавлена.')
#     return task 

@app.post("/tasks/", response_model=list[Task])   # 1f Создайте маршрут для создания новой задачи (метод POST)
async def new_task(task: TaskInput):
    task = Task(
            id=len(tasks) + 1,
            title=task.title,
            description=task.description,
            status=task.status
            )
    tasks.append(task)
    logger.info('Отработал POST запрос. Задача успешно добавлена.')
    return tasks

# @app.put("/task_id/{task_id}")
# async def put_item(task_id: int, new_task: TaskInput):
#     if len(tasks)<task_id:
#         raise HTTPException(status_code=404, detail="Task not found")
#     logger.info('Отработал PUT запрос на изменение одной задачи.')   
#     return tasks[task_id-1]
@app.put("/tasks/{task_id}", response_model=TaskInput)
async def update_task(task_id: int, new_task: TaskInput):
    if len(tasks)<task_id:
        raise HTTPException(status_code=404, detail="Task not found")
    for task in tasks:
        if task.id == task_id:
            task.title = new_task.title
            task.description = new_task.description
            task.status = new_task.status
            #return f'Задача {task_id} изменена'          
    logger.info('Отработал PUT запрос на изменение задачи {task_id}.')  
    
@app.delete("/tasks/{task_id}", response_model=str)
async def delete_task(task_id: int, new_task: TaskInput):
    if len(tasks)<task_id:
        raise HTTPException(status_code=404, detail="Task not found")
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return f'Задача {task_id} удалена'   
    logger.info('Отработал DELETE запрос на удаление задачи {task_id}.') 
    

# 52:20



"""основа"""
if __name__ == '__main__': 
    uvicorn.run("sem5_1:app", host="127.0.0.1", port=8000, reload=True)
