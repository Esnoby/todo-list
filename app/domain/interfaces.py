from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import TaskEntity


class ITaskRepository(ABC):
    """
    اینترفیس مخزن داده (Repository Interface)
    طبق اصل وارونگی وابستگی (DIP) و اصل تفکیک اینترفیس (ISP)
    """

    @abstractmethod
    def create(self, task: TaskEntity) -> TaskEntity:
        """ذخیره‌سازی یک وظیفه جدید در پایگاه داده"""
        pass

    @abstractmethod
    def get_all(self) -> List[TaskEntity]:
        """بازیابی تمام وظایف ذخیره‌شده بر اساس جدیدترین زمان ایجاد"""
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[TaskEntity]:
        """بازیابی یک وظیفه بر اساس شناسه یکتا"""
        pass


class ITaskService(ABC):
    """
    اینترفیس لایه سرویس بیزینس (Service Interface)
    """

    @abstractmethod
    def create_task(self, title: str, description: Optional[str] = None) -> TaskEntity:
        """اعتبارسنجی بیزینس و ثبت وظیفه جدید"""
        pass

    @abstractmethod
    def list_tasks(self) -> List[TaskEntity]:
        """دریافت لیست تمام وظایف موجود در سیستم"""
        pass
