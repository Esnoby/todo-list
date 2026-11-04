# ۰. فراخوانی ابزارهای اعتبارسنجی Pydantic و تایپ‌های پایه {#2ecc71, 5}
# ==========================================
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
# ==========================================

# ۱. اسکیمای اعتبارسنجی ورودی ایجاد وظیفه (Input Validation) {#9b59b6, 38}
# ==========================================
class TaskCreateSchema(BaseModel):
    """
    اسکیمای اعتبارسنجی ورودی جهت ایجاد وظیفه جدید
    طبق نیازمندی اسپرینت: جلوگیری از ثبت وظیفه با عنوان خالی، فاصله خالی یا نامعتبر
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description="عنوان وظیفه (الزامی)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="توضیحات اختیاری وظیفه"
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        # مسدودسازی رشته‌های متشکل از فاصله خالی: بررسی مقدار پس از حذف فواصل ابتدا و انتها
        if not v or not v.strip():
            raise ValueError("عنوان وظیفه نمی‌تواند خالی یا شامل صرفاً کاراکترهای فاصله باشد.")
        cleaned = v.strip()
        if len(cleaned) == 0:
            raise ValueError("عنوان وظیفه نامعتبر است.")
        return cleaned

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        # استانداردسازی فیلد اختیاری توضیحات: تبدیل رشته صرفاً فاصله به مقدار None
        if v is not None:
            cleaned = v.strip()
            return cleaned if cleaned else None
        return None
# ==========================================

# ۲. اسکیمای ساختار خروجی وظیفه برای ارسال به کلاینت {#3498db, 14}
# ==========================================
class TaskResponseSchema(BaseModel):
    """
    اسکیمای خروجی وظیفه برای ارسال به کلاینت
    """
    id: int
    title: str
    description: Optional[str] = None
    status: str
    created_at: datetime

    # پشتیبانی از تبدیل مستقیم شیء دامنه به JSON: فعال‌سازی خواندن ویژگی‌های شیء
    model_config = ConfigDict(from_attributes=True)
# ==========================================
