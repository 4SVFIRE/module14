from fastapi import APIRouter,Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas import CreateTask, UpdateTask
from typing import Annotated
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])

@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    task = db.scalars(select(Task)).all()
    return task

@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id:int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
    return task

@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], user_id:int, create_task : CreateTask):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )

    db.execute(insert(Task).values(
            title=create_task.title,
            content=create_task.content,
            priority=create_task.priority,
            user_id=user_id,
            slug=slugify(create_task.title)
        )
    )
    db.commit()

    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put('/update')
async def update_task(db:Annotated[Session, Depends(get_db)], updata_task: UpdateTask, task_id:int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
    else:
        db.execute(update(Task).where(Task.id == task_id).values(
                                       title=updata_task.title,
                                       content=updata_task.content,
                                       priority=updata_task.priority))

        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Task update is successful!'
        }

@router.delete('/delete')
async def delete_task(db:Annotated[Session, Depends(get_db)], task_id:int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
    else:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Task delete is successful!'
        }