from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.infrastructure.database import Base


class TaskModel(Base):
    """
    مدل جدول وظایف در پایگاه داده (SQLAlchemy ORM Model)
    مربوط به لایه زیرساخت (Infrastructure Layer)
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(150), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="انجام‌نشده")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<TaskModel(id={self.id}, title='{self.title}', status='{self.status}')>"
