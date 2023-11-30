import uvicorn
import databases
import sqlalchemy
from typing import List  # из модуля импортировали функцию для работы со списком данных
from fastapi import FastAPI
from pydantic import BaseModel  # базовая модель для создания классов
from pydantic import Field # Field задавает различные параметры для поля
#from fastapi.responses import HTMLResponse, JSONResponse

DATABASE_URL = "sqlite:///mydatabase.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

#=============
# Таблицы
users = sqlalchemy.Table(   # Table - класс для создания таблицы   
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),   # поле id целого типа, заполняется автоматически
    sqlalchemy.Column("first_name", sqlalchemy.String(32)),
    sqlalchemy.Column("second_name", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(32)),
    sqlalchemy.Column("password", sqlalchemy.String(32)), 
    # sqlalchemy.Column("is_active", sqlalchemy.Boolean, default=True)
    )

products = sqlalchemy.Table(   # Table - класс для создания таблицы   
    "products",
    metadata,
    sqlalchemy.Column("product_id", sqlalchemy.Integer, primary_key=True),   # поле id целого типа, заполняется автоматически
    sqlalchemy.Column("product", sqlalchemy.String(32)),
    sqlalchemy.Column("description", sqlalchemy.String(32)),
    sqlalchemy.Column("price", sqlalchemy.String(32)),
    # sqlalchemy.Column("is_active", sqlalchemy.Boolean, default=True)
    )

orders = sqlalchemy.Table(   # Table - класс для создания таблицы   
    "orders",
    metadata,
    sqlalchemy.Column("order_id", sqlalchemy.Integer, primary_key=True),   # поле id целого типа, заполняется автоматически
    sqlalchemy.Column("customer", sqlalchemy.String()),  #()?
    sqlalchemy.Column("order_product", sqlalchemy.String()),   #()?
    sqlalchemy.Column("date", sqlalchemy.String(32)),
    # sqlalchemy.Column("is_active", sqlalchemy.Boolean, default=True)
    )   

engine = sqlalchemy.create_engine(DATABASE_URL, 
        connect_args={"check_same_thread": False} # параметр нужен только для работы с sqlite
        )

metadata.create_all(engine)

app = FastAPI()

#==============
# Классы пользователей
class User(BaseModel):
    user_id: int 
    first_name: str = Field(max_length=32) 
    second_name: str = Field(max_length=32)
    email: str = Field(max_length=32) 
    password: str = Field(max_length=32)
    #is_active: Boolean = Field(default=True)  # статус наличия

class UserIn(BaseModel):         # добавление нового пользователя, идентификатор добавляется автоматически  
    first_name: str = Field(max_length=32) 
    second_name: str = Field(max_length=32)
    email: str = Field(max_length=32) 
    password: str = Field(max_length=32)
    #is_active: Boolean = Field(default=True)  # статус наличия    

# Классы товара
class Product(BaseModel):
    product_id: int # первичный ключ
    product: str = Field(max_length=32)   #  товар
    description: str = Field(max_length=32)   #  описание
    price: str = Field(max_length=32)   #  цена
    #is_active: Boolean = Field(default=True) # статус наличия

class ProductIn(BaseModel):         # добавление нового товара
    product: str = Field(max_length=32)
    description: str = Field(max_length=32)   
    price: str = Field(max_length=32)  

# Классы заказа
class Order(BaseModel):
    order_id: int  # первичный ключ
    customer: str   # вторичный ключ
    order_product:  str # вторичный ключ
    date: str = Field(max_length=32)   #  дата заказа
    #is_active: Boolean = Field(default=True)   # статус

class OrderIn(BaseModel):         # добавление нового заказа
    customer: str  # вторичный ключ
    order_product: str   # вторичный ключ
    date: str = Field(max_length=32)   #  дата заказа





#==============
@app.get("/fake/{count}")  # сгенерируем несколько тестовых пользователей в базе данных
async def create_note(count: int): # синхронный запрос к функции
    for i in range(count):
        query_users = users.insert().values(first_name=f'first_name{i+1}', second_name=f'second_name{i+1}', email=f'mail{i+1}@mail.ru', password=f'password{i+1}')
        query_products = products.insert().values(product=f'product{i+1}', description=f'description{i+1}', price=f'price{i+1}')
        query_orders = orders.insert().values(customer=f'customer{i+1}', order_product=f'order_product{i+1}', date=f'date = ')
        await database.execute(query_orders)
        await database.execute(query_products)
        await database.execute(query_users)
    return {'message': f'{count} fake users, products, orders create'}

#==================
# необходимые маршруты для реализации REST API.
# 1. Создание пользователя в БД, create
@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(**user.dict())  # insert -вставить    #    ... идентичны \  превращение модели в питоновский словарь, ** - распаковка словаря  
    last_record_id = await database.execute(query) # асинхроныый запрос, передача запроса в команду execute - выполнить и запись в переменную last_record_id
    return {**user.dict(), "id": last_record_id}

# 2. Чтение пользователей из БД, read
@app.get("/users_all/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)

# 2a. Выборка из базы данных
@app.get("/users/", response_model=List[User])
async def get_items(skip: int, limit: int):  # выборка - получить limit записей начиная с skip адреса(пропустив skip записей)
    query = users.select().offset(skip).limit(limit)
    results = await database.fetch_all(query)
    return [dict(result) for result in results]

# 3. Чтение одного пользователя из БД, read
@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)

# 4. Обновление пользователя в БД, update
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}

# 5. Удаление пользователя из БД, delete
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}

# ---=============================================================
# 1. Создание товара в БД, create
@app.post("/products/", response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(**product.dict())  # insert -вставить    #    ... идентичны \  превращение модели в питоновский словарь, ** - распаковка словаря  
    last_record_id = await database.execute(query) # асинхроныый запрос, передача запроса в команду execute - выполнить и запись в переменную last_record_id
    return {**products.dict(), "id": last_record_id}

# 2. Чтение товара из БД, read
@app.get("/products_all/", response_model=List[Product])
async def read_products():
    query = products.select()
    return await database.fetch_all(query)

# 2a. Выборка из базы данных
@app.get("/products/", response_model=List[Product])
async def get_items_product(skip: int, limit: int):  # выборка - получить limit записей начиная с skip адреса(пропустив skip записей)
    query = products.select().offset(skip).limit(limit)
    results = await database.fetch_all(query)
    return [dict(result) for result in results]

# 3. Чтение одного товара из БД, read
@app.get("/products/{product_id}", response_model=User)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)

# 4. Обновление товара в БД, update
@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(**new_product.dict())
    await database.execute(query)
    return {**new_product.dict(), "id": product_id}

# 5. Удаление товара из БД, delete
@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {'message': 'Product deleted'}

# ---=============================================================
# 1. Создание заказа в БД, create
@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(**order.dict())  # insert -вставить    #    ... идентичны \  превращение модели в питоновский словарь, ** - распаковка словаря  
    last_record_id = await database.execute(query) # асинхроныый запрос, передача запроса в команду execute - выполнить и запись в переменную last_record_id
    return {**orders.dict(), "id": last_record_id}

# 2. Чтение заказов из БД, read
@app.get("/orders_all/", response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)

# 2a. Выборка из базы данных
@app.get("/orders/", response_model=List[Order])
async def get_items_order(skip: int, limit: int):  # выборка - получить limit записей начиная с skip адреса(пропустив skip записей)
    query = orders.select().offset(skip).limit(limit)
    results = await database.fetch_all(query)
    return [dict(result) for result in results]

# 3. Чтение одного заказа из БД, read
@app.get("/products/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)

# 4. Обновление заказа в БД, update
@app.put("/orders/{product_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "id": order_id}

# 5. Удаление заказа из БД, delete
@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}



if __name__ == '__main__': 
    uvicorn.run("TASK_sem6:app", host="127.0.0.1", port=8000, reload=True) 


