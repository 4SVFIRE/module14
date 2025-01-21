from fastapi import FastAPI, status, Body, HTTPException, Path
from pydantic import BaseModel
from typing import List,Annotated

app = FastAPI()

class User(BaseModel):
    id : int
    username : str
    age : int


users : List[User] = []


@app.get("/users", response_model=List[User])
async def get_all_users():
    return users


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