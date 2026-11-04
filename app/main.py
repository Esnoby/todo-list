# ۰. فراخوانی کتابخانه‌های هسته FastAPI، دیتابیس و روترها {#2ecc71, 9}
# ==========================================
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.infrastructure.database import Base, engine
from app.api.task_router import router as task_router
# ==========================================

# ۱. مدیریت چرخه حیات برنامه و ساخت جداول پایگاه‌داده {#1abc9c, 7}
# ==========================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # تضمین وجود جداول در SQLite پیش از پذیرش درخواست: ساخت خودکار اسکیمای دیتابیس
    Base.metadata.create_all(bind=engine)
    yield
# ==========================================

# ۲. پیکربندی نمونه اصلی برنامه، فایل‌های ایستا و مسیر صفحه وب {#3498db, 26}
# ==========================================
app = FastAPI(
    title="سامانه مدیریت وظایف (Todo App)",
    description="پروژه درس مهندسی نرم‌افزار - فاز اول: اسپرینت اول (توسعه قابلیت‌های پایه بر اساس اسکرام)",
    version="1.0.0",
    lifespan=lifespan
)

# تفکیک مسیرهای API از فایل‌های قالب: ثبت روتر مدیریت وظایف در برنامه اصلی
app.include_router(task_router)

# جلوگیری از خطای عدم وجود پوشه استاتیک: بررسی و ساخت خودکار مسیر فایل‌های ایستا
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", include_in_schema=False)
async def serve_frontend():
    """ارائه صفحه وب اصلی برنامه"""
    # نمایش رابط کاربری در مسیر ریشه: ارسال مستقیم فایل index.html به مرورگر
    index_path = os.path.join(static_dir, "index.html")
    return FileResponse(index_path)
# ==========================================
