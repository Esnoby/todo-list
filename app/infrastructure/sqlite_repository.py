from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities import TaskEntity
from app.domain.interfaces import ITaskRepository
from app.infrastructure.models import TaskModel


class SQLiteTaskRepository(ITaskRepository):
    """
    پیاده‌سازی ملموس مخزن داده با استفاده از پایگاه داده SQLite و SQLAlchemy
    این کلاس به صورت جایگزین‌پذیر (Liskov Substitution) اینترفیس ITaskRepository را پیاده‌سازی می‌کند.
    """

    def __init__(self, db_session: Session):
        self._db = db_session

    def create(self, task: TaskEntity) -> TaskEntity:
        """افزودن وظیفه به پایگاه داده و برگرداندن موجودیت ذخیره شده"""
        db_task = TaskModel(
            title=task.title,
            description=task.description,
            status=task.status,
            created_at=task.created_at
        )
        self._db.add(db_task)
        self._db.commit()
        self._db.refresh(db_task)

        return self._to_entity(db_task)

    def get_all(self) -> List[TaskEntity]:
        """بازیابی کلیه وظایف به ترتیب نزولی زمان ثبت (جدیدترین‌ها اول)"""
        db_tasks = self._db.query(TaskModel).order_by(TaskModel.created_at.desc()).all()
        return [self._to_entity(item) for item in db_tasks]

    def get_by_id(self, task_id: int) -> Optional[TaskEntity]:
        """جستجوی وظیفه بر اساس شناسه یکتا"""
        db_task = self._db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not db_task:
            return None
        return self._to_entity(db_task)

    @staticmethod
    def _to_entity(model: TaskModel) -> TaskEntity:
        """تبدیل مدل زیرساخت (ORM) به موجودیت مستقل دامنه (Domain Entity)"""
        return TaskEntity(
            id=model.id,
            title=model.title,
            description=model.description,
            status=model.status,
            created_at=model.created_at
        )
