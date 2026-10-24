from typing import List, Optional
from app.domain.entities import TaskEntity
from app.domain.interfaces import ITaskRepository, ITaskService


class TaskService(ITaskService):
    """
    لایه سرویس بیزینس (Business Logic Service)
    این کلاس مسئول هماهنگی و منطق کار با وظایف است و صرفاً به اینترفیس انتزاعی ITaskRepository وابسته است (DIP).
    """

    def __init__(self, repository: ITaskRepository):
        self._repository = repository

    def create_task(self, title: str, description: Optional[str] = None) -> TaskEntity:
        """
        ایجاد و اعتبارسنجی وظیفه جدید مطابق نیازمندی‌های اسپرینت اول:
        - وضعیت اولیه تمام وظایف الزاماً «انجام‌نشده» است.
        - عنوان باید غیرخالی و معتبر باشد.
        """
        # ساخت موجودیت دامنه (درون سازنده این کلاس اعتبارسنجی‌های مربوط به رشته و خالی نبودن اجرا می‌شود)
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
        return self._repository.get_all()
