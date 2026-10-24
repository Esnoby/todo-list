from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict


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
        if not v or not v.strip():
            raise ValueError("عنوان وظیفه نمی‌تواند خالی یا شامل صرفاً کاراکترهای فاصله باشد.")
        cleaned = v.strip()
        if len(cleaned) == 0:
            raise ValueError("عنوان وظیفه نامعتبر است.")
        return cleaned

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            cleaned = v.strip()
            return cleaned if cleaned else None
        return None


class TaskResponseSchema(BaseModel):
    """
    اسکیمای خروجی وظیفه برای ارسال به کلاینت
    """
    id: int
    title: str
    description: Optional[str] = None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
