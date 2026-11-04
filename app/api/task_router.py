# ۰. فراخوانی ابزارهای مسیریابی FastAPI، اسکیماها و وابستگی‌ها {#2ecc71, 9}
# ==========================================
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.interfaces import ITaskService
from app.schemas.task_schema import TaskCreateSchema, TaskResponseSchema
from app.api.dependencies import get_task_service

router = APIRouter(prefix="/api/tasks", tags=["مدیریت وظایف"])
# ==========================================

# ۱. اندپوینت ثبت وظیفه جدید در سیستم (POST /api/tasks) {#e67e22, 26}
# ==========================================
@router.post(
    "",
    response_model=TaskResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="ثبت وظیفه جدید",
    description="ایجاد یک وظیفه جدید با عنوان و توضیحات اختیاری و ذخیره در پایگاه داده"
)
def create_task(
    task_in: TaskCreateSchema,
    service: ITaskService = Depends(get_task_service)
) -> TaskResponseSchema:
    try:
        # ارسال داده‌های اعتبارسنجی‌شده به لایه سرویس: ایجاد و ذخیره وظیفه در دیتابیس
        task = service.create_task(
            title=task_in.title,
            description=task_in.description
        )
        return TaskResponseSchema.model_validate(task)
    except ValueError as e:
        # تبدیل خطاهای منطق دامنه به پاسخ استاندارد HTTP: ارسال کد وضعیت ۴۰۰ به کلاینت
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
# ==========================================

# ۲. اندپوینت دریافت فهرست تمامی وظایف (GET /api/tasks) {#3498db, 15}
# ==========================================
@router.get(
    "",
    response_model=List[TaskResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="دریافت لیست وظایف",
    description="مشاهده تمامی وظایف ثبت‌شده در پایگاه داده"
)
def list_tasks(
    service: ITaskService = Depends(get_task_service)
) -> List[TaskResponseSchema]:
    # بازیابی لیست وظایف از لایه سرویس: تبدیل موجودیت‌های دامنه به مدل پاسخ استاندارد
    tasks = service.list_tasks()
    return [TaskResponseSchema.model_validate(task) for task in tasks]
# ==========================================
