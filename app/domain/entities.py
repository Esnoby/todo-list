from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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
        # بررسی اعتبارسنجی سطح دامنه (Domain Level Validation)
        if not self.title or not self.title.strip():
            raise ValueError("عنوان وظیفه نمی‌تواند خالی یا صرفاً فاصله باشد.")
        self.title = self.title.strip()
        if self.description:
            self.description = self.description.strip()
        if not self.created_at:
            self.created_at = datetime.utcnow()
