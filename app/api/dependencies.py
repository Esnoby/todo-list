from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.domain.interfaces import ITaskRepository, ITaskService
from app.infrastructure.sqlite_repository import SQLiteTaskRepository
from app.services.task_service import TaskService


def get_task_repository(db: Session = Depends(get_db)) -> ITaskRepository:
    """
    تزریق مخزن داده به عنوان اینترفیس ITaskRepository
    """
    return SQLiteTaskRepository(db_session=db)


def get_task_service(
    repo: ITaskRepository = Depends(get_task_repository)
) -> ITaskService:
    """
    تزریق لایه سرویس به عنوان اینترفیس ITaskService
    """
    return TaskService(repository=repo)
