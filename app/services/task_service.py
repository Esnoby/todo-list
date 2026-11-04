# ۰. فراخوانی موجودیت دامنه و اینترفیس‌های انتزاعی {#2ecc71, 5}
# ==========================================
from typing import List, Optional
from app.domain.entities import TaskEntity
from app.domain.interfaces import ITaskRepository, ITaskService
# ==========================================

# ۱. پیاده‌سازی لایه سرویس و قوانین تجاری مدیریت وظایف {#1abc9c, 33}
# ==========================================
class TaskService(ITaskService):
    """
    لایه سرویس بیزینس (Business Logic Service)
    این کلاس مسئول هماهنگی و منطق کار با وظایف است و صرفاً به اینترفیس انتزاعی ITaskRepository وابسته است (DIP).
    """

    def __init__(self, repository: ITaskRepository):
        # رعایت اصل وارونگی وابستگی (DIP): دریافت مخزن از طریق اینترفیس انتزاعی
        self._repository = repository

    def create_task(self, title: str, description: Optional[str] = None) -> TaskEntity:
        """
        ایجاد و اعتبارسنجی وظیفه جدید مطابق نیازمندی‌های اسپرینت اول:
        - وضعیت اولیه تمام وظایف الزاماً «انجام‌نشده» است.
        - عنوان باید غیرخالی و معتبر باشد.
        """
        # اعمال قوانین دامنه پیش از ذخیره‌سازی: ساخت موجودیت با وضعیت پیش‌فرض «انجام‌نشده»
        task_entity = TaskEntity(
            id=None,
            title=title,
            description=description,
            status="انجام‌نشده"
        )
        return self._repository.create(task_entity)

    def list_tasks(self) -> List[TaskEntity]:
        """
        بازیابی فهرست تمام وظایف ثبت‌شده در سیستم
        """
        # تفویض واکشی اطلاعات به لایه مخزن: حفظ جدایی منطق تجاری از کوئری‌های دیتابیس
        return self._repository.get_all()
# ==========================================
