from fastapi import FastAPI, status, Body, HTTPException, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List,Annotated

app = FastAPI()
templates = Jinja2Templates(directory='templates')

class User(BaseModel):
    id : int
    username : str
    age : int


users = []

@app.get("/")
async def get_main_page(request : Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users" : users})

@app.get("/users/{user_id}")
async def get_all_users(request:Request, user_id:int) -> HTMLResponse:
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user" : user})
        else:
            raise HTTPException(status_code=404, detail='User not found')

@app.post("/user/{username}/{age}",response_model=User)
async def create_user(
    username: Annotated[str,Path(min_length=3, max_length=30, description="Введите имя пользователя", example='Иван')],
    age: Annotated[int,Path(ge=0, le=100, description="Введите возраст пользователя", example='20')]):
    new_id = max((user.id for user in users), default=0) + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put("/users/{user_id}/{username}/{age}", response_model=User)
async def update_user(
    user_id: Annotated[int,Path(ge=0, le=100, description="Введите ID пользователя", example="11")],
    username: Annotated[str,Path(min_length=3, max_length=15, description="Введите имя", example="Алексей")],
    age: Annotated[int,Path(ge=0, le=100, description="Введите возраст", example=30)]):
        for user in users:
            if user.id == user_id:
                user.username = username
                user.age = age
                return user
            else:
                raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}",response_model=User)
async def delete_user(
    user_id: Annotated[int, Path(ge=0, le=100, description="Введите ID пользователя", example="11")]):
    for user in users:
        if user.id == user_id:
            users.pop(user_id)
            return user

    raise HTTPException(status_code=404, detail="User not found")