from sqlalchemy.schema import CreateTable
from app.models.user import User
from app.models.task import Task

print(CreateTable(User.__table__))
print(CreateTable(Task.__table__))