# ۰. فراخوانی انواع ستون‌های SQLAlchemy و کلاس پایه {#2ecc71, 5}
# ==========================================
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.infrastructure.database import Base
# ==========================================

# ۱. تعریف مدل جدول وظایف در لایه زیرساخت (ORM Model) {#e67e22, 20}
# ==========================================
class TaskModel(Base):
    """
    مدل جدول وظایف در پایگاه داده (SQLAlchemy ORM Model)
    مربوط به لایه زیرساخت (Infrastructure Layer)
    """
    __tablename__ = "tasks"

    # افزایش سرعت جستجو و یکتاسازی رکوردها: تعریف کلید اصلی خودافزا همراه با ایندکس
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # جلوگیری از درج عنوان تهی در سطح دیتابیس: اعمال محدودیت nullable=False
    title = Column(String(150), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="انجام‌نشده")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        # تسهیل دیباگ و لاگ‌گیری: نمایش خلاصه مشخصات رکورد به صورت رشته خوانا
        return f"<TaskModel(id={self.id}, title='{self.title}', status='{self.status}')>"
# ==========================================
