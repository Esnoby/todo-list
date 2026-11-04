# ۰. فراخوانی کتابخانه‌های استاندارد و تایپ‌ها {#2ecc71, 5}
# ==========================================
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
# ==========================================

# ۱. تعریف موجودیت دامنه وظیفه و اعتبارسنجی قوانین پایه {#3498db, 25}
# ==========================================
@dataclass
class TaskEntity:
    """
    موجودیت دامنه وظیفه (Domain Entity)
    مستقل از هرگونه فریم‌ورک یا دیتابیس خارجی مطابق با اصول معماری تمیز و طراحی شی‌گرا
    """
    id: Optional[int]
    title: str
    description: Optional[str] = None
    status: str = "انجام‌نشده"
    created_at: Optional[datetime] = None

    def __post_init__(self):
        # جلوگیری از ثبت داده نامعتبر در هسته دامنه: بررسی خالی نبودن و حذف فواصل اضافی عنوان
        if not self.title or not self.title.strip():
            raise ValueError("عنوان وظیفه نمی‌تواند خالی یا صرفاً فاصله باشد.")
        self.title = self.title.strip()
        # یکپارچه‌سازی متن توضیحات: حذف فواصل ابتدا و انتهای رشته در صورت وجود
        if self.description:
            self.description = self.description.strip()
        # تضمین وجود زمان ایجاد: مقداردهی خودکار با زمان فعلی در صورت عدم ارسال
        if not self.created_at:
            self.created_at = datetime.utcnow()
# ==========================================
