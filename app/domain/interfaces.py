# ۰. فراخوانی ابزارهای کلاس انتزاعی و موجودیت دامنه {#2ecc71, 5}
# ==========================================
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import TaskEntity
# ==========================================

# ۱. تعریف قرارداد انتزاعی مخزن داده (Repository Interface) {#f1c40f, 25}
# ==========================================
class ITaskRepository(ABC):
    """
    اینترفیس مخزن داده (Repository Interface)
    طبق اصل وارونگی وابستگی (DIP) و اصل تفکیک اینترفیس (ISP)
    """

    @abstractmethod
    def create(self, task: TaskEntity) -> TaskEntity:
        """ذخیره‌سازی یک وظیفه جدید در پایگاه داده"""
        # اجبار کلاس‌های فرزند به پیاده‌سازی متد ثبت: تضمین قرارداد ذخیره‌سازی داده
        pass

    @abstractmethod
    def get_all(self) -> List[TaskEntity]:
        """بازیابی تمام وظایف ذخیره‌شده بر اساس جدیدترین زمان ایجاد"""
        # اجبار کلاس‌های فرزند به پیاده‌سازی متد واکشی لیست: یکسان‌سازی خروجی مخازن
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[TaskEntity]:
        """بازیابی یک وظیفه بر اساس شناسه یکتا"""
        # اجبار کلاس‌های فرزند به پیاده‌سازی جستجو با شناسه: پشتیبانی از دسترسی مستقیم
        pass
# ==========================================

# ۲. تعریف قرارداد انتزاعی سرویس بیزینس (Service Interface) {#9b59b6, 18}
# ==========================================
class ITaskService(ABC):
    """
    اینترفیس لایه سرویس بیزینس (Service Interface)
    """

    @abstractmethod
    def create_task(self, title: str, description: Optional[str] = None) -> TaskEntity:
        """اعتبارسنجی بیزینس و ثبت وظیفه جدید"""
        # جداسازی لایه کنترلر از پیاده‌سازی منطق تجاری: تعریف امضای استاندارد ایجاد وظیفه
        pass

    @abstractmethod
    def list_tasks(self) -> List[TaskEntity]:
        """دریافت لیست تمام وظایف موجود در سیستم"""
        # جداسازی لایه کنترلر از منطق بازیابی: تعریف امضای استاندارد دریافت فهرست وظایف
        pass
# ==========================================
